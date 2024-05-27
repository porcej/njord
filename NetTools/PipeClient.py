#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PipeClient.py: A simple messenger that sends messages to a stream.

This module defines a PipeClient class that can be used to send messages to a specified pipe (such as sys.stdout)
with a specified encoding.
"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"

import sys
import io


class PipeClient:
    """
    Pipe Client that connects to a pipe, sends a message, and listens for a response.

    Attributes:
        pipe (io.TextIOWrapper): The pipe to write messages to.
        encoding (str): The encoding scheme to use for the data stream.
    """

    def __init__(self, pipe: io.TextIOWrapper = sys.stdout, encoding: str = 'utf-8'):
        """
        Initialize the pipe client with the specified pipe and encoding.

        Args:
            pipe (io.TextIOWrapper): The pipe to write messages to. Defaults to sys.stdout.
            encoding (str): Encoding scheme to use for the data stream. Defaults to 'utf-8'.
        """
        self.encoding = encoding
        self.pipe = pipe

    def print(self, message: str):
        """
        Send a message to the pipe.

        Args:
            message (str): The message to send to the pipe.
        """
        encoded_message = message.encode(self.encoding).decode(self.encoding)
        print(encoded_message, file=self.pipe)


# Usage example
if __name__ == "__main__":
    client = PipeClient()
    message = "Hello, world!"

    client.print(message)
    print("Message sent to pipe.")
