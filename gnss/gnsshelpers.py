#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides various classes for working with GNSS (Global Navigation Satellite System) data and protocols.

Classes:
    TAIP: Contains constants for the TAIP (Trimble ASCII Interface Protocol) data.
    NMEA: Contains constants for the NMEA (National Marine Electronics Association) 0183 data.
    GNSSTime: Provides methods for converting between UTC and GPS time and calculating GPS time of day.
    GNSSMeasure: Provides utility methods for converting GNSS measurement units.
    GNSSTools: Provides tools for working with GNSS data, including conversion of coordinates and checksum generation.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

from datetime import datetime, timedelta

class TAIP:
    """
    Represents different constants for the TAIP (Trimble ASCII Interface Protocol) Data.

    This class contains nested classes that define various constants used in the TAIP protocol, including
    sources and age of data.
    """

    class Sources:
        """
        Represents different sources of TAIP (Trimble ASCII Interface Protocol) data.

        Attributes:
            GPS_2D (int): Source identifier for 2D GPS data (0).
            GPS_3D (int): Source identifier for 3D GPS data (1).
            DGPS_2D (int): Source identifier for 2D Differential GPS data (2).
            DGPS_3D (int): Source identifier for 3D Differential GPS data (3).
            DR (int): Source identifier for Dead Reckoning data (6).
            DEGRADED_DR (int): Source identifier for Degraded Dead Reckoning data (8).
            UNKNOWN (int): Source identifier for unknown data source (9).
        """
        GPS_2D = 0
        GPS_3D = 1
        DGPS_2D = 2
        DGPS_3D = 3
        DR = 6  # Dead Reckoning
        DEGRADED_DR = 8
        UNKNOWN = 9

    class Age:
        """
        Represents different ages of TAIP (Trimble ASCII Interface Protocol) data.

        Attributes:
            FRESH (int): Age identifier for data fresher than 10 seconds (2).
            OLD (int): Age identifier for data older than 10 seconds (1).
            NOT_AVAILABLE (int): Age identifier for data not available (0).
        """
        FRESH = 2  # <10 Seconds
        OLD = 1    # >10 Seconds
        NOT_AVAILABLE = 0


class NMEA:
    """
    Represents different constants for NMEA (National Marine Electronics Association) 0183 Data.

    This class contains nested classes that define various constants used in the NMEA protocol, including
    position status, modes of operation, and talker identifiers.
    """

    class PositionStatus:
        """
        Represents the status of the position data in NMEA (National Marine Electronics Association) protocol.

        Attributes:
            DATA_VALID (str): Status indicating the data is valid ('A').
            DATA_INVALID (str): Status indicating the data is invalid ('V').
        """
        DATA_VALID = 'A'
        DATA_INVALID = 'V'

    class Modes:
        """
        Represents the mode of operation in NMEA protocol.

        Attributes:
            AUTONOMOUS (str): Mode indicating autonomous operation ('A').
            DIFFERENTIAL (str): Mode indicating differential operation ('D').
            ESTIMATED (str): Mode indicating estimated (dead reckoning) operation ('E').
            MANUAL (str): Mode indicating manual operation ('M').
            MODE_INVALID (str): Mode indicating invalid operation ('N').
        """
        AUTONOMOUS = 'A'
        DIFFERENTIAL = 'D'
        ESTIMATED = 'E'  # Dead Reckoning
        MANUAL = 'M'
        MODE_INVALID = 'N'

    class Talkers:
        """
        Represents different talkers in NMEA protocol.

        This class provides constants representing the talker identifiers used in NMEA sentences for different 
        satellite navigation systems. These identifiers are used to specify the source of the NMEA data.

        Attributes:
            GALILEO_POSITIONING_SYSTEM (str): Identifier for Galileo Positioning System ("GA").
            BEIDOU_SYSTEM (str): Identifier for BeiDou Navigation Satellite System ("GB").
            BEIDOU_SYSTEM_OLD (str): Older identifier for BeiDou Navigation Satellite System ("GA").
            NAV_IC (str): Identifier for Indian Regional Navigation Satellite System (IRNSS) ("GI").
            GLONASS (str): Identifier for Global Navigation Satellite System (GLONASS) ("GL").
            GNSS (str): Generic identifier for Global Navigation Satellite System (GNSS) ("GN").
            GPS (str): Identifier for Global Positioning System (GPS) ("GP").
            QZSS (str): Identifier for Quasi-Zenith Satellite System (QZSS) ("GQ").
            PROPRIETARY (str): Identifier for proprietary sentences ("P").
        """
        GALILEO_POSITIONING_SYSTEM = "GA"
        BEIDOU_SYSTEM = "GB"
        BEIDOU_SYSTEM_OLD = "GA"
        NAV_IC = "GI"
        GLONASS = "GL"
        GNSS = "GN"
        GPS = "GP"
        QZSS = "GQ"
        PROPRIETARY = "P"


