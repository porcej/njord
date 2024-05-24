#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NJORD

A buoy to augment a GNSS data stream based on known Wifi AP locations.


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
import re
import requests
import tests
from datetime import datetime
from aosclient import AOSClient, AOSKeys
from gnss import GNSS
import NetTools as NT


class NJORD:
    """
    A GNSS buoy that looks for access points with known locations and updates
    GNSS state based off of those known location, otherwise uses AOS API to 
    obtain GNSS State.

    Attributes:
        messengers (list): List of objects to send GNSS data, calls send_message(message) on the object
        access_points (dict): Dicts of known access points and their locations, keyed on SSID.
        update_time (datetime): Timestamp for the last configuration
        AOSUrl (str): AOS API Base URL
        config_url (str): URL for config file updates
        aos_username (str): AOS Username used to generate access token
        aos_password (str): AOS Password used to genreate access token
    """


    def __init__(self, config_file_path, aos_url=None, config_url=None, aos_username=None, aos_password=None):
        """
        Initialize the API client with the base URL and access token.

        Args:
            config_file_path (str): String representing local file path for config
            known_access_points (list): List of known access points.
            known_access_point_update_time: The update time for the known access points list.
        """
        self.messengers = []
        self.access_points = {}
        self.set_known_access_point_update_from_timestamp(0)
        self.config_local_path = config_file_path
        self.config_url = config_url

        # Load Configuration file
        try:
            self.load_json_configuration()
        except FileNotFoundError:
            pass 

        # If we have an configuraiton update URL, check for updates
        if config_url is not None:
            self.download_json_if_updated()
            try:
                self.load_json_configuration()
            except FileNotFoundError:
                pass


        # Create our AOS API Client
        self.AOSClient = AOSClient(base_url=aos_url, access_token=None, username=aos_username, password=aos_password)

        # Authenticate and get access token
        self.AOSClient. generate_authentication_token()

    def send_gnss(self, messege_type='TAIP_PV'):
        messege = self.generate_location_message(messege_type)
        for messenger in self.messengers:
            messenger.print(messege)


    def add_messanger(self, messenger):
        """
        """
        self.messengers.append(messenger)

        try:
            self.messengers[len(self.messengers)-1].start()
        except AttributeError:
            pass


    def set_known_access_point_update_from_timestamp(self, timestamp):
        """
        Sets the known_access_point_update_time from a unix timestamp.

        Args:
            timestamp (int): The Unix timestamp to convert.

        Returns:
            datetime: The corresponding datetime object.
        """
        try:
            # Ensure the timestamp is a valid integer
            if not isinstance(timestamp, int):
                raise ValueError("Timestamp must be an integer")
            
            # Convert the Unix timestamp to a datetime object
            self.known_access_point_update_time = datetime.fromtimestamp(timestamp)
            
        except Exception as e:
            raise ValueError(f"Error converting timestamp to datetime: {e}")



    def download_json_if_updated(self, verify_cert=False):
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

            if 'last_updated' not in data:
                raise ValueError("JSON file does not contain a 'last_updated' field.")

            json_last_updated_time = datetime.fromisoformat(data['last_updated'])

            if json_last_updated_time > self.known_access_point_update_time:
                try:
                    with open(self.self.config_local_path, 'w') as file:
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
        # Check if the configuration file exists
        if not os.path.exists(self.config_local_path):
            raise FileNotFoundError(f"The configuration file '{self.config_local_path}' does not exist.")
        
        try:
            # Open and load the JSON configuration file
            with open(self.config_local_path, "r") as file:
                config_data = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON from the configuration file: {e}")

        try:
            # Extract required data from the JSON configuration
            aps = config_data['KnownAps']
                    # Reorganize the list of known access points into a more digestable form
            self.access_points = {wn['Ssid']: [d for d in aps if d['Ssid'] == wn['Ssid']] for wn in aps}

            self.set_known_access_point_update_from_timestamp(config_data['LastUpdated'])
            self.aos_username = config_data['ApiUser']['Username']
            self.aos_password = config_data['ApiUser']['Password']
        except KeyError as e:
            raise KeyError(f"Missing required key in configuration data: {e}")


    def check_for_known_access_points(self, aos_resp):
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
                        # Reorganize the Wifi Network Access points to be keyed on BSSID
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


    def generate_location_message(self, message_type='TAIP_PV'):
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
                from pprint import pprint
                print(pprint(aos_resp))
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
            from pprint import pprint
            raise Exception(f"An unexpected error occurred: {pprint(e)}")












# Example usage:
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-c', '--config', default='data/config.json', help='File path for local config file.')
    parser.add_argument('-C', '--config_url', help='URL to aquire net config files.')

    parser.add_argument("-b", "--aosurl", default="https://192.168.1.1", help="Base URL for AOS API, defaults to \"https://192.168.1.1\", if a file path is provided, tries to read the file as a proxy API")
    parser.add_argument("-g", "--gateway", action="store_true", help="Sets the AOS API URL to the network's gateway.  Overrides --aosurl.")

    parser.add_argument('-U', '--udpport', default=21000, help='UDP port to send GNSS broadcast messages')
    parser.add_argument("-s", "--stdout", action='store_true', help="Prints TAIP messages to Standard Output")
    parser.add_argument('-t', '--tcpport', default=9011, help='TCP Port to send GNSS messages')
    parser.add_argument('-T', '--tcphost', help='TCP Server to send messages.')
    
    parser.add_argument("-u", "--username", type=str, help="Username for AOS authentication. - overrides config file")
    parser.add_argument("-p", "--password", type=str, help="Password for AOS authentication. - overrides config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    # parser.add_argument("-T", "--testaoswifi", type=str,  help="URL or file path to AOS API response, reads response, prints TAIP Message associated with scene Wifi Access Points.")
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument("-c", "--config", type=str, help="URL or file path of the JSON configuration file")
    # group.add_argument("-t", "--testaosgnss", type=str, help="URL or file path to AOS API response, reads response, prints TAIP Message and exits.")
    args = parser.parse_args()



    aos_url = args.aosurl

    if args.gateway:

        gateway_ip = NT.get_default_gateway_linux()
        if gateway_ip is None:
            gateway_ip = NT.get_default_gateway_macos()

        if gateway_ip is not None:
            aos_url = f'https://{gateway_ip}'

    app = NJORD(args.config,
                aos_url=aos_url,
                config_url=args.config_url,
                aos_username=args.username,
                aos_password=args.password)

    if args.tcpport is not None and args.tcphost is not None:
        app.add_messanger(NT.TCPClient('127.0.0.1', args.tcpport))

    if args.udpport is not None:
        app.add_messanger(NT.UDPClient(server_host='255.255.255.255', server_port=args.udpport))

    if args.stdout is not None:
        app.add_messanger(NT.PipeClient())

    # print(app.generate_location_message())
    app.send_gnss()



