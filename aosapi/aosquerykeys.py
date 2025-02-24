#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aosgnsskeys.py

Keys GNSS Information in theJSON Response from the Airlink OS API.

This module defines the AOSKeys class that provides constants representing JSON keys for AOS's API response
and a method to generate WiFi keys dynamically.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

class AOSQueryKeys:
    """
    Constants representing JSON keys for AOS's API response.

    Attributes:
        GNSS (str): Query keys to request GNSS information from Airlink OS API
        WIFI (str): Query keys to request Wifi information from Airlink OS API

    """
    GNSS = "location.gnss"
    WIFI = "net.wifi.ssid"
    INTERFACE = "net.interface"
    IGNITION_STATUS = "vehicle.can.ignitionstatus"