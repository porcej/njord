#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDPServer.py: A simple UDP Server.

This module defines a UDPServer class that accepts connections from multiple clients, handles incoming messages,
and broadcasts messages to all connected clients.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import socket


class UDPServer:
    """
    UDP Server that accepts connections from multiple clients and sends messages to all of them.

    Attributes:
        host (str): The hostname or IP address to bind the server to.
        port (int): The port number to bind the server to.
        encoding (str): The encoding used for the data stream.
        clients (dict): Dictionary to track connected clients.
        socket (socket.socket): The socket used for the server.
    """

    def __init__(self, host: str, port: int, encoding: str = "utf-8"):
        """
        Initialize the UDP server with the specified host and port.

        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
            encoding (str): The encoding used for the data stream. Defaults to 'utf-8'.

        Raises:
            RuntimeError: If there is an error creating or binding the socket.
        """
        self.host = host
        self.port = port
        self.encoding = encoding
        self.clients = {}  # Dictionary to track connected clients
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
        except socket.error as e:
            raise RuntimeError(f"Failed to create and bind socket: {e}")

    def run(self):
        """
        Start running the UDP server, accepting connections from clients and sending messages.
        """
        print(f"UDP Server listening on {self.host}:{self.port}")
        try:
            while True:
                data, client_address = self.socket.recvfrom(1024)
                print(f"Received message from {client_address}: {data.decode(self.encoding)}")
                self.handle_message(data, client_address)
        except socket.error as e:
            raise RuntimeError(f"Socket error: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def handle_message(self, message: bytes, client_address: tuple):
        """
        Handle an incoming message from a client.

        Args:
            message (bytes): The message received from the client, encoded as bytes.
            client_address (tuple): The address of the client (hostname, port).
        """
        if client_address not in self.clients:
            self.clients[client_address] = True
        self.send_to_all(message)

    def send_to_all(self, message: bytes):
        """
        Send the specified message to all connected clients.

        Args:
            message (bytes): The message to send, encoded as bytes.
        """
        for client_address in self.clients:
            try:
                self.socket.sendto(message, client_address)
            except socket.error as e:
                print(f"Error sending message to client {client_address}: {e}")
                self.disconnect_client(client_address)

    def disconnect_client(self, client_address: tuple):
        """
        Disconnect a client.

        Args:
            client_address (tuple): The address of the client to disconnect (hostname, port).
        """
        if client_address in self.clients:
            del self.clients[client_address]
            print(f"Client disconnected: {client_address}")

    def get_connected_clients(self) -> list:
        """
        Get a list of connected client addresses.

        Returns:
            list: A list of tuples containing client address and port.
        """
        return list(self.clients.keys())


# Usage example
if __name__ == "__main__":
    try:
        server = UDPServer('127.0.0.1', 9000)
        server.run()
    except RuntimeError as e:
        print(f"An error occurred: {e}")
