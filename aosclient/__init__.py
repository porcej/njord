#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aosclient.py

A client for Sierra Wireless Router's Web Service API


"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"
__description__ = "A client for Sierra Wireless Router's Web Service API."
__app_name__ = "AOSClient"



import requests

class AOSClient:
    """
    AOS client for a web service API that handles authentication and includes the access token in requests.

    Attributes:
        base_url (str): The base URL of the API.
        access_token (str): The access token used for authentication.
        headers (dict): Headers to be included in API requests.
    """

    GET_API_ENDPOINT="/api/v1/db/get"
    AUTH_API_ENDPOINT="/api/v1/auth/tokens"

    def __init__(self, base_url, access_token):
        """
        Initialize the API client with the base URL and access token.

        Args:
            base_url (str): The base URL of the API.
            access_token (str): The access token used for authentication.
        """
        self.verify_ssl = False
        self.base_url = base_url
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "accept": "application/vnd.api+json",
            "User-Agent": f"{__app_name__}/{__version__}"  # Add your custom user agent here
        }

    def login_and_get_access_token(self, login, password):
        """
        Send a JSON containing login and password to the API's login endpoint and get the access token.

        Args:
            login (str): The login username.
            password (str): The login password.

        Returns:
            str: The access token obtained from the API, or None if authentication fails.
        """
        try:
            url = f"{self.base_url}{self.AUTH_API_ENDPOINT}"
            json_data = {
                "login": login,
                "password": password
            }
            response = requests.post(url, json=json_data, headers=self.headers, verify=self.verify_ssl)
            if response.status_code == 200:
                response_json = response.json()
                self.access_token = response_json.get("data", {}).get("access_token")
                self.headers["Authorization"] = f"Bearer {self.access_token}"
                return self.access_token
            else:
                print(f"Error: Authentication failed with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_data(self, fields):
        """
        Send a GET request to the specified API endpoint and retrieve data.

        Args:
            endpoint (str): The API endpoint to send the request to.

        Returns:
            dict: The JSON response from the API, or None if an error occurs.
        """
        try:
            url = f"{self.base_url}{self.GET_API_ENDPOINT}"
            json_data = {
                "fields": fields
            }
            response = requests.post(url, json=[json_data], headers=self.headers, verify=self.verify_ssl)
            if response.status_code == 200:
                return response.json().get("data", {})
            else:
                print(f"Error: Request failed with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

