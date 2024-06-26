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

from .aosquerykeys import AOSQueryKeys
from .aosgnsskeys import AOSGNSSKeys
from .aoswifikeys import AOSWifiKeys

class AOSKeys:
    """
    Constants representing JSON keys for AOS's API response.

    Attributes:
        QUERY (obj): Keys for Airlink OS API Queries
        GNSS (obj): Keys for GNSS information in the JSON response.
        WIFI (obj): Keys to access Wifi information in List of WiFi bands.
    """

    QUERY = AOSQueryKeys
    GNSS = AOSGNSSKeys
    WIFI = AOSWifiKeys

