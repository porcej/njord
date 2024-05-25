#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetTools: a simple UDP and TCP Client and Server
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


