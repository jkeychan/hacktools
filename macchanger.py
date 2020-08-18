#!/usr/bin/env python3

# subprocess for the shell commands like ifconfig
# optparse for the command line help and arguments
# sys.exit for a clean ending and restarting the program in the loop
# platform to understand which command to use
# match for the regular expressions in the loops below

import subprocess
import optparse
import sys
import os
import platform
from re import match



def get_arguments():
    # Add command line argument support/help for user inputs (network interface and new MAC address)
    # This is the optparse stuff

    cli_parser = optparse.OptionParser()
    cli_parser.add_option("-i", "--interface", dest="interface", help="Interface to change.")
    cli_parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address.")
    if not options.interface: # if not True (value not set) then...
        cli_parser.error('[-] Please specify an interface name (ex. eth0), use --help for more info')
    elif not options.new_mac:
        cli_parser.error('[-] Please specify an MAC Address (ex. d6:1a:dd:85:2a:f9), use --help for more info')
    return options

def change_mac(interface, new_mac):
    print("\nChanging MAC address to " + new_mac + " ...\n")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    print("\nBringing " + interface + " back up now... \n")
    subprocess.call(["ifconfig", interface, "up"])
    print("Done! \n" + new_mac + " has been set on " + interface + "\n\n")
    subprocess.call(["ip ", "link ", "show", interface])
    print()

# Runs the get_arguments function and returns values to pass to the next function to initialize options and arguments

(options) = get_arguments()



# First command to read the network interface details
# command1 = ['ifconfig'] # Linux
# command1 = ['ipconfig'] # OSX/Darwin

if platform.system == "Darwin":
    command1 = ['ipconfig']
else:
    command1 = ['ifconfig']

# Take stdout from command1 and put into a pipe

command1.append(options.interface)
process1 = subprocess.Popen(command1, stdout=subprocess.PIPE)

# Second command to grep for the MAC/hw address and initialize as current_mac
# Takes stdout from process1 and puts into the pipe

command2 = ['grep', '-o', '-E', '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}']
process2 = subprocess.Popen(command2, stdin=process1.stdout, stdout=subprocess.PIPE)

# Initialize current_mac variable
(current_mac, err) = process2.communicate()

# User interaction

print("\n [+] Original MAC address of " + options.interface + " is: " + str(current_mac))
print("\n WARNING - This will restart your network interface and you might temporarily lose connectivity \n")
answer = input("\n Change MAC address to " + options.new_mac + " (y/N) ?  \n")

# Use regex from re to ensure only one character of a-z can be accepted, else restart the program

if not match("^[a-z]*$", answer):

    print("Invalid input. Please enter 'y' or 'n' \n")
    os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the whole program on bad input

elif answer == "y":
    change_mac(options.interface,options.new_mac)  # custom function change_mac to simplify readability

elif answer == "":
    print("Nevermind. Exiting... \n")

elif answer == "n":
    print("Nevermind. Exiting... \n")
    sys.exit()

else:
    print("Invalid input. Please enter 'y' or 'n' \n")
    os.execl(sys.executable, sys.executable, *sys.argv)