class GNSSTime:
    """
    A class to handle time conversions between UTC and GPS time, and to calculate GPS time of day.

    This class includes static methods for:
        - Converting UTC time to GPS time
        - Converting GPS time to UTC time
        - Calculating the GPS time of day from a given time

    Attributes:
        LEAP_SECONDS (list): A list of datetime objects representing the dates and times of leap seconds.
        GPS_EPOCH (datetime): The epoch for GPS time (January 6, 1980).
        UNIX_EPOCH (datetime): The epoch for UNIX time (January 1, 1970).
    """

    LEAP_SECONDS = [
        datetime(1981, 6, 30, 23, 59, 59),
        datetime(1982, 6, 30, 23, 59, 59),
        datetime(1983, 6, 30, 23, 59, 59),
        datetime(1985, 6, 30, 23, 59, 59),
        datetime(1987, 12, 31, 23, 59, 59),
        datetime(1989, 12, 31, 23, 59, 59),
        datetime(1990, 12, 31, 23, 59, 59),
        datetime(1992, 6, 30, 23, 59, 59),
        datetime(1993, 6, 30, 23, 59, 59),
        datetime(1994, 6, 30, 23, 59, 59),
        datetime(1995, 12, 31, 23, 59, 59),
        datetime(1997, 6, 30, 23, 59, 59),
        datetime(1998, 12, 31, 23, 59, 59),
        datetime(2005, 12, 31, 23, 59, 59),
        datetime(2008, 12, 31, 23, 59, 59),
        datetime(2012, 6, 30, 23, 59, 59),
        datetime(2015, 6, 30, 23, 59, 59),
        datetime(2016, 12, 31, 23, 59, 59)
    ]

    GPS_EPOCH = datetime(1980, 1, 6, 0, 0, 0)
    UNIX_EPOCH = datetime(1970, 1, 1, 0, 0, 0)

    @staticmethod
    def utc_to_gps(utc_time: datetime) -> datetime:
        """
        Convert UTC time to GPS time.

        Args:
            utc_time (datetime): The UTC time to be converted.

        Returns:
            datetime: The corresponding GPS time.

        Raises:
            ValueError: If utc_time is not a datetime instance.
        """
        if not isinstance(utc_time, datetime):
            raise ValueError("utc_time must be a datetime instance")

        leap_seconds = sum(1 for leap_second in GNSSTime.LEAP_SECONDS if utc_time > leap_second)

        gps_time = utc_time + timedelta(seconds=leap_seconds)

        gps_offset = (GNSSTime.GPS_EPOCH - GNSSTime.UNIX_EPOCH).total_seconds()

        gps_time = gps_time - timedelta(seconds=gps_offset)

        return gps_time

    @staticmethod
    def gps_to_utc(gps_time: datetime) -> datetime:
        """
        Convert GPS time to UTC time.

        Args:
            gps_time (datetime): The GPS time to be converted.

        Returns:
            datetime: The corresponding UTC time.

        Raises:
            ValueError: If gps_time is not a datetime instance.
        """
        if not isinstance(gps_time, datetime):
            raise ValueError("gps_time must be a datetime instance")

        gps_offset = (GNSSTime.GPS_EPOCH - GNSSTime.UNIX_EPOCH).total_seconds()

        utc_time = gps_time + timedelta(seconds=gps_offset)

        leap_seconds = sum(1 for leap_second in GNSSTime.LEAP_SECONDS if utc_time > leap_second)

        utc_time = utc_time - timedelta(seconds=leap_seconds)

        return utc_time

    @staticmethod
    def gps_time_of_day(time: datetime) -> int:
        """
        Calculate the GPS Time of Day for the given fix time.

        Args:
            time (datetime): The time of the GPS fix.

        Returns:
            int: GPS Time of Day - Number of seconds since the previous midnight, rounded to whole seconds.

        Raises:
            ValueError: If time is not a datetime instance.
        """
        if not isinstance(time, datetime):
            raise ValueError("time must be a datetime instance.")

        previous_midnight = time.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_since_previous_midnight = (time - previous_midnight).total_seconds()
        return int(seconds_since_previous_midnight)

