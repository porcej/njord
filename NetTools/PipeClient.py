#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PipeClient.py: a simple messenger that sends to a stream
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
    Pipe Client that connects to a pipe, sends a message, and listens for a response.
    """

    def __init__(self, pipe=sys.stdout, encoding='utf-8'):
        """
        Initialize the pipe client with the specified pipe and encoding.

        Args:
            pipe (io.TextIOWrapper): The pipe to write messages to. Defaults to sys.stdout.
            encoding (str): Encoding scheme to use for data stream. Defaults to 'utf-8'.
        """
        self.encoding = encoding
        self.pipe = pipe


    def print(self, message):
        """
        Sends a message to the pipe.

        Args:
            message (str): The message to send to the pipe.
        """
        print(message.encode(self.encoding).decode(self.encoding), file=self.pipe)


# Usage example
if __name__ == "__main__":
    client = PipeClient()
    message = "Hello, world!"

    client.print(message)
    print("Message sent to pipe.")