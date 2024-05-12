#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gnss.py

GNSS Data Class.

Class to model the state of a GNSS receiver.

"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"


from datetime import datetime


class GNSS:
    """
    GNSS Data class.
    Representative state for a GNSS receiver.

    TODO: 
        - Sanity Checks when converting to TAIP A
        - Calculate Age of Data Paramter in TAIP Message
    """
    DEFAULT_SOURCE = 6
    DEFAULT_AGE = 2
    DEFAULT_TAIP_ID = "0000"

    def __init__(self):
        """
        Constructor.
        """
        self.fixtime = datetime.now().replace(microsecond=0)  # Time of GPS Fix
        self.latitude = 0.0                     # latitude as decimal degrees
        self.lonitude = 0.0                     # longitude as decimal as degress
        self.altitude = 0.0                     # height above sea level as decimal meters (m)
        self.speed = 0.0                        # ground speed as decimale meters per second (m/s)
        self.heading = 0.0                      # track degrees
        self.fix = "NO FIX"                     # fix type as string e.g. "3D"
        self.satellites_in_view = 0             # satellites in view as integer
        self.satellites_in_position = 0         # satellites in position solution as integer
        self.p_dop = 0.0                        # dilution of precision DOP as decimal
        self.horizontal_dop = 0.0               # horizontal DOP as decimal
        self.vertical_dop = 0.0                 # vertical DOP as decimal
        self.horizontal_accuracy = 0.0          # horizontal accuracy as decimal meters (m)
        self.vertical_accuracy = 0.0            # vertical accuracy as decimal meters (m)
        self.seperation  = 0.0                  # separation from ellipsoid (height - hMSL) as decimal meters (m)
        self.differential_correction = 0        # DGPS correction status True/False
        self.differential_age = 0               # DGPS correction age as integer seconds
        self.differential_station = "N/A"       # DGPS station id
        self.relative_position_heading = 0.0    # rover relative position heading in decimal degress
        self.relative_position_length = 0.0     # rover relative position distance
        self.accuracy_heading = 0.0             # rover relative position heading accuracy
        self.accuracy_length = 0.0              # rover relative position distance accuracy
        self.taip_id = self.DEFAULT_TAIP_ID     # TAIP ID String to identify this GPS Unit
        self.relative_position_flags = []       # rover relative position flags
        self.gsv_data = []                      # list of satellite tuples (gnssId, svid, elev, azim, cno)
        self.version_data = {}                  # dict of hardware, firmware and software versions
        self.sysmon_data = {}                   # dict of system monitor data (cpu and memory load, etc.)
        self.spectrum_data = []                 # list of spectrum data (spec, spn, res, ctr, pga)
        self.comms_data = {}                    # dict of comms port utilisation (tx and rx loads)
        self.source = self.DEFAULT_SOURCE       # int representing TAIP source
        self.age = self.DEFAULT_AGE             # int representing TAIP data age


    def set_basic_values(self, fixtime=None, latitude=0.0, longitude=0.0, heading=0.0, speed=0.0, taip_id="0000", source=None, age=None):
        """
        Set basic GNSS Values

        Args:
        - fixtime (str): Time of GPS Fix
        - latitude (float): Latitude as decimal degrees
        - longitude (float): Longitude as decimal degrees
        - heading (float): Track degrees
        - speed (float): Ground speed as decimal meters per second (m/s)
        - taip_id (str): TAIP ID String to identify this GPS Unit
        """
        self.fixtime = datetime.fromtimestamp(fixtime/100) if fixtime else datetime.now().replace(microsecond=0)
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.speed = speed
        self.taip_id = taip_id
        self.source = source if source else self.DEFAULT_SOURCE
        self.age = age if age else self.DEFAULT_AGE

    def gps_time_of_day(self):
        """
        Calculate the GPS Time of Day for a given Unix timestamp.

        Args:
            unix_timestamp (int): Unix timestamp representing a specific moment in time.

        Returns:
            int: GPS Time of Day - Number of seconds since the previous midnight.
        """
        timestamp = self.fixtime
        previous_midnight = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_since_previous_midnight = (timestamp - previous_midnight).total_seconds()
        return int(seconds_since_previous_midnight)


    def taip_pv_message(self):
        """
        Generate a TAIP PV message from the current GNSS Data Set.

        >RPV15714+3739438-1220384601512612;ID=1234;*7F<
        >AAAAABBBCCCCCDDDDEEEEEFFFGGGHI<
        
        ID          | Meaning                       | # of Chars    | Units      
        ============|===============================|===============|==========
        >           | Start of Message Delimiter    | 1             |
        R           | Response Qualifier            | 1             |
        PV          | PV message Identifier         | 2             |
        15714       | GPS Time of Day               | 5             | Sec
        +3739438    | Latitude                      | 8             | Deg
        -12203846   | Longitude                     | 9             | Deg
        015         | Speed                         | 3             | MPH
        126         | Heading                       | 3             | Deg
        1           | Source of data                | 1             | See Source of Data Below
        2           | Age of Data                   | 1             | See Age of Data Below
        ;ID=1234    | Vehicle ID                    | 7             |
        ;*7F        | Checksum                      | 3             |
        <           | End of Message Delimiter      |               |

        Source of Data
        Value   | Meaning
        ========|===============
        0       | 2D GPS
        1       | 3D GPS
        3       | 2D DGPS
        4       | 3d DGPS
        5       | ------
        6       | DR
        7       | ------
        8       | Degraded DR
        9       | Unknown

        Age of Data Indicator
        Value   | Meaning
        ========|==================
        2       | Fresh (< 10 sec)
        1       | Old (> 10 sec)
        0       | Not available (Invalid Data)

        Returns:
            str: TAIP PV message.
        """

        gps_tod = self.gps_time_of_day()    # GPS Time of Day

        # The latitude formated as ABBBCCCCC where:
        #    - A (+ or -): + for West Longitudes and - for East Longitudes
        #    - BBB (int): whole number part of the latitude, left zero padded
        #    - CCCCC (int): decimla part of the latitude, right zero padded 
        sign = '+' if self.latitude >= 0 else '-'
        lat = f'{sign}{abs(self.latitude)*100000:0>7.0f}'

        # The latitude formated as ABBBCCCCC where:
        #   - A (+ or -): + for West Longitudes and - for East Longitudes
        #   - BBB (int): whole number part of the latitude, left zero padded
        #   - CCCCC (int): decimla part of the latitude, right zero padded 
        sign = '+' if self.longitude >= 0 else '-'
        longi = f'{sign}{abs(self.longitude)*100000:0>8.0f}'

        # Convert meter per second (m/s) to miles per hour (mph)
        speed = f'{self.speed * 2.2369362920544:0>3.0f}'

        # Formate heading by dropping decimale degrees and left padding three spaces
        heading = f'{self.heading:0>3.0f}'

        message = f">RPV{gps_tod}{lat}{longi}{speed}{heading}{self.source}{self.age};ID={self.taip_id};*"
        return f"{message}{self.hex_xor_checksum(message)}<"


    def hex_xor_checksum(self, string, encoding="utf-8"):
        """
        Generate a checksum by XORing all the characters in the provided string.

        Args:
            string (str): The input string to generate the checksum from.
            encoding (str, optional): The encoding to use for converting the string to bytes. Default is UTF-8.

        Returns:
            str: The hexadecimal representation of the XOR checksum value.
        """
        # Convert the string to bytes using the specified encoding
        string_bytes = bytes(string, encoding=encoding)

        # Initialize the checksum to 0x0
        checksum = 0x0

        # XOR each byte of the string to compute the checksum
        for byte in string_bytes:
            checksum ^= byte

        # Convert the checksum to hexadecimal representation and return
        return f'{checksum:x}'
