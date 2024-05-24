#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

TCPServer.py: a simple TCP Server

"""

import socket
import threading

class TCPServer:
    """
    TCP Server that accepts connections from multiple clients
    """

    def __init__(self, host, port):
        """
        Initialize the TCP server with the specified host and port.
        
        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []

    def start(self):
        """
        Start the TCP server and listen for incoming client connections.
        """
        print(f"TCP Server listening on {self.host}:{self.port}")
        self.server_socket.listen(5)  # Listen for up to 5 incoming connections
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        """
        Handle messages from a connected client.
        
        Args:
            client_socket (socket): The socket object representing the connected client.
        """
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                print(f"Received message from {client_socket.getpeername()}: {message.decode()}")
                self.send_to_all(message)
            except ConnectionResetError:
                self.disconnect_client(client_socket)
                break

    def send_to_all(self, message):
        """
        Send the specified message to all connected clients.
        
        Args:
            message (bytes): The message to send, encoded as bytes.
        """
        for client_socket in self.clients:
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                self.disconnect_client(client_socket)

    def disconnect_client(self, client_socket):
        """
        Disconnect a client.
        
        Args:
            client_socket (socket): The socket object representing the client to disconnect.
        """
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()
            print(f"Client disconnected: {client_socket.getpeername()}")

# Usage example
if __name__ == "__main__":
    server = TCPServer('127.0.0.1', 9000)
    server.start()