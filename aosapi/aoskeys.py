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
        GNSS_ALTITUDE (str): Key for GNSS altitude in the JSON response.
        GNSS_ANTENNA_CONNECTTHRESHOLD (str): Key for GNSS antenna connect threshold in the JSON response.
        GNSS_ANTENNA_DETECTION (str): Key for GNSS antenna detection in the JSON response.
        GNSS_ANTENNA_DISCONNECTTHRESHOLD (str): Key for GNSS antenna disconnect threshold in the JSON response.
        GNSS_ANTENNA_SHORTED (str): Key for GNSS antenna shorted state in the JSON response.
        GNSS_ANTENNA_STATE (str): Key for GNSS antenna state in the JSON response.
        GNSS_ANTENNABIAS (str): Key for GNSS antenna bias in the JSON response.
        GNSS_CONFIGURED (str): Key for GNSS configured state in the JSON response.
        GNSS_CONSTELLATION (str): Key for GNSS constellation in the JSON response.
        GNSS_CUSTOMSTRING (str): Key for GNSS custom string in the JSON response.
        GNSS_DEBUG_DRSENMSG_ENABLED (str): Key for GNSS debug DRSEN message enabled in the JSON response.
        GNSS_DEBUG_ENABLED (str): Key for GNSS debug enabled state in the JSON response.
        GNSS_DEBUG_FASTHIGHSENTENCES (str): Key for GNSS debug fast high sentences in the JSON response.
        GNSS_DEBUG_FASTLOWSENTENCES (str): Key for GNSS debug fast low sentences in the JSON response.
        GNSS_DEBUG_FASTRATE (str): Key for GNSS debug fast rate in the JSON response.
        GNSS_DEBUG_FILTER (str): Key for GNSS debug filter in the JSON response.
        GNSS_DEBUG_HIGHSENTENCES (str): Key for GNSS debug high sentences in the JSON response.
        GNSS_DEBUG_LOWSENTENCES (str): Key for GNSS debug low sentences in the JSON response.
        GNSS_DEBUG_NMEASENTENCES (str): Key for GNSS debug NMEA sentences in the JSON response.
        GNSS_DEVICEIDTYPE (str): Key for GNSS device ID type in the JSON response.
        GNSS_DRSTATUS (str): Key for GNSS DR status in the JSON response.
        GNSS_ENABLED (str): Key for GNSS enabled state in the JSON response.
        GNSS_FIXTIME (str): Key for GNSS fix time in the JSON response.
        GNSS_FWUPDATE_CURRENTFIRMWARE (str): Key for GNSS firmware update current firmware in the JSON response.
        GNSS_FWUPDATE_DRCAPABLE (str): Key for GNSS firmware update DR capable in the JSON response.
        GNSS_FWUPDATE_FLASHEDFIRMWARE (str): Key for GNSS firmware update flashed firmware in the JSON response.
        GNSS_FWUPDATE_MODE (str): Key for GNSS firmware update mode in the JSON response.
        GNSS_FWUPDATE_SELECTEDFIRMWARE (str): Key for GNSS firmware update selected firmware in the JSON response.
        GNSS_HDOP (str): Key for GNSS HDOP in the JSON response.
        GNSS_HEADING (str): Key for GNSS heading in the JSON response.
        GNSS_LATITUDE (str): Key for GNSS latitude in the JSON response.
        GNSS_LONGITUDE (str): Key for GNSS longitude in the JSON response.
        GNSS_LUDICROUSSPEEDTHRESHOLD (str): Key for GNSS ludicrous speed threshold in the JSON response.
        GNSS_QI (str): Key for GNSS QI in the JSON response.
        GNSS_SATCOUNT (str): Key for GNSS satellite count in the JSON response.
        GNSS_SPEED (str): Key for GNSS speed in the JSON response.
        GNSS_STATE (str): Key for GNSS state in the JSON response.
        GNSS_STATIONARYSPEEDTHRESHOLD (str): Key for GNSS stationary speed threshold in the JSON response.
        GNSS_TAIPID (str): Key for GNSS TAIP ID in the JSON response.
        GNSS_TTYPORT (str): Key for GNSS TTY port in the JSON response.
        GNSS_VB_ACCELQUALTIME (str): Key for GNSS VB acceleration quality time in the JSON response.
        GNSS_VB_ACCELTHRESHOLD (str): Key for GNSS VB acceleration threshold in the JSON response.
        GNSS_VB_BRAKEQUALTIME (str): Key for GNSS VB brake quality time in the JSON response.
        GNSS_VB_BRAKETHRESHOLD (str): Key for GNSS VB brake threshold in the JSON response.
        GNSS_VB_SIDEQUALTIME (str): Key for GNSS VB side quality time in the JSON response.
        GNSS_VB_SIDETHRESHOLD (str): Key for GNSS VB side threshold in the JSON response.
        GNSS_VB_STATE (str): Key for GNSS VB state in the JSON response.
        GNSS_VB_SUMQUALTIME (str): Key for GNSS VB sum quality time in the JSON response.
        GNSS_VB_SUMTHRESHOLD (str): Key for GNSS VB sum threshold in the JSON response.
        WIFI_BANDS (list): List of WiFi bands.
    """
    GNSS_ALTITUDE = "location.gnss.altitude"
    GNSS_ANTENNA_CONNECTTHRESHOLD = "location.gnss.antenna.connectthreshold"
    GNSS_ANTENNA_DETECTION = "location.gnss.antenna.detection"
    GNSS_ANTENNA_DISCONNECTTHRESHOLD = "location.gnss.antenna.disconnectthreshold"
    GNSS_ANTENNA_SHORTED = "location.gnss.antenna.shorted"
    GNSS_ANTENNA_STATE = "location.gnss.antenna.state"
    GNSS_ANTENNABIAS = "location.gnss.antennabias"
    GNSS_CONFIGURED = "location.gnss.configured"
    GNSS_CONSTELLATION = "location.gnss.constellation"
    GNSS_CUSTOMSTRING = "location.gnss.customstring"
    GNSS_DEBUG_DRSENMSG_ENABLED = "location.gnss.debug.drsenmsg.enabled"
    GNSS_DEBUG_ENABLED = "location.gnss.debug.enabled"
    GNSS_DEBUG_FASTHIGHSENTENCES = "location.gnss.debug.fasthighsentences"
    GNSS_DEBUG_FASTLOWSENTENCES = "location.gnss.debug.fastlowsentences"
    GNSS_DEBUG_FASTRATE = "location.gnss.debug.fastrate"
    GNSS_DEBUG_FILTER = "location.gnss.debug.filter"
    GNSS_DEBUG_HIGHSENTENCES = "location.gnss.debug.highsentences"
    GNSS_DEBUG_LOWSENTENCES = "location.gnss.debug.lowsentences"
    GNSS_DEBUG_NMEASENTENCES = "location.gnss.debug.nmeasentences"
    GNSS_DEVICEIDTYPE = "location.gnss.deviceidtype"
    GNSS_DRSTATUS = "location.gnss.drstatus"
    GNSS_ENABLED = "location.gnss.enabled"
    GNSS_FIXTIME = "location.gnss.fixtime"
    GNSS_FWUPDATE_CURRENTFIRMWARE = "location.gnss.fwupdate.currentfirmware"
    GNSS_FWUPDATE_DRCAPABLE = "location.gnss.fwupdate.drcapable"
    GNSS_FWUPDATE_FLASHEDFIRMWARE = "location.gnss.fwupdate.flashedfirmware"
    GNSS_FWUPDATE_MODE = "location.gnss.fwupdate.mode"
    GNSS_FWUPDATE_SELECTEDFIRMWARE = "location.gnss.fwupdate.selectedfirmware"
    GNSS_HDOP = "location.gnss.hdop"
    GNSS_HEADING = "location.gnss.heading"
    GNSS_LATITUDE = "location.gnss.latitude"
    GNSS_LONGITUDE = "location.gnss.longitude"
    GNSS_LUDICROUSSPEEDTHRESHOLD = "location.gnss.ludicrousspeedthreshold"
    GNSS_QI = "location.gnss.qi"
    GNSS_SATCOUNT = "location.gnss.satcount"
    GNSS_SPEED = "location.gnss.speed"
    GNSS_STATE = "location.gnss.state"
    GNSS_STATIONARYSPEEDTHRESHOLD = "location.gnss.stationaryspeedthreshold"
    GNSS_TAIPID = "location.gnss.taipid"
    GNSS_TTYPORT = "location.gnss.ttyport"
    GNSS_VB_ACCELQUALTIME = "location.gnss.vb.accelqualtime"
    GNSS_VB_ACCELTHRESHOLD = "location.gnss.vb.accelthreshold"
    GNSS_VB_BRAKEQUALTIME = "location.gnss.vb.brakequaltime"
    GNSS_VB_BRAKETHRESHOLD = "location.gnss.vb.brakethreshold"
    GNSS_VB_SIDEQUALTIME = "location.gnss.vb.sidequaltime"
    GNSS_VB_SIDETHRESHOLD = "location.gnss.vb.sidethreshold"
    GNSS_VB_STATE = "location.gnss.vb.state"
    GNSS_VB_SUMQUALTIME = "location.gnss.vb.sumqualtime"
    GNSS_VB_SUMTHRESHOLD = "location.gnss.vb.sumthreshold"
    GNSS_TAIP_ID = self.GNSS_TAIPID
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
