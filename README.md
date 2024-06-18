
# NJORD

**NJORD** is a Python application designed to augment a GNSS data stream based on known WiFi AP (Access Point) locations. This application is intended for use in a buoy setup to improve GNSS accuracy using WiFi APs.  Initial GNSS information is obtained from the AirlinkOS API.

## Features
- Updates GNSS state based on known WiFi AP locations.
- Falls back to using the AirlinkOS API for GNSS state if no known APs are available.
- Supports configuration updates from a local file or a remote URL.
- Provides options to send GNSS data via UDP, TCP, or to standard output.

## Installation
Ensure you have Python 3.x installed on your system. You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage
You can run the NJORD application using the command line. Below are the available options:

```bash
usage: njord.py [-h] [-a AOSURL] [-c CONFIG] [-C CONFIG_URL] [-g] [-U UDPPORT]
                [-s] [-t TCPPORT] [-T TCPHOST] [-u USERNAME] [-p PASSWORD]
                [-v] [-B BEACON] [-M {taip_pv,nmea_rmc,all}] [-i UPDATE]
                [-m MSG_TYPE PROTOCOL PORT HOST]
                [-z MSG_TYPE PROTOCOL PORT HOST ALIAS] [-b MSG_TYPE PORT]
                [-Z MSG_TYPE PORT ALIAS] [-n NUM_WIFI_SCAN]
                [-W WIFI_SCAN_DELAY] [-d HDOP_EXCELLENT_THRESHOLD]
                [-D HDOP_POOR_THRESHOLD]

NJORD - A buoy to augment a GNSS data stream based on known Wifi AP locations.

options:
  -h, --help            show this help message and exit
  -a AOSURL, --aosurl AOSURL
                        Base URL for AOS API, defaults to
                        "https://192.168.1.1", if a file path is provided,
                        tries to read the file as a proxy API.
  -c CONFIG, --config CONFIG
                        File path for local config file.
  -C CONFIG_URL, --config_url CONFIG_URL
                        URL to acquire net config files.
  -g, --gateway         Sets the AOS API URL to the network\'s gateway.
                        Overrides --aosurl.
  -U UDPPORT, --udpport UDPPORT
                        UDP port to send GNSS broadcast messages
  -s, --stdout          Prints TAIP messages to Standard Output
  -t TCPPORT, --tcpport TCPPORT
                        TCP Port to send GNSS messages.
  -T TCPHOST, --tcphost TCPHOST
                        TCP Server to send messages.
  -u USERNAME, --username USERNAME
                        Username for AOS authentication. - overrides config
                        file
  -p PASSWORD, --password PASSWORD
                        Password for AOS authentication. - overrides config
                        file
  -v, --verbose         Prints messages to standard output.
  -B BEACON, --beacon BEACON
                        Sets the beacon interval in seconds
  -M {taip_pv,nmea_rmc,all}, --messagetype {taip_pv,nmea_rmc,all}
                        Specify the message type (taip_pv, nmea_rmc, or all).
                        Default is "taip_rmc".
  -i UPDATE, --update UPDATE
                        Sets the config update interval in seconds.
  -m MSG_TYPE PROTOCOL PORT HOST, --message MSG_TYPE PROTOCOL PORT HOST
                        Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC),
                        PROTOCOL (TCP/UDP), PORT (int), HOST (str)
  -z MSG_TYPE PROTOCOL PORT HOST ALIAS, --message-alias-taip MSG_TYPE PROTOCOL PORT HOST ALIAS
                        Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC),
                        PROTOCOL (TCP/UDP), PORT (int), HOST (str), TAIP ALIAS
                        (fixed value or +N/-N)
  -b MSG_TYPE PORT, --broadcast-message MSG_TYPE PORT
                        Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PORT
                        (int)
  -Z MSG_TYPE PORT ALIAS, --broadcast-message-alias-taip MSG_TYPE PORT ALIAS
                        Message parameters: MSG_TYPE (TAIP_PV/NMEA_RMC), PORT
                        (int), TAIP ALIAS (fixed value or +N/-N)
  -n NUM_WIFI_SCAN, --num-wifi-scan NUM_WIFI_SCAN
                        Number of times to scan for Wifi APs per beacon
                        interval (int) Defaults is 1.
  -W WIFI_SCAN_DELAY, --wifi-scan-delay WIFI_SCAN_DELAY
                        Delay between subsaquint Wifi scans in seconds.
                        Default is 1.
  -d HDOP_EXCELLENT_THRESHOLD, --hdop-excellent-threshold HDOP_EXCELLENT_THRESHOLD
                        When GNSS data is reported to be less than this value
                        (float), Wifi scan is not performed and GNSS data is
                        reported.
  -D HDOP_POOR_THRESHOLD, --hdop-poor-threshold HDOP_POOR_THRESHOLD
                        When GNSS data has a HDOP greather than this value,
                        the GNSS data is ignored as invalid.


```

## Example
To run NJORD with a local configuration file and send GNSS data to a TCP server:

```bash
python3 njord.py -c /path/to/config.json -T your.tcphost.com -t 9011
```

## Configuration
The configuration file should be in JSON format and include the known access points and API credentials. Below is an example of a configuration file:

```json
{
    "KnownAps": [
        {
            "Ssid": "example_ssid",
            "Bssid": "00:11:22:33:44:55",
            "Latitude": 40.7128,
            "Longitude": -74.0060
        }
    ],
    "LastUpdated": "2024-05-28T00:00:00",
    "ApiUser": {
        "Username": "your_username",
        "Password": "your_password"
    }
}
```

## License
NJORD is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author
- **Joe Porcelli** - *Initial work* - [www.kt3i.com](www.kt3i.com)

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Acknowledgements
- Special thanks to the developers of the `requests` and `argparse` libraries for making network requests and command-line argument parsing easier.

---
