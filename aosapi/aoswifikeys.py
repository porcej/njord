#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aoskeys.py

Keys for JSON Response in the Airlink OS API.

This module defines the AOSKeys class that provides constants representing JSON keys for AOS's API response
and a method to generate WiFi keys dynamically.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

class AOSWifiKeys:
    """
    Constants representing JSON keys for AOS's API response.

    Attributes:
        BANDS (list): List of WiFi bands.
    """

    BANDS = ["band2400", "band5400"]

    @staticmethod
    def ap_list(ssid, band="band2400"):
        """
        Generate a key for a WiFi AP in AOS's API JSON response.

        Args:
            ssid (str): The SSID for the AP.
            band (str): Representation for the AP band. Defaults to 'band2400'.

        Returns:
            str: Key for the WiFi AP list in the AOS JSON response.
        """
        return f'net.wifi.ssid.scan[{ssid}].{band}'

    @staticmethod
    def ap_security_mode(ssid):
        """
        Generate a key for WiFi AP's security mode in AOS's API JSON response.

        Args:
            ssid (str): The SSID for the AP.

        Returns:
            str: Key for the WiFi AP in the AOS JSON response.
        """
        return f'net.wifi.ssid.scan[{ssid}].security.mode'

    @staticmethod
    def ap_selected(ssid):
        """
        Generate a key for WiFi AP selection status in AOS's API JSON response.

        Args:
            ssid (str): The SSID for the AP.

        Returns:
            str: Key for the WiFi AP in the AOS JSON response.
        """
        return f'net.wifi.ssid.scan[{ssid}].selected'