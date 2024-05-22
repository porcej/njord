#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NJORD Tests

A buoy to augment a GNSS data stream based on known Wifi AP locations.

A set of test to run against njord

"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"
__description__ = "A buoy to augment a GNSS data stream based on known Wifi AP locations."
__app_name__ = "NJORD"

import argparse
import json
import os
import re
import requests
from urllib.parse import urlparse
from aosclient import AOSClient, AOSKeys
from gnss import GNSS

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NJORD

A buoy to augment a GNSS data stream based on known Wifi AP locations.


"""

__author__ = "Joe Porcelli"
__copyright__ = "Copyright 2024, Joe Porcelli"

__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "porcej@gmail.com"
__status__ = "Development"
__description__ = "A buoy to augment a GNSS data stream based on known Wifi AP locations."
__app_name__ = "NJORD"

import argparse
import json
import os
import re
import requests
from urllib.parse import urlparse
from aosclient import AOSClient, AOSKeys
from gnss import GNSS
import njord



def test_aos_wifi_response(file_or_url, config):
    """
    Reads JSON data from a file path or URL, generates a TAIP A PV message based on a known Wifi AP, prints the message to standard output,
    and exits with an appropriate return code.

    Args:
        file_or_url (str): The file path or URL from which to read the JSON data.
        conifg (dict): The configuration dictionary for the application including the KnownAccessPoints list.

    """
    aos_resp = njord.load_json_from_url_or_file(file_or_url)
    gnss = njord.load_aos_check_and_set_state(aos_resp, config)
    taip_message = gnss.taip_pv_message()
    print(taip_message)

def test_aos_gnss_response(file_or_url):
    """
    Reads JSON data from a file path or URL, generates a TAIP A PV message, prints the message to standard output,
    and exits with an appropriate return code.

    Args:
        file_or_url (str): The file path or URL from which to read the JSON data.

    """
    config = {'KnownAps': {}}
    aos_resp = njord.load_json_from_url_or_file(file_or_url)
    gnss = njord.load_aos_check_and_set_state(aos_resp, config)
    taip_message = gnss.taip_pv_message()
    print(taip_message)

