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


class GNSSS:
    """
    GNSS Data class.
    Representative state for a GNSS receiver.

    TODO: 
        - Sanity Checks when converting to TAIP A
        - Calculate Age of Data Paramter in TAIP Message
    """

    def __init__(self):
        """
        Constructor.
        """
        self.fixtime = datetime.utc().time().replace(microsecond=0)  # Time of GPS Fix
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
        self.taip_id = "0000"                   # TAIP ID String to identify this GPS Unit
        self.relative_position_flags = []       # rover relative position flags
        self.gsv_data = []                      # list of satellite tuples (gnssId, svid, elev, azim, cno)
        self.version_data = {}                  # dict of hardware, firmware and software versions
        self.sysmon_data = {}                   # dict of system monitor data (cpu and memory load, etc.)
        self.spectrum_data = []                 # list of spectrum data (spec, spn, res, ctr, pga)
        self.comms_data = {}                    # dict of comms port utilisation (tx and rx loads)


    def set_basic_values(self, fixtime=None, latitude=0.0, longitude=0.0, heading=0.0, speed=0.0, taip_id="0000"):
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

        self.fixtime = fixtime if fixtime else datetime.utc().time().replace(microsecond=0)
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.speed = speed
        self.taip_id = taip_id

    def gps_time_of_day(self):
        """
        Calculate the GPS Time of Day for a given Unix timestamp.

        Args:
            unix_timestamp (int): Unix timestamp representing a specific moment in time.

        Returns:
            int: GPS Time of Day - Number of seconds since the previous midnight.
        """
    
        timestamp = datetime.fromtimestamp(self.fixtime)
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
            lat = f'{sign}{self.latitude:0>7.0f}'

            # The latitude formated as ABBBCCCCC where:
            #   - A (+ or -): + for West Longitudes and - for East Longitudes
            #   - BBB (int): whole number part of the latitude, left zero padded
            #   - CCCCC (int): decimla part of the latitude, right zero padded 
            sign = '+' if self.longitude >= 0 else '-'
            longi = f'{sign}{self.longitude:0>8.0f}'

            # Convert meter per second (m/s) to miles per hour (mph)
            speed = f'{self.speed * 2.2369362920544:0>3.0f}'

            heading = f'{self.heading:0>3.of}'
            source = '6'
            age_of_data = 2

            message = f">RPV{gps_tod}{lat}{longi}{spped}{jeading}{source}{age_of_data};ID={self.taip_id};*"
            return f"{message}{self.calculate_checksum(message)}<"
            message  


    def calculate_checksum(data):
        """
        Calculates a 2-bit checksum for the given data.

        Args:
            data: A byte string.

        Returns:
            A 2-bit checksum.
        """

        checksum = 0
        for byte in data:
            checksum ^= byte
        
        return checksum & 0x3
