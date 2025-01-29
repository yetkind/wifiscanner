# WiFi Scanner

A simple Python script to scan nearby WiFi networks, retrieve their SSID, BSSID, signal strength (RSSI), and encryption status, and save the results to a CSV file.

## Features
- Scans available WiFi networks using `netsh` (Windows only).
- Displays SSID, BSSID (MAC address), RSSI (signal strength in dBm), and encryption status.
- Saves scan results to a timestamped CSV file.
- Runs continuously until stopped with `Ctrl+C`.

## Requirements
- Windows OS
- Python 3.x installed

## Usage
```sh
python wifi_scanner.py
```
Press `Ctrl+C` to stop the scan and save results to a CSV file.

## License
MIT License

