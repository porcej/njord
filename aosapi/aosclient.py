#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aosclient.py

A client for Sierra Wireless Router's AirlinkOS API.

This module defines an AOSClient class that handles authentication and API requests to interact with the
AirlinkOS API.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import json
import os
import requests
from urllib.parse import urlparse
import warnings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import HTTPError, RequestException
from .aoskeys import AOSKeys


class AOSClient:
    """
    AOS client for a web service API that handles authentication and includes the access token in requests.

    Attributes:
        base_url (str): The base URL of the API.
        username (str): Username used to generate authentication token.
        password (str): Password used to generate authentication token.
        access_token (str): The access token used for authentication.
        headers (dict): Headers to be included in API requests.
        file_proxy_api_data (dict): Cached response data from file.
        verify_ssl (bool): Flag to verify SSL certificates.
    """

    GET_API_ENDPOINT = "/api/v1/db/get"
    AUTH_API_ENDPOINT = "/api/v1/auth/tokens"

    def __init__(self, base_url, access_token=None, username=None, password=None):
        """
        Initialize the API client with the base URL and access token.

        Args:
            base_url (str): The base URL of the API.
            access_token (str): The access token used for authentication.
            username (str): Username used to generate authentication token.
            password (str): Password used to generate authentication token.

        Raises:
            ValueError: If the base URL or file path is invalid.
        """
        self.verify_ssl = False
        warnings.simplefilter("ignore", InsecureRequestWarning)
        self.file_proxy_api_data = None

        result = urlparse(base_url)
        if all([result.scheme, result.netloc]):
            self.base_url = base_url
        elif os.path.isfile(base_url):
            self.base_url = None
            self.load_json_file(base_url)
        else:
            raise ValueError("Invalid base URL or file path provided")

        self.set_credentials(username, password)
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "accept": "application/vnd.api+json",
            "User-Agent": "AOSClient/0.0.1"
        }

    def set_credentials(self, username, password):
        """
        Set the username and password used to generate the authentication token.

        Args:
            username (str): Username used to generate authentication token.
            password (str): Password used to generate authentication token.
        """
        self.username = username
        self.password = password

    def generate_authentication_token(self):
        """
        Send a JSON containing login and password to the API's login endpoint and get the access token.

        Raises:
            HTTPError: If the request to the API returns an unsuccessful status code.
            RequestException: If there's an issue with the network request.
            ValueError: If the response JSON does not contain the access token.

        Returns:
            str: The access token obtained from the API.
        """
        if self.file_proxy_api_data is not None:
            self.access_token = "file access"
            return "file access"

        url = f"{self.base_url}{self.AUTH_API_ENDPOINT}"
        json_data = {
            "login": self.username,
            "password": self.password
        }

        try:
            response = requests.post(url, json=json_data, headers=self.headers, verify=self.verify_ssl)
            response.raise_for_status()  # Raises HTTPError for bad responses
        except HTTPError as http_err:
            raise HTTPError(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            raise RequestException(f"Request error occurred: {req_err}")

        response_json = response.json()
        self.access_token = response_json.get("data", {}).get("access_token")

        if not self.access_token:
            raise ValueError("Authentication failed: Access token not found in response")

        self.headers["Authorization"] = f"Bearer {self.access_token}"
        return self.access_token

    def get_data(self, fields):
        """
        Send a POST request to the specified API endpoint and retrieve data.

        Args:
            fields (list): The fields to include in the request payload.

        Raises:
            HTTPError: If the request to the API returns an unsuccessful status code.
            RequestException: If there's an issue with the network request.
            ValueError: If an error occurs during data retrieval.

        Returns:
            dict: The JSON response from the API containing the requested data.
        """
        if self.file_proxy_api_data is not None:
            return self.file_proxy_api_data

        url = f"{self.base_url}{self.GET_API_ENDPOINT}"
        json_data = {
            "fields": fields
        }

        try:
            response = requests.post(url, json=[json_data], headers=self.headers, verify=self.verify_ssl)
            response.raise_for_status()  # Raises HTTPError for bad responses
        except HTTPError as http_err:
            if response.status_code == 401:
                # Token might be expired, try to regenerate it
                self.generate_authentication_token()
                return self.get_data(fields)
            raise HTTPError(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            raise RequestException(f"Request error occurred: {req_err}")

        try:
            data = response.json().get("data", {})[0]
            if not data:
                raise ValueError("Failed to retrieve data: No data found in response")
            return data
        except ValueError as val_err:
            raise ValueError(f"Value error occurred: {val_err}")

    def load_json_file(self, file_path):
        """
        Sets file_proxy_api_data by loading a JSON file from a local file path.

        Args:
            file_path (str): The path to the JSON configuration file.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        try:
            with open(file_path, "r") as file:
                self.file_proxy_api_data = json.load(file).get('data', [None])[0]
        except FileNotFoundError:
            raise FileNotFoundError(f'Failed to read AOS API JSON {file_path}')
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f'Failed to decode AOS API JSON: {file_path}')
