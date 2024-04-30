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

import os
import argparse
import json
import requests
from urllib.parse import urlparse
from aosclient import AOSClient

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
        log_message("ERROR", f"Loading decoding JSON from {url}: {e}")
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


# Example usage:
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-c", "--config", required=True, type=str, help="URL or file path of the JSON configuration file")
    parser.add_argument("-b", "--aosurl", default="https://192.168.1.1", help="Base URL for AOS API, defaults to \"https://192.168.1.1\"")
    parser.add_argument("-u", "--username", type=str, help="Username for AOS authentication.")
    parser.add_argument("-p", "--password", type=str, help="Password for AOS authentication.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    args = parser.parse_args()

    if is_valid_url(args.config):
        config = load_json_from_url(args.config)
    elif is_valid_file_path(args.config):
        config = load_json_from_file(args.config)
    else:
        log_message("ERROR", "Please provide either a valid URL or a valid file path for the configuration JSON.")
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
