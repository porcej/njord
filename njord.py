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
import json
import os
import requests
import time
from datetime import datetime, timedelta
from requests.exceptions import HTTPError, RequestException
from aosapi import AOSClient, AOSKeys
from gnss import GNSS
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
        """
        self.messengers = []
        self.access_points = {}
        self.next_config_update = datetime(1970, 1, 1, 0, 0, 0) # set to the distant past
        self.config_update_interval = config_update_interval
        self.set_known_access_point_update_from_timestamp(0)
        self.config_local_path = config_file_path
        self.config_url = config_url
        try:
            self.load_json_configuration()
        except FileNotFoundError:
            pass        

        self.update_config()

        # Create our AOS API Client
        self.AOSClient = AOSClient(base_url=aos_url, access_token=None, username=aos_username, password=aos_password)

        # Authenticate and get access token
        self.AOSClient.generate_authentication_token()

    def update_config(self):
        """
        Load and update the configuration file if needed.
        """
        if self.config_url is not None and self.config_update_interval is not None:
            now = datetime.datetime.now()
            if now > self.next_config_update:
                # If we have a configuration update URL, check for updates
                
                self.download_json_if_updated()
                try:
                    self.load_json_configuration()
                except FileNotFoundError:
                    raise FileNotFoundError('Unable to read configuration file.')
                self.next_config_update = datetime.datetime.now() + timedelta(seconds=self.config_update_interval)


    def send_gnss(self, message_type: str = 'TAIP_PV'):
        """
        Sends the GNSS message to all registered messengers.

        Args:
            message_type (str): The type of message to generate. Default is 'TAIP_PV'.
        """
        message = self.generate_location_message(message_type)
        for messenger in self.messengers:
            messenger.print(message)
        message = self.generate_location_message('NMEA_RMC')
        for messenger in self.messengers:
            messenger.print(message)

    def add_messenger(self, messenger: object):
        """
        Adds a messenger to the list of messengers.

        Args:
            messenger: An object with a send_message method to send the GNSS data.
        """
        self.messengers.append(messenger)
        try:
            self.messengers[-1].start()
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
            self.aos_username = ConfigJsonKeys.get_username(config_data)
            self.aos_password = ConfigJsonKeys.get_password(config_data)
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

    def generate_location_message(self, message_type: str = 'TAIP_PV') -> str:
        """
        Sets position from Access Point if available or uses AOS API location if no Wifi APs are available.

        Args:
            message_type (str): The type of message to generate. Default is 'TAIP_PV'.

        Returns:
            str: The generated location message.

        Raises:
            KeyError: If required keys are missing in the AOS API response.
            Exception: If an unexpected error occurs during processing.
        """
        try:
            fields = ["net.wifi.ssid", "location.gnss"]
            aos_resp = self.AOSClient.get_data(fields)
            ap_info = self.check_for_known_access_points(aos_resp)
            gnss = GNSS()

            if ap_info is not None:
                gnss.set_basic_values(fixtime=None,
                                      latitude=ap_info['Latitude'],
                                      longitude=ap_info['Longitude'],
                                      heading=0,
                                      speed=0,
                                      taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID],
                                      source=9,
                                      age=2)
            else:
                gnss.set_basic_values(fixtime=aos_resp[AOSKeys.GNSS_FIXTIME],
                                      latitude=aos_resp[AOSKeys.GNSS_LATITUDE],
                                      longitude=aos_resp[AOSKeys.GNSS_LONGITUDE],
                                      heading=aos_resp[AOSKeys.GNSS_HEADING],
                                      speed=aos_resp[AOSKeys.GNSS_SPEED],
                                      taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID])

            return gnss.get_message(message_type=message_type)
        except KeyError as e:
            raise KeyError(f"Missing required key in AOS response data: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")


def main():
    """
    The main function to parse arguments and initialize the NJORD application.
    """
    parser = argparse.ArgumentParser(description='NJORD GNSS Buoy Configuration')
    parser.add_argument('-c', '--config', default='data/config.json', help='File path for local config file.')
    parser.add_argument('-C', '--config_url', help='URL to acquire net config files.')

    parser.add_argument("-a", "--aosurl", default="https://192.168.1.1",
                        help='Base URL for AOS API, defaults to "https://192.168.1.1", if a file path is provided, tries to read the file as a proxy API')
    parser.add_argument("-g", "--gateway", action="store_true", help="Sets the AOS API URL to the network's gateway.  Overrides --aosurl.")

    parser.add_argument('-U', '--udpport', type=int, default=21000, help='UDP port to send GNSS broadcast messages')
    parser.add_argument("-s", "--stdout", action='store_true', help="Prints TAIP messages to Standard Output")
    parser.add_argument('-t', '--tcpport', type=int, default=9011, help='TCP Port to send GNSS messages')
    parser.add_argument('-T', '--tcphost', help='TCP Server to send messages.')

    parser.add_argument("-u", "--username", type=str, help="Username for AOS authentication. - overrides config file")
    parser.add_argument("-p", "--password", type=str, help="Password for AOS authentication. - overrides config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("-b", "--beacon", type=int, help="Sets the beacon interval in seconds")
    parser.add_argument("-i", "--update", type=int, help="Sets the config update internal in seconds")

    args = parser.parse_args()

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

    if args.tcpport is not None and args.tcphost is not None:
        app.add_messenger(NT.TCPClient(args.tcphost, args.tcpport))

    if args.udpport is not None:
        app.add_messenger(NT.UDPClient(server_host='255.255.255.255', server_port=args.udpport))

    if args.stdout:
        app.add_messenger(NT.PipeClient())

    app.send_gnss()

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
