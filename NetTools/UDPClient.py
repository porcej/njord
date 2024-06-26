#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDPClient.py: A simple UDP Client.

This module defines a UDPClient class that can be used to connect to a UDP server, send messages, and listen for responses.
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
    UDP Client that connects to a server, sends messages, and listens for responses.

    Attributes:
        server_host (str): The hostname or IP address of the server.
        server_port (int): The port number of the server.
        encoding (str): The encoding scheme to use for the data stream.
        socket (socket.socket): The socket used for the connection.
    """

    def __init__(self, server_host: str ='255.255.255.255', server_port: int =21000, encoding: str ='utf-8'):
        """
        Initialize the UDP client with the specified server hostname and port.

        Args:
            server_host (str): The hostname or IP address of the server. Defaults to subnet broadcast.
            server_port (int): The port number of the server. Defaults to 21000.
            encoding (str): Encoding scheme to use for the data stream. Defaults to 'utf-8'.

        Raises:
            RuntimeError: If there is an error creating the socket.
        """
        self.encoding = encoding
        self.server_host = server_host
        self.server_port = server_port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except socket.error as e:
            raise RuntimeError(f"Failed to create socket: {e}")

    def send_message(self, message: bytes):
        """
        Send a message to the server.

        Args:
            message (bytes): The message to send, encoded as bytes.

        Raises:
            RuntimeError: If there is an error sending the message.
        """
        try:
            self.socket.sendto(message, (self.server_host, self.server_port))
        except socket.error as e:
            raise RuntimeError(f"Failed to send message: {e}")

    def receive_response(self) -> bytes:
        """
        Listen for a response from the server.

        Returns:
            bytes: The received message from the server, encoded as bytes.

        Raises:
            RuntimeError: If there is an error receiving the response.
        """
        try:
            response, server_address = self.socket.recvfrom(1024)
            return response
        except socket.error as e:
            raise RuntimeError(f"Failed to receive response: {e}")

    def send_string(self, message: str):
        """
        Send a string message to the server.

        Args:
            message (str): The message to send.

        Raises:
            RuntimeError: If there is an error sending the message.
        """
        self.send_message(message.encode(self.encoding))

    def receive_string(self) -> str:
        """
        Listen for a string response from the server.

        Returns:
            str: The received message from the server, decoded as a string.

        Raises:
            RuntimeError: If there is an error receiving the response.
        """
        response = self.receive_response()
        return response.decode(self.encoding)

    def print(self, message: str):
        """
        A wrapper for send_string.

        Args:
            message (str): The message to send to the server.
        """
        self.send_string(message)


# Usage example
if __name__ == "__main__":
    client = UDPClient('255.255.255.255', 21000)
    message = "Hello, world!"

    try:
        client.send_string(message)
        print("Message sent to server.")
        response = client.receive_string()
        print(f"Received response from server: {response}")
    except RuntimeError as e:
        print(f"An error occurred: {e}")
