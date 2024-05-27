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

class AOSKeys:
    """
    Constants representing JSON keys for AOS's API response.

    Attributes:
        GNSS_FIXTIME (str): Key for GNSS fix time in the JSON response.
        GNSS_LATITUDE (str): Key for GNSS latitude in the JSON response.
        GNSS_LONGITUDE (str): Key for GNSS longitude in the JSON response.
        GNSS_HEADING (str): Key for GNSS heading in the JSON response.
        GNSS_SPEED (str): Key for GNSS speed in the JSON response.
        GNSS_TAIP_ID (str): Key for GNSS TAIP ID in the JSON response.
        WIFI_BANDS (list): List of WiFi bands.
    """
    GNSS_FIXTIME = "location.gnss.fixtime"
    GNSS_LATITUDE = "location.gnss.latitude"
    GNSS_LONGITUDE = "location.gnss.longitude"
    GNSS_HEADING = "location.gnss.heading"
    GNSS_SPEED = "location.gnss.speed"
    GNSS_TAIP_ID = "location.gnss.taipid"
    WIFI_BANDS = ["band2400", "band5400"]

    @staticmethod
    def generate_wifi_key(ssid, band="band2400"):
        """
        Generate a key for a WiFi AP in AOS's API JSON response.

        Args:
            ssid (str): The SSID for the AP.
            band (str): Representation for the AP band. Defaults to 'band2400'.

        Returns:
            str: Key for the WiFi AP in the AOS JSON response.
        """
        return f'net.wifi.ssid.scan[{ssid}].{band}'
