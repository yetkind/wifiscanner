# MIT License
# Copyright (c) 2025 Yetkin Degirmenci

import subprocess
import time
import sys
import csv
from datetime import datetime

def scan_networks():
    try:
        # Run netsh command to get WiFi networks
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            text=True, encoding='utf-8', errors='ignore'
        )
    except subprocess.CalledProcessError:
        print("Failed to scan networks. Try running as Administrator.")
        return []

    networks = []
    current_ssid = None
    current_auth = None
    current_bssid = None

    for line in output.split('\n'):
        line = line.strip()
        
        # SSID 
        if line.startswith('SSID'):
            parts = line.split(':', 1)
            if len(parts) >= 2:
                current_ssid = parts[1].strip()
                current_auth = None  # Reset authentication for new SSID
                
        # Authentication 
        elif current_ssid and 'Authentication' in line:
            parts = line.split(':', 1)
            if len(parts) >= 2:
                current_auth = parts[1].strip()
                
        # BSSID 
        elif line.startswith('BSSID'):
            parts = line.split(':', 1)
            if len(parts) >= 2:
                current_bssid = parts[1].strip()
                
        # Detect Signal strength 
        elif current_bssid and 'Signal' in line:
            parts = line.split(':', 1)
            if len(parts) >= 2 and current_ssid and current_auth is not None:
                try:
                    # Convert signal percentage to RSSI (approximate ¯\_(ツ)_/¯)
                    signal = int(parts[1].strip().replace('%', ''))
                    rssi = (signal / 2) - 100  
                except ValueError:
                    continue
                
                networks.append({
                    'ssid': current_ssid,
                    'bssid': current_bssid,   
                    'rssi': int(rssi),
                    'encrypted': current_auth != 'Open'
                })
                current_bssid = None  # Reset for next BSSID

    return networks

def save_to_csv(networks, filename):
    # Define CSV headers
    headers = ["SSID", "BSSID", "RSSI (dBm)", "Encrypted"]
    
    # Write to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  
        for network in networks:
            writer.writerow([
                network['ssid'],
                network['bssid'],
                network['rssi'],
                "Yes" if network['encrypted'] else "No"
            ])
    print(f"Scan results saved to {filename}")

def main():
    print("Initializing WiFi scan...")
    print("Press Ctrl+C to exit the program.\n")
    
    try:
        while True:
            print("Scanning...")
            networks = scan_networks()
            print("Scan done!\n")
            
            if not networks:
                print("No networks found")
            else:
                print(f"{len(networks)} networks found:")
                for i, network in enumerate(networks):
                    encryption = '*' if network['encrypted'] else ' '
                    print(f"{i+1}: {network['ssid']} ({network['bssid']}) ({network['rssi']} dBm) {encryption}")
            
            print("\n-----------------------------")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting program...")
        
        # Generate filename with current date and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"wifi_scan_{timestamp}.csv"
        
        # Save the CSV
        save_to_csv(networks, filename)
        sys.exit(0)

if __name__ == "__main__":
    main()
