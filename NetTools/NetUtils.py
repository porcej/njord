#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetUtils.py: A collection of miscellaneous network utilities
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import socket
import struct
import subprocess


def get_default_gateway_linux():
    """
    Read the default gateway directly from /proc/net/route.

    This function reads the /proc/net/route file to find the default gateway 
    for the Linux system. It looks for a line where the destination (second field) 
    is '00000000' (which signifies the default route) and the flags (fourth field) 
    include the RTF_GATEWAY flag (0x2). The function then extracts and returns 
    the gateway IP address in a human-readable format.

    Returns:
        str: The default gateway IP address if found, otherwise None.

    Raises:
        IOError: If there is an issue reading the /proc/net/route file.
        ValueError: If there is an issue parsing the gateway address.
    """
    try:
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue  # If not default route or not RTF_GATEWAY, skip it

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
    except (IOError, ValueError) as e:
        # print(f"Error converting timestamp to datetime: {e}")
        return None


def get_default_gateway_macos():
    """
    Get the default gateway IP address on macOS.

    This function uses the `netstat -nr` command to retrieve the network routing table
    and then parses the output to find the default gateway IP address. The function
    looks for a line containing the word "default" and extracts the gateway IP address
    from that line.

    Returns:
        str: The default gateway IP address if found, otherwise None.

    Raises:
        subprocess.CalledProcessError: If there is an error executing the `netstat` command.
    """
    try:
        result = subprocess.run(["netstat", "-nr"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "default" in line:
                gateway_ip = line.split()[1]
                return gateway_ip
    except subprocess.CalledProcessError as e:
        # raise subprocess.CalledProcessError(f"Error executing netstat: {e}")
        return None
