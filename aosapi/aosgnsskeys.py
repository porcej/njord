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

class AOSGNSSKeys:
    """
    Constants representing JSON keys for AOS's API response.

    Attributes:
        CONFIGURED (str): Key for GNSS configured state in the JSON response.
        CONSTELLATION (str): Key for GNSS constellation in the JSON response.
        CUSTOMSTRING (str): Key for GNSS custom string in the JSON response.
        DEVICEIDTYPE (str): Key for GNSS device ID type in the JSON response.
        DRSTATUS (str): Key for GNSS DR status in the JSON response.
        ENABLED (str): Key for GNSS enabled state in the JSON response.
        FIXTIME (str): Key for GNSS fix time in the JSON response.
        HDOP (str): Key for GNSS HDOP in the JSON response.
        HEADING (str): Key for GNSS heading in the JSON response.
        LATITUDE (str): Key for GNSS latitude in the JSON response.
        LONGITUDE (str): Key for GNSS longitude in the JSON response.
        LUDICROUSSPEEDTHRESHOLD (str): Key for GNSS ludicrous speed threshold in the JSON response.
        QI (str): Key for GNSS QI in the JSON response.
        SATCOUNT (str): Key for GNSS satellite count in the JSON response.
        SPEED (str): Key for GNSS speed in the JSON response.
        STATE (str): Key for GNSS state in the JSON response.
        STATIONARYSPEEDTHRESHOLD (str): Key for GNSS stationary speed threshold in the JSON response.
        TAIPID (str): Key for GNSS TAIP ID in the JSON response.
        TTYPORT (str): Key for GNSS TTY port in the JSON response.
        ANTENNA (obj): Keys for GNSS Antenna informaation in the JSON response.
        DEBUG (obj): Key to facilitate debuging in the JSON response.
        FWUPDATE (obj): Keys related to firmware in the JSON response.
        VB (obj): Keys related to vehicle telemetry in the JSON response.

    """
    ALTITUDE = "location.gnss.altitude"
    CONFIGURED = "location.gnss.configured"
    CONSTELLATION = "location.gnss.constellation"
    CUSTOMSTRING = "location.gnss.customstring"
    DEVICEIDTYPE = "location.gnss.deviceidtype"
    DRSTATUS = "location.gnss.drstatus"
    ENABLED = "location.gnss.enabled"
    FIXTIME = "location.gnss.fixtime"
    HDOP = "location.gnss.hdop"
    HEADING = "location.gnss.heading"
    LATITUDE = "location.gnss.latitude"
    LONGITUDE = "location.gnss.longitude"
    LUDICROUSSPEEDTHRESHOLD = "location.gnss.ludicrousspeedthreshold"
    QI = "location.gnss.qi"
    SATCOUNT = "location.gnss.satcount"
    SPEED = "location.gnss.speed"
    STATE = "location.gnss.state"
    STATIONARYSPEEDTHRESHOLD = "location.gnss.stationaryspeedthreshold"
    TAIPID = "location.gnss.taipid"
    TTYPORT = "location.gnss.ttyport"
    TAIP_ID = "location.gnss.taipid"

    class ANTENNA:
        """
        Constants representing JSON keys for AOS's API GNSS debug response.

        Attributes:
            ALTITUDE (str): Key for GNSS altitude in the JSON response.
            ANTENNA_CONNECTTHRESHOLD (str): Key for GNSS antenna connect threshold in the JSON response.
            ANTENNA_DETECTION (str): Key for GNSS antenna detection in the JSON response.
            ANTENNA_DISCONNECTTHRESHOLD (str): Key for GNSS antenna disconnect threshold in the JSON response.
            ANTENNA_SHORTED (str): Key for GNSS antenna shorted state in the JSON response.
            ANTENNA_STATE (str): Key for GNSS antenna state in the JSON response.
            ANTENNABIAS (str): Key for GNSS antenna bias in the JSON response.
        """
        ANTENNA_CONNECTTHRESHOLD = "location.gnss.antenna.connectthreshold"
        ANTENNA_DETECTION = "location.gnss.antenna.detection"
        ANTENNA_DISCONNECTTHRESHOLD = "location.gnss.antenna.disconnectthreshold"
        ANTENNA_SHORTED = "location.gnss.antenna.shorted"
        ANTENNA_STATE = "location.gnss.antenna.state"
        ANTENNA_BIAS = "location.gnss.antennabias"

    class DEBUG:
        """
        Constants representing JSON keys for AOS's API GNSS debug response.

        Attributes:
            DEBUG_DRSENMSG_ENABLED (str): Key for GNSS debug DRSEN message enabled in the JSON response.
            DEBUG_ENABLED (str): Key for GNSS debug enabled state in the JSON response.
            DEBUG_FASTHIGHSENTENCES (str): Key for GNSS debug fast high sentences in the JSON response.
            DEBUG_FASTLOWSENTENCES (str): Key for GNSS debug fast low sentences in the JSON response.
            DEBUG_FASTRATE (str): Key for GNSS debug fast rate in the JSON response.
            DEBUG_FILTER (str): Key for GNSS debug filter in the JSON response.
            DEBUG_HIGHSENTENCES (str): Key for GNSS debug high sentences in the JSON response.
            DEBUG_LOWSENTENCES (str): Key for GNSS debug low sentences in the JSON response.
            DEBUG_NMEASENTENCES (str): Key for GNSS debug NMEA sentences in the JSON response.
        """
        DEBUG_DRSENMSG_ENABLED = "location.gnss.debug.drsenmsg.enabled"
        DEBUG_ENABLED = "location.gnss.debug.enabled"
        DEBUG_FASTHIGHSENTENCES = "location.gnss.debug.fasthighsentences"
        DEBUG_FASTLOWSENTENCES = "location.gnss.debug.fastlowsentences"
        DEBUG_FASTRATE = "location.gnss.debug.fastrate"
        DEBUG_FILTER = "location.gnss.debug.filter"
        DEBUG_HIGHSENTENCES = "location.gnss.debug.highsentences"
        DEBUG_LOWSENTENCES = "location.gnss.debug.lowsentences"
        DEBUG_NMEASENTENCES = "location.gnss.debug.nmeasentences"

    class FWUPDATE: 
        """
        Constants representing JSON keys for AOS's API GNNS firmware response.

        Attributes:
            FWUPDATE_CURRENTFIRMWARE (str): Key for GNSS firmware update current firmware in the JSON response.
            FWUPDATE_DRCAPABLE (str): Key for GNSS firmware update DR capable in the JSON response.
            FWUPDATE_FLASHEDFIRMWARE (str): Key for GNSS firmware update flashed firmware in the JSON response.
            FWUPDATE_MODE (str): Key for GNSS firmware update mode in the JSON response.
            FWUPDATE_SELECTEDFIRMWARE (str): Key for GNSS firmware update selected firmware in the JSON response.
        """
        FWUPDATE_CURRENTFIRMWARE = "location.gnss.fwupdate.currentfirmware"
        FWUPDATE_DRCAPABLE = "location.gnss.fwupdate.drcapable"
        FWUPDATE_FLASHEDFIRMWARE = "location.gnss.fwupdate.flashedfirmware"
        FWUPDATE_MODE = "location.gnss.fwupdate.mode"
        FWUPDATE_SELECTEDFIRMWARE = "location.gnss.fwupdate.selectedfirmware"
        
    class VB:
        """
        Constants representing JSON keys for AOS's API GNNS.VB response.

        Attributes:
            VB_ACCELQUALTIME (str): Key for GNSS VB acceleration quality time in the JSON response.
            VB_ACCELTHRESHOLD (str): Key for GNSS VB acceleration threshold in the JSON response.
            VB_BRAKEQUALTIME (str): Key for GNSS VB brake quality time in the JSON response.
            VB_BRAKETHRESHOLD (str): Key for GNSS VB brake threshold in the JSON response.
            VB_SIDEQUALTIME (str): Key for GNSS VB side quality time in the JSON response.
            VB_SIDETHRESHOLD (str): Key for GNSS VB side threshold in the JSON response.
            VB_STATE (str): Key for GNSS VB state in the JSON response.
            VB_SUMQUALTIME (str): Key for GNSS VB sum quality time in the JSON response.
            VB_SUMTHRESHOLD (str): Key for GNSS VB sum threshold in the JSON response.
        """

        VB_ACCELQUALTIME = "location.gnss.vb.accelqualtime"
        VB_ACCELTHRESHOLD = "location.gnss.vb.accelthreshold"
        VB_BRAKEQUALTIME = "location.gnss.vb.brakequaltime"
        VB_BRAKETHRESHOLD = "location.gnss.vb.brakethreshold"
        VB_SIDEQUALTIME = "location.gnss.vb.sidequaltime"
        VB_SIDETHRESHOLD = "location.gnss.vb.sidethreshold"
        VB_STATE = "location.gnss.vb.state"
        VB_SUMQUALTIME = "location.gnss.vb.sumqualtime"
        VB_SUMTHRESHOLD = "location.gnss.vb.sumthreshold"
