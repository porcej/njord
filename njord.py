#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NJORD

A buoy to augment a GNSS data stream based on known Wifi AP locations.

This module provides the NJORD class that updates the GNSS state based on known Wifi AP locations or the AirlinkOS API.
It also includes a main function to parse arguments and initialize the NJORD application.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"
__description__ = "A buoy to augment a GNSS data stream based on known Wifi AP locations."
__app_name__ = "NJORD"

import argparse
import heapq
import json
import os
import requests
import sys
import time
from datetime import datetime, timedelta
from requests.exceptions import HTTPError, RequestException
from aosapi import AOSClient, AOSKeys
from gnss import GNSS
from gnss.gnsshelpers import TAIP
import NetTools as NT


class ConfigJsonKeys:
    """
    Constants representing JSON keys for the configuration file.

    Attributes:
        LAST_UPDATED (str): The key for the last updated timestamp.
        API_USER (str): The key for the API user section.
        USERNAME (str): The key for the username.
        PASSWORD (str): The key for the password.
        KNOWN_APS (str): The key for the known access points.
    """
    LAST_UPDATED = 'LastUpdated'
    API_USER = 'ApiUser'
    USERNAME = 'Username'
    PASSWORD = 'Password'
    KNOWN_APS = 'KnownAps'

    @staticmethod
    def get_username(config: dict) -> str:
        """
        Retrieve the username from the configuration dictionary.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            str: The username from the configuration.

        Raises:
            KeyError: If the API_USER or USERNAME key is not found in the config.
        """
        try:
            return config[ConfigJsonKeys.API_USER][ConfigJsonKeys.USERNAME]
        except KeyError as e:
            raise KeyError(f"Missing key in configuration: {e}")

    @staticmethod
    def get_password(config: dict) -> str:
        """
        Retrieve the password from the configuration dictionary.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            str: The password from the configuration.

        Raises:
            KeyError: If the API_USER or PASSWORD key is not found in the config.
        """
        try:
            return config[ConfigJsonKeys.API_USER][ConfigJsonKeys.PASSWORD]
        except KeyError as e:
            raise KeyError(f"Missing key in configuration: {e}")




