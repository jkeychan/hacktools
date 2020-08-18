#!/usr/bin/env python3

# subprocess for the shell commands like ifconfig
# optparse for the command line help and arguments
# sys.exit for a clean ending and restarting the program in the loop
# re for the regular expressions and matching in MAC address and user answers
# time for basic sleep after restarting the network interface

import subprocess
import optparse
import sys
import os
import re
import time


def get_arguments():
    # Add command line argument support/help for user inputs (network interface and new MAC address)
    # This is the optparse stuff

    cli_parser = optparse.OptionParser()
    cli_parser.add_option("-i", "--interface", dest="interface", help="Interface to change.")
    cli_parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address.")
    (options, arguments) = cli_parser.parse_args()
    if not options.interface:  # if not True (value not set) then...
        cli_parser.error('[-] Please specify an interface name (ex. eth0), use --help for more info')
    elif not options.new_mac:
        cli_parser.error('[-] Please specify an MAC Address (ex. d6:1a:dd:85:2a:f9), use --help for more info')
    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


def change_mac(interface, new_mac):
    current_mac = get_current_mac(options.interface)
    print("\nChanging MAC address from " + current_mac + " to " + new_mac + " ...\n")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    print("\nBringing " + interface + " back up now... \n")
    time.sleep(2)
    subprocess.call(["ifconfig", interface, "up"])


# Runs the get_arguments function and returns values to pass to the next function to initialize options and arguments
(options) = get_arguments()

# Brings current_mac out of the function for others to use
current_mac = get_current_mac(options.interface)

# User interaction

print("\n [+] Original MAC address of " + options.interface + " is: " + str(current_mac))
print("\n WARNING - This will restart your network interface and you might temporarily lose connectivity \n")
answer = input("\n Change MAC address to " + options.new_mac + " (y/N) ?  \n")

# Use regex from re to ensure only Y or N can be accepted, else restart the program. If N, then exit

if not re.match(r"[Yy]|[Nn]", answer):
    print("Invalid input. Please enter 'y' or 'n' \n")
    os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the whole program on bad input

elif re.match(r"[Yy]", answer):
    change_mac(options.interface, options.new_mac)  # custom function change_mac to simplify readability

else:
    print("Nevermind. Exiting... \n")
    sys.exit()
