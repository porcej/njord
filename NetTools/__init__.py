#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetTools Module.

This module provides tools for creating simple UDP and TCP clients and servers, as well as pipe clients.
It includes functions to get the default gateway for Linux and macOS systems.

Classes and Functions:
    - get_default_gateway_linux: Retrieve the default gateway for Linux.
    - get_default_gateway_macos: Retrieve the default gateway for macOS.
    - TCPClient: A simple TCP client.
    - TCPServer: A simple TCP server.
    - UDPClient: A simple UDP client.
    - UDPServer: A simple UDP server.
    - PipeClient: A simple pipe client for inter-process communication.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

from NetTools.NetUtils import get_default_gateway_linux, get_default_gateway_macos
from NetTools.TCPClient import TCPClient
from NetTools.TCPServer import TCPServer
from NetTools.UDPClient import UDPClient
from NetTools.UDPServer import UDPServer
from NetTools.PipeClient import PipeClient