class NJORD:
    """
    A GNSS buoy that looks for access points with known locations and updates
    GNSS state based off of those known locations, otherwise uses AOS API to 
    obtain GNSS State.

    Attributes:
        messengers (list): List of objects to send GNSS data, calls send_message(message) on the object.
        access_points (dict): Dicts of known access points and their locations, keyed on SSID.
        next_config_update (datetime): Timestamp for the next configuration update.
        config_update_interval (int): Interval between config updates in seconds.
        config_local_path (str): Path to the local configuration file.
        config_url (str): URL for configuration file updates.
        AOSClient (AOSClient): Client for interacting with the AOS API.
        gnss (object): Current GNSS Data, invalidated after every request
    """

    def __init__(self, config_file_path: str, config_update_interval: int = None, aos_url: str = None, config_url: str = None, aos_username: str = None, aos_password: str = None):
        """
        Initialize the NJORD instance with configuration and API details.

        Args:
            config_file_path (str): Path to the local configuration file.
            config_update_interval (int): Number of seconds between config file updates.
            aos_url (str): AOS API base URL.
            config_url (str): URL for configuration file updates.
            aos_username (str): AOS Username for authentication.
            aos_password (str): AOS Password for authentication.
            gnss (object): Current GNSS Data, invalidated after every request
            taip_id (int): Place holder for taip_id when using taip_id alias
        """
        self.messengers = []
        self.access_points = {}
        self.file_creds = True
        self.next_config_update = datetime(1970, 1, 1, 0, 0, 0) # set to the distant past
        self.config_update_interval = config_update_interval
        self.set_known_access_point_update_from_timestamp(0)
        self.config_local_path = config_file_path
        self.config_url = config_url
        self.gnss = GNSS()
        taip_id = '0000'

        # This is a hack to accomadate the Central Square Mobile Clinets
        self.gnss.age = TAIP.Age.FRESH

        if aos_username is not None and aos_password is not None:
            self.file_creds = False

        # Create our AOS API Client
        self.AOSClient = AOSClient(base_url=aos_url, access_token=None, username=aos_username, password=aos_password)
        
        try:
            self.load_json_configuration()
        except FileNotFoundError:
            pass

        self.update_config()

        # Authenticate and get access token
        self.AOSClient.generate_authentication_token()

    def apply_taip_alias(self, taip_alias: str):
        """
        Apply a TAIP alias to the current TAIP ID.

        Args:
            taip_alias (str): The TAIP alias to apply. This can be a fixed ID or a
                              mathematical operation (e.g., '+100' or '-50').

        Raises:
            ValueError: If the alias is not properly formatted.
        """
        self.taip_id = self.gnss.taip_id

        if isinstance(taip_alias, int):
            self.gnss.taip_id = f'{taip_alias:04d}'[-4:]
        elif isinstance(taip_alias, str):
            taip_id = int(self.gnss.taip_id)
            if taip_alias.startswith('+'):
                taip_id  += int(taip_alias[1:])
            elif taip_alias.startswith('-'):
                taip_id  -= int(taip_alias[1:])
            else:
                taip_id  = int(taip_alias)
            self.gnss.taip_id = f'{taip_id:04d}'[-4:]

    def update_config(self):
        """
        Load and update the configuration file if needed.
        """
        if self.config_url is not None and self.config_update_interval is not None:
            now = datetime.now()
            if now > self.next_config_update:
                # If we have a configuration update URL, check for updates
                
                self.download_json_if_updated()
                try:
                    self.load_json_configuration()
                except FileNotFoundError:
                    raise FileNotFoundError('Unable to read configuration file.')
                self.next_config_update = datetime.now() + timedelta(seconds=self.config_update_interval)

    def send_gnss(self):
        """
        Sends the GNSS message to all registered messengers.

        """
        self.get_location()
        for messenger in self.messengers:
            if messenger['taip_alias'] is not None:
                self.apply_taip_alias(messenger['taip_alias'])
            message  = self.gnss.get_message(message_type=messenger['message_type'])
            messenger['carrier'].print(message)
            if messenger['taip_alias'] is not None:
                self.gnss.taip_id = self.taip_id


    def add_messenger(self, messenger: object):
        """
        Adds a messenger to the list of messengers.

        Args:
            messenger: An object with a send_message method to send the GNSS data.
        """
        self.messengers.append(messenger)
        try:
            self.messengers[-1]['carrier'].start()
        except AttributeError:
            pass

    def set_known_access_point_update_from_timestamp(self, timestamp: int):
        """
        Sets the known_access_point_update_time from a Unix timestamp.

        Args:
            timestamp (int): The Unix timestamp to convert.
        """
        try:
            if not isinstance(timestamp, int):
                raise ValueError("Timestamp must be an integer")
            self.known_access_point_update_time = datetime.fromtimestamp(timestamp)
        except Exception as e:
            raise ValueError(f"Error converting timestamp to datetime: {e}")

    def download_json_if_updated(self, verify_cert: bool = False):
        """
        Downloads a JSON file from the given URL and saves it to the local file path
        if the JSON file's last updated time is newer than the given datetime.

        Args:
            verify_cert (bool): A Boolean indicating whether to verify the server's TLS certificate.

        Raises:
            ValueError: If the JSON file does not contain a valid 'last_updated' field.
            HTTPError: If the request to the URL returns an unsuccessful status code.
            RequestException: If there's an issue with the network request.
            Exception: If there is an error during the file writing process.
        """
        try:
            response = requests.get(self.config_url, verify=verify_cert)
            response.raise_for_status()  # Check for HTTP request errors
        except HTTPError as http_err:
            raise HTTPError(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            raise RequestException(f"Request error occurred: {req_err}")

        try:
            data = response.json()

            if ConfigJsonKeys.LAST_UPDATED not in data:
                raise ValueError(f"JSON file does not contain a '{ConfigJsonKeys.LAST_UPDATED}' field.")

            json_last_updated_time = datetime.fromtimestamp(data[ConfigJsonKeys.LAST_UPDATED])

            if json_last_updated_time > self.known_access_point_update_time:
                try:
                    with open(self.config_local_path, 'w') as file:
                        json.dump(data, file, indent=4)
                except Exception as e:
                    raise Exception(f"Error writing JSON file: {e}")
            else:
                # Current configuration is newer so do nothing
                pass
        except ValueError as val_err:
            raise ValueError(f"Error processing JSON data: {val_err}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def load_json_configuration(self):
        """
        Loads a JSON configuration file from the file system.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
            JSONDecodeError: If the JSON file cannot be processed.
            KeyError: If required keys are missing in the JSON data.
        """
        if not os.path.exists(self.config_local_path):
            raise FileNotFoundError(f"The configuration file '{self.config_local_path}' does not exist.")

        try:
            with open(self.config_local_path, "r") as file:
                config_data = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON from the configuration file: {e}")

        try:
            aps = config_data[ConfigJsonKeys.KNOWN_APS]
            self.access_points = {wn['Ssid']: [d for d in aps if d['Ssid'] == wn['Ssid']] for wn in aps}
            self.set_known_access_point_update_from_timestamp(config_data[ConfigJsonKeys.LAST_UPDATED])
            if self.file_creds:
                self.AOSClient.set_credentials(ConfigJsonKeys.get_username(config_data),
                                               ConfigJsonKeys.get_password(config_data))
        except KeyError as e:
            raise KeyError(f"Missing required key in configuration data: {e}")

    def check_for_known_access_points(self, aos_resp: dict) -> dict:
        """
        Checks if a known access point is in range and returns its position.

        Args:
            aos_resp (dict): Data object representing an AOS API JSON Response.

        Returns:
            dict or None: Access Point for the first seen Access Point or None if no Access Points are in range.

        Raises:
            ValueError: If the aos_resp is not a dictionary.
            KeyError: If required keys are missing in aos_resp.
        """
        if not isinstance(aos_resp, dict):
            raise ValueError("The aos_resp parameter must be a dictionary.")

        try:
            for ssid, wifi_access_points in self.access_points.items():
                for band in AOSKeys.WIFI_BANDS:
                    ap_key = AOSKeys.generate_wifi_key(ssid, band=band)

                    if ap_key in aos_resp:
                        access_points = {ap['Bssid']: ap for ap in wifi_access_points}
                        bssids = list(access_points.keys())

                        ap_info_str_list = aos_resp[ap_key].strip().split('\n\n')
                        for ap_info_str in ap_info_str_list:
                            tokens = ap_info_str.strip().split('\n')
                            aos_wifi_info = {k.strip(): v.strip() for k, v in (token.split(':', 1) for token in tokens)}
                            if aos_wifi_info['BSSID'] in bssids:
                                return access_points[aos_wifi_info['BSSID']]
        except KeyError as e:
            raise KeyError(f"Missing required key in AOS response data: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def get_location(self):
        """
        Sets position (gnss) from Access Point if available or uses AOS API location if no Wifi APs are available.

        Raises:
            KeyError: If required keys are missing in the AOS API response.
            Exception: If an unexpected error occurs during processing.
        """
        try:
            fields = ["net.wifi.ssid", "location.gnss"]
            aos_resp = self.AOSClient.get_data(fields)
            ap_info = self.check_for_known_access_points(aos_resp)

            if ap_info is not None:
                self.gnss.set_basic_values(fixtime=None,
                                      latitude=ap_info['Latitude'],
                                      longitude=ap_info['Longitude'],
                                      heading=0,
                                      speed=0,
                                      taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID],
                                      source=9)
            else:
                self.gnss.set_basic_values(fixtime=aos_resp[AOSKeys.GNSS_FIXTIME],
                                      latitude=aos_resp[AOSKeys.GNSS_LATITUDE],
                                      longitude=aos_resp[AOSKeys.GNSS_LONGITUDE],
                                      heading=aos_resp[AOSKeys.GNSS_HEADING],
                                      speed=aos_resp[AOSKeys.GNSS_SPEED],
                                      taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID])

        except KeyError as e:
            raise KeyError(f"Missing required key in AOS response data: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

def parse_arguments():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description=f'{__app_name__} - {__description__}')
    parser.add_argument(
        '-c', '--config',
        default='data/config.json',
        help='File path for local config file.'
    )
    parser.add_argument(
        '-C', '--config_url',
        help='URL to acquire net config files.'
    )
    parser.add_argument(
        '-a', '--aosurl',
        default='https://192.168.1.1',
        help='Base URL for AOS API, defaults to "https://192.168.1.1", if a file path is provided, tries to read the file as a proxy API.'
    )
    parser.add_argument(
        "-g", "--gateway",
        action="store_true",
        help="Sets the AOS API URL to the network's gateway.  Overrides --aosurl."
    )
    parser.add_argument(
        '-U', '--udpport',
        type=int,
        help='UDP port to send GNSS broadcast messages'
    )
    parser.add_argument(
        "-s", "--stdout",
        action='store_true',
        help="Prints TAIP messages to Standard Output"
    )
    parser.add_argument(
        '-t', '--tcpport',
        type=int,
        help='TCP Port to send GNSS messages.'
    )
    parser.add_argument(
        '-T', '--tcphost',
        help='TCP Server to send messages.'
    )
    parser.add_argument(
        '-u', '--username',
        type=str,
        help='Username for AOS authentication. - overrides config file'
    )
    parser.add_argument(
        '-p', '--password',
        type=str,
        help='Password for AOS authentication. - overrides config file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print verbose output'
    )
    parser.add_argument(
        '-B', '--beacon',
        type=int,
        help='Sets the beacon interval in seconds'
    )
    parser.add_argument(
        '-M', '--messagetype',
        choices=['taip_pv', 'nmea_rmc', 'all'],
        default='taip_pv',
        help='Specify the message type (taip_pv, nmea_rmc, or all). Default is "taip_rmc".'
    )
    parser.add_argument(
        "-i", "--update",
        type=int,
        help='Sets the config update interval in seconds.'
    )
    parser.add_argument(
        '-m', '--message', 
        action='append', 
        nargs=4, 
        metavar=('MSG_TYPE', 'PROTOCOL', 'PORT', 'HOST'),
        help='Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PROTOCOL (TCP/UDP), PORT (int), HOST (str)')

    parser.add_argument(
        '-z', '--message-alias-taip', 
        action='append', 
        nargs=5, 
        metavar=('MSG_TYPE', 'PROTOCOL', 'PORT', 'HOST', 'ALIAS'),
        help='Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PROTOCOL (TCP/UDP), PORT (int), HOST (str), TAIP ALIAS (fixed value or +N/-N)')

    parser.add_argument(
        '-b', '--broadcast-message', 
        action='append', 
        nargs=2, 
        metavar=('MSG_TYPE', 'PORT'),
        help='Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PORT (int)')

    parser.add_argument(
        '-Z', '--broadcast-message-alias-taip', 
        action='append', 
        nargs=3, 
        metavar=('MSG_TYPE', 'PORT', 'ALIAS'),
        help='Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PORT (int), TAIP ALIAS (fixed value or +N/-N)')

    return parser.parse_args()

def make_message_dict(
    msg_type: str,
    protocol: str,
    host: str = None,
    port: int = None,
    taip_alias: str = None
) -> dict:
    """
    Create a dictionary representing a message configuration.

    Args:
        msg_type (str): The type of the message. Must be either 'TAIP_PV' or 'NMEA_RMC'.
        protocol (str): The communication protocol. Must be either 'TCP' or 'UDP'.
        port (int, optional): The port number. Must be an integer if provided.
        host (str, optional): The host address. Must be provided.
        taip_alias (str, optional): An alias for the TAIP ID. ().

    Returns:
        dict: A dictionary containing the message configuration.

    Raises:
        ValueError: If msg_type is not 'TAIP_PV' or 'NMEA_RMC'.
        ValueError: If protocol is not 'TCP' or 'UDP'.
        ValueError: If port is provided and is not an integer.
        ValueError: If host is not provided.
    """
    msg_type = msg_type.upper()
    protocol = protocol.upper()

    if msg_type not in ['TAIP_PV', 'NMEA_RMC']:
        raise ValueError(f"Invalid message type: {msg_type}")
    
    if protocol not in ['TCP', 'UDP']:
        raise ValueError(f"Invalid protocol: {protocol}")
    
    if port is not None:
        try:
            port = int(port)
        except (ValueError, TypeError):
            raise ValueError(f"Port must be an integer: {port}")
    else:
        raise ValueError("Port must be provided")

    if host is None:
        raise ValueError("Host must be provided")

    return {
        'msg_type': msg_type,
        'protocol': protocol,
        'port': port,
        'host': host,
        'alias': taip_alias
    }


def validate_and_process_message_arguments(args: object):
    """
    Validates and processes the command line arguments.

    Args:
        Args (object): Args object.

    Returns:
        list of dict: List of message parameters.

    Raises:
        ValueError: If the any of the message parameters are not valid.
    """
    messages = []
    if args.message is not None:
        for msg in args.message:
            msg_type, protocol, port, host = msg
            msg_dict = make_message_dict(msg_type=msg_type, protocol=protocol, port=port, host=host)
            messages.append(msg_dict)

    if args.broadcast_message is not None:
        for msg in args.broadcast_message:
            msg_type, port = msg
            msg_dict = make_message_dict(msg_type=msg_type, protocol='UDP', port=port, host='255.255.255.255')
            messages.append(msg_dict)

    if args.message_alias_taip is not None:
        for msg in message_alias_taip:
            msg_type, protocol, port, host, alias = msg
            msg_dict = make_message_dict(msg_type=msg_type, protocol=protocol, port=port, host=host, taip_alias=alias)
            messages.append(msg_dict)

    if args.broadcast_message_alias_taip is not None:
        for msg in args.broadcast_message_alias_taip:
            msg_type, port, alias = msg
            msg_dict = make_message_dict(msg_type=msg_type, protocol='UDP', port=port, host='255.255.255.255',  taip_alias=alias)
            messages.append(msg_dict)
        

    return messages

def main():
    """
    The main function to parse arguments and initialize the NJORD application.
    """
    args = parse_arguments()
    

    try:
        messages = validate_and_process_message_arguments(args)
    except ValueError as val_err:
        print(f'Parsing message argument: {val_err}', file=sys.stderr)
        exit(5)

    aos_url = args.aosurl

    if args.gateway:
        gateway_ip = NT.get_default_gateway_linux()
        if gateway_ip is None:
            gateway_ip = NT.get_default_gateway_macos()

        if gateway_ip is not None:
            aos_url = f'https://{gateway_ip}'

    app = NJORD(config_file_path=args.config,
                config_update_interval=args.update,
                aos_url=aos_url,
                config_url=args.config_url,
                aos_username=args.username,
                aos_password=args.password)

    messenger = {'message_type': args.messagetype.upper(), 'carrier': None}

    if args.tcpport is not None and args.tcphost is not None:
        messenger['carrier'] = NT.TCPClient(args.tcphost, args.tcpport)
        
    if args.udpport is not None:
        messenger['carrier'] = NT.UDPClient(server_host='255.255.255.255', server_port=args.udpport)
        app.add_messenger(messenger)


    if args.stdout:
        messenger['carrier'] = NT.PipeClient()
        app.add_messenger(messenger)

    for msg in messages:
        messenger = {'message_type': msg['msg_type'], 'carrier': None, 'taip_alias': msg['alias']}
        if msg['protocol'] == 'UDP':
            messenger['carrier'] = NT.UDPClient(msg['host'], msg['port'])
        elif msg['protocol'] == 'TCP':
            messenger['carrier'] = NT.TCPClient(msg['host'], msg['port'])
            
        app.add_messenger(messenger)


    update_config_time = time

    if args.beacon is not None:
        while(1):
            app.send_gnss()
            app.update_config()
            time.sleep(args.beacon)

    else:
        app.send_gnss()




if __name__ == "__main__":
    main()
