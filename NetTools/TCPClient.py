#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCPClient.py: A simple TCP Client.

This module defines a TCPClient class that can be used to connect to a TCP server, send messages, and listen for responses.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import socket
import threading


class TCPClient:
    """
    TCP Client that connects to a server, allows sending messages, and listens for responses.

    Attributes:
        server_host (str): The hostname or IP address of the server.
        server_port (int): The port number of the server.
        encoding (str): The encoding scheme to use for the data stream.
        socket (socket.socket): The socket used for the connection.
    """

    def __init__(self, server_host: str, server_port: int, encoding: str = "utf-8"):
        """
        Initialize the TCP client with the specified server hostname and port.

        Args:
            server_host (str): The hostname or IP address of the server.
            server_port (int): The port number of the server.
            encoding (str): Encoding scheme to use for the data stream. Defaults to 'utf-8'.

        Raises:
            RuntimeError: If there is an error creating or connecting the socket.
        """
        self.encoding = encoding
        self.server_host = server_host
        self.server_port = server_port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
        except socket.error as e:
            raise RuntimeError(f"Failed to create and connect socket: {e}")

    def send_message(self, message: str):
        """
        Send a message to the server.

        Args:
            message (str): The message to send to the server.

        Raises:
            RuntimeError: If there is an error sending the message.
        """
        try:
            self.socket.sendall(message.encode(self.encoding))
        except socket.error as e:
            raise RuntimeError(f"Failed to send message: {e}")

    def print(self, message: str):
        """
        A wrapper for send_message.

        Args:
            message (str): The message to send to the server.
        """
        self.send_message(message)

    def receive_messages(self):
        """
        Listen for messages from the server.

        Raises:
            RuntimeError: If there is an error receiving messages.
        """
        while True:
            try:
                response = self.socket.recv(1024)
                if not response:
                    break
                print(f"Received message from server: {response.decode(self.encoding)}")
            except ConnectionResetError:
                raise RuntimeError("Connection closed by server")
            except socket.error as e:
                raise RuntimeError(f"Failed to receive message: {e}")

    def start_receiving(self):
        """
        Start a thread to listen for messages from the server.
        """
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

    def close(self):
        """
        Close the connection to the server.

        Raises:
            RuntimeError: If there is an error closing the socket.
        """
        try:
            self.socket.close()
        except socket.error as e:
            raise RuntimeError(f"Failed to close socket: {e}")


# Usage example
if __name__ == "__main__":
    client = TCPClient('127.0.0.1', 9000)
    client.start_receiving()
    try:
        while True:
            message = input("Enter message to send to server: ")
            if message.lower() == 'exit':
                client.close()
                break
            client.send_message(message)
    except KeyboardInterrupt:
        client.close()
    except RuntimeError as e:
        print(f"An error occurred: {e}")
        client.close()