class GNSSMeasure:
    """
    Provides utility methods for converting GNSS measurement units.

    This class includes static methods to convert speeds between:
        - Meters per second (m/s) and knots
        - Meters per second (m/s) and miles per hour (mph)

    Conversion factors:
        - 1 meter per second is approximately 1.94384 knots.
        - 1 meter per second is approximately 2.2369362920544 miles per hour.
    """

    _MS_TO_KNOTS = 1.94384  # Meters per second to knots conversion factor
    _MS_TO_MPH = 2.2369362920544  # Meters per second to miles per hour conversion factor

    @staticmethod
    def ms_to_knots(speed_ms: float) -> float:
        """
        Convert speed from meters per second to knots.

        Args:
            speed_ms (float): Speed in meters per second.

        Returns:
            float: Speed in knots.
        """
        return speed_ms * GNSSMeasure._MS_TO_KNOTS

    @staticmethod
    def knots_to_ms(speed_knots: float) -> float:
        """
        Convert speed from knots to meters per second.

        Args:
            speed_knots (float): Speed in knots.

        Returns:
            float: Speed in meters per second.
        """
        return speed_knots / GNSSMeasure._MS_TO_KNOTS

    @staticmethod
    def ms_to_mph(speed_ms: float) -> float:
        """
        Convert speed from meters per second to miles per hour.

        Args:
            speed_ms (float): Speed in meters per second.

        Returns:
            float: Speed in miles per hour.
        """
        return speed_ms * GNSSMeasure._MS_TO_MPH

    @staticmethod
    def mph_to_ms(speed_mph: float) -> float:
        """
        Convert speed from miles per hour to meters per second.

        Args:
            speed_mph (float): Speed in miles per hour.

        Returns:
            float: Speed in meters per second.
        """
        return speed_mph / GNSSMeasure._MS_TO_MPH

class GNSSTools:
    """
    A collection of tools for working with GNSS (Global Navigation Satellite System) data.

    This class provides static methods for converting decimal latitude and longitude values 
    to NMEA (National Marine Electronics Association) format and for generating checksums 
    using XOR operations.

    Methods:
        convert_to_nmea_lat_long(value, coord_type): Converts decimal latitude or longitude to NMEA format.
        hex_xor_checksum(string, encoding="utf-8"): Generates an XOR checksum from a string.
    """
    
    @staticmethod
    def convert_to_nmea_lat_long(value: float, coord_type: str) -> str:
        """
        Convert decimal latitude/longitude to NMEA format.

        Args:
            value (float): The latitude or longitude in decimal degrees.
            coord_type (str): 'lat' for latitude or 'lon' for longitude.

        Returns:
            str: The NMEA formatted latitude or longitude.

        Raises:
            ValueError: If coord_type is not 'lat' or 'lon', or if value is out of valid range.
        """
        if coord_type not in ('lat', 'lon'):
            raise ValueError("coord_type must be 'lat' or 'lon'.")
        if not isinstance(value, (float, int)):
            raise ValueError("value must be a float or an integer.")

        degrees = int(value)
        minutes = (abs(value) - abs(degrees)) * 60

        if coord_type == 'lat':
            if not (-90 <= value <= 90):
                raise ValueError("Latitude value must be between -90 and 90 degrees.")
            direction = 'N' if value >= 0 else 'S'
            return f"{abs(degrees):02d}{minutes:07.4f},{direction}"
        elif coord_type == 'lon':
            if not (-180 <= value <= 180):
                raise ValueError("Longitude value must be between -180 and 180 degrees.")
            direction = 'E' if value >= 0 else 'W'
            return f"{abs(degrees):03d}{minutes:07.4f},{direction}"

    @staticmethod
    def hex_xor_checksum(string: str, encoding: str = "utf-8") -> str:
        """
        Generate a checksum by XORing all the characters in the provided string.

        Args:
            string (str): The input string to generate the checksum from.
            encoding (str, optional): The encoding to use for converting the string to bytes. Default is UTF-8.

        Returns:
            str: The hexadecimal representation of the XOR checksum value.

        Raises:
            ValueError: If string is not a valid str.
        """
        if not isinstance(string, str):
            raise ValueError("string must be a valid str.")

        string_bytes = string.encode(encoding)
        checksum = 0x0
        for byte in string_bytes:
            checksum ^= byte
        return f'{checksum:02X}'
