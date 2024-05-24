#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

UDPClient.py: a simple UDP Server

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
    UDP Server that accepts connections from multiple clients and sends a message to all of them.
    """

    def __init__(self, host, port, encoding="utf-8"):
        """
        Initialize the UDP server with the specified host and port.
        
        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
            encoding (str): The encoding used for the data stream
        """
        self.host = host
        self.port = port
        self.encoding = encoding
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.clients = {}  # Dictionary to track connected clients

    def run(self):
        """
        Start running the UDP server, accepting connections from clients and sending messages.
        """
        print(f"UDP Server listening on {self.host}:{self.port}")
        while True:
            data, client_address = self.socket.recvfrom(1024)
            print(f"Received message from {client_address}: {data.decode(self.encoding)}")
            self.handle_message(data, client_address)

    def handle_message(self, message, client_address):
        """
        Handle an incoming message from a client.
        
        Args:
            message (bytes): The message received from the client, encoded as bytes.
            client_address (tuple): The address of the client (hostname, port).

        Returns:
            str: The received message.
        """
        if client_address not in self.clients:
            self.clients[client_address] = True
        return message

    def send_to_all(self, message):
        """
        Send the specified message to all connected clients.
        
        Args:
            message (bytes): The message to send, encoded as bytes.
        """
        for client_address in self.clients:
            self.socket.sendto(message, client_address)

    def disconnect_client(self, client_address):
        """
        Disconnect a client.
        
        Args:
            client_address (tuple): The address of the client to disconnect (hostname, port).
        """
        if client_address in self.clients:
            del self.clients[client_address]
            print(f"Client disconnected: {client_address}")

    def get_connected_clients(self):
        """
        Get a list of connected client addresses.
        
        Returns:
            list: A list of tuples containing client address and port.
        """
        return list(self.clients.keys())


# Usage example
if __name__ == "__main__":
    server = UDPServer('127.0.0.1', 9000)
    server.run()
