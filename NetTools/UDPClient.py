#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

UDPClient.py: a simple UDP Client

"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import socket

class UDPClient:
    """
    UDP Client that connects to a server, sends a message, and listens for a response.
    """

    def __init__(self, server_host='255.255.255.255', server_port=21000, encoding='utf-8'):
        """
        Initialize the UDP client with the specified server hostname and port.
        
        Args:
            server_host (str): The hostname or IP address of the server. Detaults to subnet broadcast
            server_port (int): The port number of the server. Defaults to 21000
            encoding (str): Endoding scheme to use for data stream
        """
        self.encoding = encoding
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    def send_message(self, message):
        """
        Send a message to the server.
        
        Args:
            message (bytes): The message to send, encoded as bytes.
        """
        self.socket.sendto(message, (self.server_host, self.server_port))


    def receive_response(self):
        """
        Listen for a response from the server.
        
        Returns:
            bytes: The received message from the server, encoded as bytes.
        """
        response, server_address = self.socket.recvfrom(1024)
        return response


    def print(self, message):
        """
        A wrapper for send_string
        
        Args:
            message (str): The message to send to the server.
        """
        self.send_string(message)


    def send_string(self, message):
        """
        Send a message to the server.
        
        Args:
            message (str): The message to send
        """
        self.send_message(message.encode(self.encoding))


    def receive_string(self):
        """
        Listen for a response from the server.
        
        Returns:
            bytes: The received message from the server, encoded as bytes.
        """
        response, server_address = self.socket.recvfrom(1024)
        return response.decode(self.encoding)

# Usage example
if __name__ == "__main__":
    # client = UDPClient('127.0.0.1', 9000)
    client = UDPClient('255.255.255.255', 21000)
    message = "Hello, world!"

    client.send_string(message)
    print("Message sent to server.")
    response = client.receive_string()
    print(f"Received response from server: {response}")
