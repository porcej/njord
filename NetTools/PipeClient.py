#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

STDOUTClientpy: a simple messenger that sends to the screen

"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import sys

class PipeClient:
    """
    Pipe Client that connects to a server, sends a message, and listens for a response.
    """

    def __init__(self, pipe=sys.stdout, encoding='utf-8'):
        """
        Initialize the pipe client with the specified server hostname and port.
        
        Args:
            server_host (str): The hostname or IP address of the server. Detaults to subnet broadcast
            server_port (int): The port number of the server. Defaults to 21000
            encoding (str): Endoding scheme to use for data stream
        """
        self.encoding = encoding
        self.pipe = pipe
        print("Hello")


    def print(self, message):
        """
        Sends a message to the pipe
        
        Args:
            message (str): The message to send to the pipe.
        """
        print("HERE")
        print(message.encode(self.encoding), file=self.pipe)



# Usage example
if __name__ == "__main__":
    # client = UDPClient('127.0.0.1', 9000)
    client = UDPClient('255.255.255.255', 21000)
    message = "Hello, world!"

    client.send_string(message)
    print("Message sent to server.")
    response = client.receive_string()
    print(f"Received response from server: {response}")
