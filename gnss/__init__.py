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

from datetime import datetime, timezone
import json
import requests

class GNSS:
    """
    GNSS Data class.
    Representative state for a GNSS receiver.

    TODO: 
        - Sanity Checks when converting to TAIP A
        - Calculate Age of Data Parameter in TAIP Message
    """
    DEFAULT_SOURCE = 6
    DEFAULT_AGE = 2
    DEFAULT_TAIP_ID = "0000"

    def __init__(self):
        """
        Constructor.
        """
        self.fixtime = datetime.utcnow().replace(microsecond=0)  # Time of GPS Fix
        self.latitude = 0.0                     # latitude as decimal degrees
        self.longitude = 0.0                    # longitude as decimal degrees
        self.altitude = 0.0                     # height above sea level as decimal meters (m)
        self.speed = 0.0                        # ground speed as decimal meters per second (m/s)
        self.heading = 0.0                      # track degrees
        self.fix = "NO FIX"                     # fix type as string e.g. "3D"
        self.satellites_in_view = 0             # satellites in view as integer
        self.satellites_in_position = 0         # satellites in position solution as integer
        self.p_dop = 0.0                        # dilution of precision DOP as decimal
        self.horizontal_dop = 0.0               # horizontal DOP as decimal
        self.vertical_dop = 0.0                 # vertical DOP as decimal
        self.horizontal_accuracy = 0.0          # horizontal accuracy as decimal meters (m)
        self.vertical_accuracy = 0.0            # vertical accuracy as decimal meters (m)
        self.separation = 0.0                   # separation from ellipsoid (height - hMSL) as decimal meters (m)
        self.differential_correction = 0        # DGPS correction status True/False
        self.differential_age = 0               # DGPS correction age as integer seconds
        self.differential_station = "N/A"       # DGPS station id
        self.relative_position_heading = 0.0    # rover relative position heading in decimal degrees
        self.relative_position_length = 0.0     # rover relative position distance
        self.accuracy_heading = 0.0             # rover relative position heading accuracy
        self.accuracy_length = 0.0              # rover relative position distance accuracy
        self.taip_id = self.DEFAULT_TAIP_ID     # TAIP ID String to identify this GPS Unit
        self.relative_position_flags = []       # rover relative position flags
        self.gsv_data = []                      # list of satellite tuples (gnssId, svid, elev, azim, cno)
        self.version_data = {}                  # dict of hardware, firmware and software versions
        self.sysmon_data = {}                   # dict of system monitor data (cpu and memory load, etc.)
        self.spectrum_data = []                 # list of spectrum data (spec, spn, res, ctr, pga)
        self.comms_data = {}                    # dict of comms port utilization (tx and rx loads)
        self.source = self.DEFAULT_SOURCE       # int representing TAIP source
        self.age = self.DEFAULT_AGE             # int representing TAIP data age
        self.talker_identifier='GP'             # Talker ID for NMEA sentences

    def set_basic_values(self, fixtime=None, latitude=0.0, longitude=0.0, heading=0.0, speed=0.0, taip_id="0000", source=None, age=None):
        """
        Set basic GNSS Values

        Args:
            fixtime (int or None): Time of GPS Fix as Unix timestamp (milliseconds), None for current time.
            latitude (float): Latitude as decimal degrees.
            longitude (float): Longitude as decimal degrees.
            heading (float): Track degrees.
            speed (float): Ground speed as decimal meters per second (m/s).
            taip_id (str): TAIP ID String to identify this GPS Unit.
            source (int or None): Source of data.
            age (int or None): Age of data.
        """
        self.fixtime = datetime.fromtimestamp(fixtime / 1000) if fixtime else datetime.utcnow().replace(microsecond=0)
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.speed = speed
        self.taip_id = taip_id
        self.source = source if source else self.DEFAULT_SOURCE
        self.age = age if age else self.DEFAULT_AGE

    def gps_time_of_day(self):
        """
        Calculate the GPS Time of Day for the instance's fix time.

        Returns:
            int: GPS Time of Day - Number of seconds since the previous midnight.
        """
        timestamp = self.fixtime
        previous_midnight = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_since_previous_midnight = (timestamp - previous_midnight).total_seconds()
        return int(seconds_since_previous_midnight)

    def get_message(self, message_type="TAIP_PV"):
        """
        Get the message in the specified format.

        Args:
            message_type (str): The type of message to generate ("TAIP_PV" or "NMEA").

        Returns:
            str: The generated message.

        Raises:
            ValueError: If an unknown message type is specified.
        """
        if message_type == "TAIP_PV":
            return self.taip_pv_message()
        elif message_type == "NMEA":
            return self.generate_nmea_messages()
        elif message_type == "NMEA_RMC":
            return self.generate_nmea_rmc()
        else:
            raise ValueError(f'Unknown message type: {message_type}')

    def taip_pv_message(self):
        """
        Generate a TAIP PV message from the current GNSS Data Set.

        Returns:
            str: TAIP PV message.
        """
        gps_tod = self.gps_time_of_day()  # GPS Time of Day

        # Format latitude and longitude
        lat_sign = '+' if self.latitude >= 0 else '-'
        lat = f'{lat_sign}{abs(self.latitude) * 100000:07.0f}'

        long_sign = '+' if self.longitude >= 0 else '-'
        longi = f'{long_sign}{abs(self.longitude) * 100000:08.0f}'

        # Convert speed from meters per second to miles per hour
        speed = f'{self.speed * 2.2369362920544:03.0f}'

        # Format heading
        heading = f'{self.heading:03.0f}'

        # Generate the message
        message = f">RPV{gps_tod}{lat}{longi}{speed}{heading}{self.source}{self.age};ID={self.taip_id};*"
        return f"{message}{self.hex_xor_checksum(message)}<"

    def hex_xor_checksum(self, string, encoding="utf-8"):
        """
        Generate a checksum by XORing all the characters in the provided string.

        Args:
            string (str): The input string to generate the checksum from.
            encoding (str, optional): The encoding to use for converting the string to bytes. Default is UTF-8.

        Returns:
            str: The 2-bit hexadecimal representation of the XOR checksum value.
        """
        # Convert the string to bytes using the specified encoding
        string_bytes = bytes(string, encoding=encoding)

        # Initialize the checksum to 0x0
        checksum = 0x0

        # XOR each byte of the string to compute the checksum
        for byte in string_bytes:
            checksum ^= byte

        # Convert the checksum to hexadecimal representation and return
        return f'{checksum:02X}'

    def generate_nmea_messages(self):
        """
        Generate all NMEA messages ($GxGGA, $GxGLL, $GxGSA, $GxGSV, $GxRMC, $GxVTG, $GxZDA).

        Returns:
            dict: A dictionary of all generated NMEA messages.
        """
        return {
            f"{self.talker_identifier}GGA": self.generate_nmea_gga(),
            f"{self.talker_identifier}GLL": self.generate_nmea_gll(),
            f"{self.talker_identifier}GSA": self.generate_nmea_gsa(),
            f"{self.talker_identifier}GSV": self.generate_nmea_gsv(),
            f"{self.talker_identifier}RMC": self.generate_nmea_rmc(),
            f"{self.talker_identifier}VTG": self.generate_nmea_vtg(),
            f"{self.talker_identifier}ZDA": self.generate_nmea_zda()
        }

    def generate_nmea_gga(self):
        """
        Generate $GxGGA NMEA message.

        Returns:
            str: The $GxGGA message.
        """
        utc_time = self.fixtime.strftime('%H%M%S')
        lat = self.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = self.convert_to_nmea_lat_long(self.longitude, 'lon')
        message = f"GPGGA,{utc_time},{lat},{lon},{self.fix},{self.satellites_in_position},{self.p_dop},{self.altitude},M,{self.separation},M,{self.differential_age},{self.differential_station}"
        return f"${message}*{self.hex_xor_checksum(message)}"

    def generate_nmea_gll(self):
        """
        Generate $GxGLL NMEA message.

        Returns:
            str: The $GxGLL message.
        """
        utc_time = self.fixtime.strftime('%H%M%S')
        lat = self.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = self.convert_to_nmea_lat_long(self.longitude, 'lon')
        message = f"GPGLL,{lat},{lon},{utc_time},{self.fix}"
        return f"${message}*{self.hex_xor_checksum(message)}"

    def generate_nmea_gsa(self):
        """
        Generate $GxGSA NMEA message.

        Returns:
            str: The $GxGSA message.
        """
        message = f"GPGSA,A,{self.fix},{','.join(['' for _ in range(12)])},{self.p_dop},{self.horizontal_dop},{self.vertical_dop}"
        return f"${message}*{self.hex_xor_checksum(message)}"

    def generate_nmea_gsv(self):
        """
        Generate $GxGSV NMEA message.

        Returns:
            str: The $GxGSV message.
        """
        num_messages = (len(self.gsv_data) + 3) // 4
        gsv_messages = []
        for i in range(num_messages):
            satellites = self.gsv_data[i*4:(i+1)*4]
            satellite_data = ",".join([f"{s[1]},{s[2]},{s[3]},{s[4]}" for s in satellites])
            message = f"GPGSV,{num_messages},{i+1},{self.satellites_in_view},{satellite_data}"
            gsv_messages.append(f"${message}*{self.hex_xor_checksum(message)}")
        return gsv_messages

    def generate_nmea_rmc(self):
        """
        Generate $GxRMC NMEA message.

        Returns:
            str: The $GxRMC message.
        """
        utc_time = self.fixtime.strftime('%H%M%S')
        lat = self.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = self.convert_to_nmea_lat_long(self.longitude, 'lon')
        date = self.fixtime.strftime('%d%m%y')
        message = f"GPRMC,{utc_time},{self.fix},{lat},{lon},{self.speed * 1.94384},{self.heading},{date}"
        return f"${message}*{self.hex_xor_checksum(message)}"

    def generate_nmea_vtg(self):
        """
        Generate $GxVTG NMEA message.

        Returns:
            str: The $GxVTG message.
        """
        message = f"GPVTG,{self.heading},T,,M,{self.speed * 1.94384},N,{self.speed * 3.6},K"
        return f"${message}*{self.hex_xor_checksum(message)}"

    def generate_nmea_zda(self):
        """
        Generate $GxZDA NMEA message.

        Returns:
            str: The $GxZDA message.
        """
        utc_time = self.fixtime.strftime('%H%M%S.%f')[:-4]
        day = self.fixtime.strftime('%d')
        month = self.fixtime.strftime('%m')
        year = self.fixtime.strftime('%Y')
        message = f"ZDA,{utc_time},{day},{month},{year},,"
        return self.pack_nmea_message(message)

    def pack_nmea_message(self, message):
        """
        Packs a NMEA Message

        Args:
            message (str): Message to pack in the form of CCCX where "ccc" identifies the message type and "x" is the data

        Returns:
            str: Packed NMEA-0183 message
        """
        message = f'{self.talker_identifier}{message}'
        return f"${message}*{self.hex_xor_checksum(message)}\r\n"

    def convert_to_nmea_lat_long(self, value, type):
        """
        Convert decimal latitude/longitude to NMEA format.

        Args:
            value (float): The latitude or longitude in decimal degrees.
            type (str): 'lat' for latitude or 'lon' for longitude.

        Returns:
            str: The NMEA formatted latitude or longitude.
        """
        degrees = int(value)
        minutes = (abs(value) - abs(degrees)) * 60
        if type == 'lat':
            direction = 'N' if value >= 0 else 'S'
            return f"{abs(degrees):02d}{minutes:07.4f},{direction}"
        elif type == 'lon':
            direction = 'E' if value >= 0 else 'W'
            return f"{abs(degrees):03d}{minutes:07.4f},{direction}"
        else:
            raise ValueError("Type must be 'lat' or 'lon'.")

# Example usage
if __name__ == "__main__":
    gnss = GNSS()
    gnss.set_basic_values(latitude=37.7749, longitude=-122.4194)
    print(gnss.fixtime)
    nmea_messages = gnss.generate_nmea_messages()
    for msg_type, msg in nmea_messages.items():
        print(f"{msg_type}: {msg}")
