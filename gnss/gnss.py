#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNSS Data Class Module.

This module defines a class for modeling GNSS data, including methods for setting values,
generating messages in various formats, and performing conversions and checks related to GNSS data.

Classes:
    GNSS: Represents a GNSS receiver's state and provides methods for data manipulation and message generation.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

from datetime import datetime
from enum import Enum
import json
import requests
from gnss.gnsshelpers import GNSSMeasure, GNSSTime, GNSSTools, NMEA, TAIP

class GNSS:
    """
    GNSS Data class.
    Represents the state of a GNSS receiver.

    Attributes:
        DEFAULT_TAIP_ID (str): Default TAIP ID.
    """
    DEFAULT_TAIP_ID = "0000"

    def __init__(self):
        """
        Initialize GNSS attributes with default values.
        """
        self.fixtime = datetime.utcnow().replace(microsecond=0)
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.speed = 0.0
        self.heading = 0.0
        self.fix = "NO FIX"
        self.satellites_in_view = 0
        self.satellites_in_position = 0
        self.p_dop = 0.0
        self.horizontal_dop = 0.0
        self.vertical_dop = 0.0
        self.horizontal_accuracy = 0.0
        self.vertical_accuracy = 0.0
        self.separation = 0.0
        self.differential_correction = 0
        self.differential_age = 0
        self.differential_station = "N/A"
        self.relative_position_heading = 0.0
        self.relative_position_length = 0.0
        self.accuracy_heading = 0.0
        self.accuracy_length = 0.0
        self.taip_id = self.DEFAULT_TAIP_ID
        self.relative_position_flags = []
        self.gsv_data = []
        self.version_data = {}
        self.sysmon_data = {}
        self.spectrum_data = []
        self.comms_data = {}
        self.source = TAIP.Sources.UNKNOWN
        self.age = TAIP.Age.NOT_AVAILABLE
        self.talker_identifier = NMEA.Talkers.GPS
        self.nmea_mode = NMEA.Modes.MODE_INVALID

    def set_basic_values(self, fixtime=None, latitude=None, longitude=None, heading=None,
                         speed_ms=None, speed_kmph=None, speed_knots=None, speed_mph=None, taip_id=None, nmea_mode=None, source=None, age=None):
        """
        Set basic GNSS values.

        Args:
            fixtime (int or None): Time of GPS fix as Unix timestamp (milliseconds), None for current time.
            latitude (float): Latitude in decimal degrees.
            longitude (float): Longitude in decimal degrees.
            heading (float): Track degrees.
            speed_ms (float): Ground speed in meters per second (m/s).
            speed_kmph (float): Ground speed in kilometers per hour (kmps).
            speed_knots (float): Ground speed in knots (knot).
            speed_mph (float): Ground speed in miles per hour (mph).
            taip_id (str): TAIP ID string to identify this GPS unit.
            nmea_mode (str): NMEA string to identify the GPS mode of operation.
            source (TAIP.Sources or None): Source of data.
            age (TAIP.Age or None): Age of data.
        """
        
        # Convert speed to M/s
        speed = None
        if speed_kmph is not None:
            speed = GNSSMeasure.kmph_to_ms(speed_kmph)
        elif speed_ms is not None:
            speed = speed_ms
        elif speed_knots is not None:
            speed = GNSSMeasure.knots_to_ms(speed_knots)
        elif speed_mph is not None:
            speed = GNSSMeasure.mph_to_ms(speed_mph)

        self.fixtime = datetime.fromtimestamp(fixtime / 1000) if fixtime else datetime.utcnow().replace(microsecond=0)
        self.latitude = latitude if latitude is not None else self.latitude
        self.longitude = longitude if longitude is not None else self.longitude
        self.heading = heading if heading is not None else self.heading
        self.speed = speed if speed is not None else self.speed
        self.taip_id = taip_id if taip_id is not None else self.taip_id
        self.source = source if source is not None else self.source
        self.nmea_mode = nmea_mode if nmea_mode is not None else self.nmea_mode
        self.age = age if age is not None else self.age

    def get_message(self, message_type: str = "TAIP_PV") -> str:
        """
        Get the message in the specified format.

        Args:
            message_type (str): The type of message to generate ("TAIP_PV", "NMEA", or "NMEA_RMC").

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

    def gps_time_of_day(self) -> int:
        """
        Generate the GPS Time of Day for the fixtime.

        Returns:
            int: GPS Time of Day in seconds since the previous midnight.
        """
        return GNSSTime.gps_time_of_day(self.fixtime)

    def taip_pv_message(self) -> str:
        """
        Generate a TAIP PV message from the current GNSS data.

        Returns:
            str: TAIP PV message.
        """
        gps_tod = self.gps_time_of_day()
        lat_sign = '+' if self.latitude >= 0 else '-'
        lat = f'{lat_sign}{abs(self.latitude) * 100000:07.0f}'
        long_sign = '+' if self.longitude >= 0 else '-'
        longi = f'{long_sign}{abs(self.longitude) * 100000:08.0f}'
        speed = f'{GNSSMeasure.ms_to_mph(self.speed):03.0f}'
        heading = f'{self.heading:03.0f}'
        message = f">RPV{gps_tod:05d}{lat}{longi}{speed}{heading}{self.source}{self.age};ID={self.taip_id};*"
        return f"{message}{GNSSTools.hex_xor_checksum(message)}<"

    def generate_nmea_messages(self) -> dict:
        """
        Generate all NMEA messages.

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

    def generate_nmea_gga(self) -> str:
        """
        Generate $GxGGA NMEA message.

        Returns:
            str: The $GxGGA message.
        """
        utc_time = self.fixtime.strftime('%H%M%S')
        lat = GNSSTools.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = GNSSTools.convert_to_nmea_lat_long(self.longitude, 'lon')
        message = (
            f"GPGGA,{utc_time},{lat},{lon},{self.fix},{self.satellites_in_position},"
            f"{self.p_dop},{self.altitude},M,{self.separation},M,{self.differential_age},"
            f"{self.differential_station}"
        )
        return f"${message}*{GNSSTools.hex_xor_checksum(message)}"

    def generate_nmea_gll(self) -> str:
        """
        Generate $GxGLL NMEA message.

        Returns:
            str: The $GxGLL message.
        """
        utc_time = self.fixtime.strftime('%H%M%S')
        lat = GNSSTools.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = GNSSTools.convert_to_nmea_lat_long(self.longitude, 'lon')
        message = f"GLL,{lat},{lon},{utc_time},{self.fix}"
        return self.pack_nmea_message(message)

    def generate_nmea_gsa(self) -> str:
        """
        Generate $GxGSA NMEA message.

        Returns:
            str: The $GxGSA message.
        """
        message = (
            f"GSA,A,{self.fix},{','.join(['' for _ in range(12)])},"
            f"{self.p_dop},{self.horizontal_dop},{self.vertical_dop}"
        )
        return self.pack_nmea_message(message)

    def generate_nmea_gsv(self) -> list:
        """
        Generate $GxGSV NMEA message.

        Returns:
            list: A list of $GxGSV messages.
        """
        num_messages = (len(self.gsv_data) + 3) // 4
        gsv_messages = []
        for i in range(num_messages):
            satellites = self.gsv_data[i*4:(i+1)*4]
            satellite_data = ",".join([f"{s[1]},{s[2]},{s[3]},{s[4]}" for s in satellites])
            message = f"GSV,{num_messages},{i+1},{self.satellites_in_view},{satellite_data}"
            gsv_messages.append(self.pack_nmea_message(message))
        return gsv_messages

    def generate_nmea_rmc(self) -> str:
        """
        Generate $GxRMC NMEA message.

        Returns:
            str: The $GxRMC message.
        """
        utc_time = self.fixtime.strftime('%H%M%S.%f')[:-4]
        lat = GNSSTools.convert_to_nmea_lat_long(self.latitude, 'lat')
        lon = GNSSTools.convert_to_nmea_lat_long(self.longitude, 'lon')
        date = self.fixtime.strftime('%d%m%y')
        magnetic_variation = 0.0
        magnetic_variation_direction = 'E'
        message = (
            f"RMC,{utc_time},{self.nmea_is_valid_data()},{lat},{lon},{GNSSMeasure.ms_to_knots(self.speed)},"
            f"{self.heading},{date},{magnetic_variation},{magnetic_variation_direction},{self.nmea_mode}"
        )
        return self.pack_nmea_message(message)

    def generate_nmea_vtg(self) -> str:
        """
        Generate $GxVTG NMEA message.

        Returns:
            str: The $GxVTG message.
        """
        message = (
            f"VTG,{self.heading:.3f},T,,M,{GNSSMeasure.ms_to_knots(self.speed)},N,{self.speed * 3.6},K"
        )
        return self.pack_nmea_message(message)

    def generate_nmea_zda(self) -> str:
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

    def nmea_is_valid_data(self) -> str:
        """
        Check if data is valid.

        Returns:
            str: 'A' if valid data, 'V' if invalid data.

        TODO:
            Implement the logic to check the GNSS data for validity.
        """
        return 'A'

    def pack_nmea_message(self, message: str) -> str:
        """
        Pack an NMEA message.

        Args:
            message (str): Message to pack in the form of CCCX where "ccc" identifies the message type and "x" is the data.

        Returns:
            str: Packed NMEA-0183 message.
        """
        message = f'{self.talker_identifier}{message}'
        return f"${message}*{GNSSTools.hex_xor_checksum(message)}\r\n"
