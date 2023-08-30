#!/usr/bin/env python3

import subprocess
import re
import sys
import time
import argparse
import platform


def get_arguments():
    parser = argparse.ArgumentParser(description="MAC Address Changer Tool",
                                     usage="macchanger.py -i <interface> -m <MAC_address>")
    parser.add_argument("-i", "--interface", dest="interface",
                        required=True, help="Interface to change. (Required)")
    parser.add_argument("-m", "--mac", dest="new_mac", required=True,
                        help="New MAC Address in format XX:XX:XX:XX:XX:XX. (Required)")
    return parser.parse_args()


def validate_mac(mac_address):
    if re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac_address):
        return True
    else:
        print("[-] Invalid MAC address format. Ensure it's in format XX:XX:XX:XX:XX:XX")
        sys.exit(1)


def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(
            ["ifconfig", interface]).decode()
        mac_address_search_result = re.search(
            r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Could not read MAC address.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print(
            f"[-] Could not get details for {interface}. Ensure the interface name is correct.")
        sys.exit(1)


def change_mac(interface, new_mac, current_mac):
    print(f"\nChanging MAC address from {current_mac} to {new_mac} ...\n")
    try:
        if platform.system() == "Linux":
            subprocess.call(["sudo", "ifconfig", interface, "down"])
            subprocess.call(
                ["sudo", "ifconfig", interface, "hw", "ether", new_mac])
            subprocess.call(["sudo", "ifconfig", interface, "up"])
        elif platform.system() == "Darwin":  # Darwin indicates macOS
            subprocess.call(["sudo", "ifconfig", interface, "ether", new_mac])
            subprocess.call(["sudo", "ifconfig", interface, "up"])
        else:
            print("[-] Unsupported Operating System.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"[-] Failed to change MAC address for {interface}.")
        sys.exit(1)

    if get_current_mac(interface) == new_mac:
        print(f"\n[+] MAC address was successfully changed to {new_mac}")
    else:
        print("[-] MAC address did not change. Please try again.\n")


if __name__ == '__main__':
    options = get_arguments()

    if validate_mac(options.new_mac):
        current_mac = get_current_mac(options.interface)
        print(
            f"\n[+] The current MAC address of {options.interface} is: {current_mac}")
        print("\n WARNING - This may restart your network interface and you might temporarily lose connectivity.\n")
        answer = input(f"Change MAC address to {options.new_mac} (y/n)? ")

        if answer.lower() not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            sys.exit(1)
        elif answer.lower() == 'y':
            change_mac(options.interface, options.new_mac, current_mac)
        else:
            print("Nevermind. Exiting...")
            sys.exit()
