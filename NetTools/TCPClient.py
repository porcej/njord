#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

TCPClient.py: a simple TCP Client

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
    """

    def __init__(self, server_host, server_port, encoding="utf-8"):
        """
        Initialize the TCP client with the specified server hostname and port.
        
        Args:
            server_host (str): The hostname or IP address of the server.
            server_port (int): The port number of the server.
            encoding (str): Endoding scheme to use for data stream
        """
        self.encoding = encoding
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

    def send_message(self, message):
        """
        Send a message to the server.
        
        Args:
            message (str): The message to send to the server.
        """
        self.socket.sendall(message.encode(self.encoding))

    def print(self, message):
        """
        A wrapper for send_mesage
        
        Args:
            message (str): The message to send to the server.
        """
        self.send_message(message)
    def print(self, message):
        """
        A wrapper for send_mesage
        
        Args:
            message (str): The message to send to the server.
        """
        self.send_message(message)

    def receive_messages(self):
        """
        Listen for messages from the server.
        """
        while True:
            try:
                response = self.socket.recv(1024)
                if not response:
                    break
                print(f"Received message from server: {response.decode(self.encoding)}")
            except ConnectionResetError:
                print("Connection closed by the server.")
                break

    def start_receiving(self):
        """
        Start a thread to listen for messages from the server.
        """
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def close(self):
        """
        Close the connection to the server.
        """
        self.socket.close()

# Usage example
if __name__ == "__main__":
    client = TCPClient('127.0.0.1', 9000)
    client.start_receiving()
    while True:
        try:
            message = input("Enter message to send to server: ")
            if message.lower() == 'exit':
                client.close()
                break
            client.send_message(message)
        except KeyboardInterrupt:
            client.close()
            break