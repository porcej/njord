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
from urllib.parse import urlparse
from aosclient import AOSClient, AOSKeys
from gnss import GNSS


def load_json_from_url(url):
    """
    Loads a JSON configuration file from a given URL.

    Parameters:
    - url (str): The URL of the JSON configuration file.

    Returns:
    - dict or None: The parsed JSON data as a dictionary, or None if there was an error.
    """
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for bad status codes
        json_data = response.json()
        return json_data
    except requests.RequestException as e:
        log_message("ERROR", f"Loading JSON from {url}: {e}")
        return None

def load_json_from_file(file_path):
    """
    Loads a JSON configuration file from a local file path.

    Parameters:
    - file_path (str): The path to the JSON configuration file.

    Returns:
    - dict or None: The parsed JSON data as a dictionary, or None if there was an error.
    """
    try:
        with open(file_path, "r") as file:
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        log_message("ERROR", f"File, {file} not found!")
        return None
    except json.JSONDecodeError as e:
        log_message("ERROR", f"Loading JSON from {url}: {e}")
        return None

def is_valid_url(input_str):
    """
    Check if the input string is a valid URL.

    Args:
        input_str (str): The string to be checked.

    Returns:
        bool: True if the input string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(input_str)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_file_path(input_str):
    """
    Check if the input string is a valid file path.

    Args:
        input_str (str): The string to be checked.

    Returns:
        bool: True if the input string is a valid file path, False otherwise.
    """
    try:
        # Check if the path exists and is a file
        return os.path.isfile(input_str)
    except Exception:
        return False


def load_json_from_url_or_file(input_str):
    """
    Load JSON data from a URL or a file path.

    Args:
        input_str (str): The input string containing either a URL or a file path.

    Returns:
        dict or None: The loaded JSON object if successful, else None.
    """
    jobj = None       # Explicitly set Nonetype for Clairty
    if is_valid_url(input_str):
            jobj = load_json_from_url(input_str)
    elif is_valid_file_path(input_str):
            jobj = load_json_from_file(input_str)

    return jobj


def log_message(log_level, message):
    """
    Print a formatted log message.

    Args:
        log_level (str): The log level (e.g., "INFO", "WARNING", "ERROR").
        message (str): The message to be logged.

    Returns:
        None
    """
    formatted_message = f"{log_level.upper()}:\t{message}"
    print(formatted_message)


def check_for_known_access_points(config, aos_resp):
    """
    Checks if a known access point is in range.

    Args:
        conifg (dict): The configuration dictionary for the application including the KnownAccessPoints list.
        aos_resp (dict): Data object representing an AOS API JSON Response

    Returns:
        (dict or None): Access Point Dict for the first seen Access Point or None if no Access Points are in Range
    """
    # Reorganize the list of known access points into a more digestable form
    wifi_networks = {wn['Ssid']: [d for d in config if d['Ssid'] == wn['Ssid']] for wn in config}

    for ssid, wifi_access_points in wifi_networks.items():
        for band in ["band2400", "band5400"]:
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

    # No Access Points Founds
    return None


def test_aos_wifi_response(file_or_url, config):
    """
    Reads JSON data from a file path or URL, generates a TAIP A PV message based on a known Wifi AP, prints the message to standard output,
    and exits with an appropriate return code.

    Args:
        file_or_url (str): The file path or URL from which to read the JSON data.
        conifg (dict): The configuration dictionary for the application including the KnownAccessPoints list.

    """

    aos_resp = load_json_from_url_or_file(file_or_url)

    # Extract the data Elements from the AOS Json Response
    aos_resp = aos_resp['data'][0]
    
    if aos_resp is None:
        raise Exception("Please provide either a valid URL or a valid file path for the AOS response JSON.")
    
    access_point = check_for_known_access_points(config, aos_resp)
    if access_point is not None:
        gnss = GNSS()
        gnss.set_basic_values(fixtime=None, 
                              latitude=access_point['Latitude'],
                              longitude=access_point['Longitude'],
                              heading=0,
                              speed=0,
                              taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID],
                              source=9,
                              age=2)
        taip_message = gnss.taip_pv_message()
        print(taip_message)
    else:
        print("No Access Points seen.")






def test_aos_gnss_response(file_or_url):
    """
    Reads JSON data from a file path or URL, generates a TAIP A PV message, prints the message to standard output,
    and exits with an appropriate return code.

    Args:
        file_or_url (str): The file path or URL from which to read the JSON data.

    """
    aos_resp = load_json_from_url_or_file(file_or_url)
    if aos_resp is None:
        raise Exception("Please provide either a valid URL or a valid file path for the AOS response JSON.")

    aos_resp = aos_resp['data'][0]

    gnss = GNSS()
    gnss.set_basic_values(fixtime=aos_resp[AOSKeys.GNSS_FIXTIME], 
                          latitude=aos_resp[AOSKeys.GNSS_LATITUDE],
                          longitude=aos_resp[AOSKeys.GNSS_LONGITUDE],
                          heading=aos_resp[AOSKeys.GNSS_HEADING],
                          speed=aos_resp[AOSKeys.GNSS_SPEED],
                          taip_id=aos_resp[AOSKeys.GNSS_TAIP_ID])
    taip_message = gnss.taip_pv_message()
    print(taip_message)

# Example usage:
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-b", "--aosurl", default="https://192.168.1.1", help="Base URL for AOS API, defaults to \"https://192.168.1.1\"")
    parser.add_argument("-u", "--username", type=str, help="Username for AOS authentication.")
    parser.add_argument("-p", "--password", type=str, help="Password for AOS authentication.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("-T", "--testaoswifi", type=str,  help="URL or file path to AOS API response, reads response, prints TAIP Message associated with scene Wifi Access Points.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--config", type=str, help="URL or file path of the JSON configuration file")
    group.add_argument("-t", "--testaosgnss", type=str, help="URL or file path to AOS API response, reads response, prints TAIP Message and exits.")
    args = parser.parse_args()


    # Run Test Harness for Parsing AOS API Respone and Generating a TAIP A PV Message
    if args.testaosgnss is not None:
        test_aos_gnss_response(args.testaosgnss)
        exit(0)

    # Load Wifi AP Config
    config = load_json_from_url_or_file(args.config)
    if config is None:
        log_message("ERROR", "Please provide either a valid URL or a valid file path for the configuration JSON.")
        exit(1)

    # Run test Harness for PArsing AOS API Respone and Wifi Config then generating a TAIP A PV Message
    if args.testaoswifi is not None:
        test_aos_wifi_response(args.testaoswifi, config)
        exit(1)


    if config:
        print("Configuration read successfully:")
        print(json.dumps(config, indent=4))

        # "https://192.168.1.1"
        client = AOSClient(args.aosurl, access_token=None)

        # Authenticate and get access token
        access_token = client.login_and_get_access_token(args.username, args.password)

        if access_token:
            # Use the client to make authenticated requests
            fields = ["net.wifi.ssid", "location.gnss"]
            data_response = client.get_data(fields)
            if data_response:
                print("Data received successfully:")
                print(data_response)
            else:
                log_message("WARN", "API Data not loaded")
        else:
            log_message("WARN", "API Authentication Failed")
