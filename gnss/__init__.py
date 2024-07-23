#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNSS Data Class Module.

This module provides tools for handling GNSS data, including a class for representing the state of a GNSS receiver and methods for generating various GNSS data messages.

Example Usage:
    if __name__ == "__main__":
        gnss = GNSS()
        gnss.set_basic_values(latitude=37.7749, longitude=-122.4194)
        print(gnss.fixtime)
        nmea_messages = gnss.generate_nmea_messages()
        for msg_type, msg in nmea_messages.items():
            print(f"{msg_type}: {msg}")

        msg = gnss.taip_pv_message()
        print(f'TAIP PV: {msg}')
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

from gnss.gnss import GNSS
from gnss.gnsshelpers import GNSSSpeed, GNSSTime, GNSSTools, NMEA, TAIP

# Example usage
if __name__ == "__main__":
    gnss = GNSS()
    gnss.set_basic_values(latitude=37.7749, longitude=-122.4194)
    print(gnss.fixtime)
    nmea_messages = gnss.generate_nmea_messages()
    for msg_type, msg in nmea_messages.items():
        print(f"{msg_type}: {msg}")

    msg = gnss.taip_pv_message()
    print(f'TAIP PV: {msg}')