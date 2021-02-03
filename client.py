# UDP_Pinger_client.py from Lab 1 was used as the Framework for this Assignment. Everything was build on top

# Written by Shaviyo Marasinghe: 101019133
# SYSC 4502 Assignment 1

import random
import time
from socket import *
import sys
import string

# Get address and port number from command arguments
address = sys.argv[1]
port = sys.argv[2]

# create cleintSocket with Arguments passed from parameters
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)


# The functions for days.txt file reading command
def days():
    return "0"


# The functions for rooms.txt file reading command
def rooms():
    return "1"


# The functions for timeslots.txt file reading command
def timeslots():
    return "2"


# The functions for retrieving current reservations for a room command
def check():
    # Prompts user for Room number
    room = input("Please enter the Room Number you wish to check: ")
    room.strip()
    return "3, {}".format(room)


# The function for Reserving a room command
def reserve():
    room = input("Please enter the Room Number you wish to reserve: ")
    room.strip()
    day = input("Please enter the Day you wish the reservation to be made on: ")
    day.strip()
    timeslot = input("Please enter the time slot you wish to reserve: ")
    timeslot.strip()
    return "4, {}, {}, {}".format(room, timeslot, day)


# The function for deleting an already made reservation command
def delete():
    room = input("Please enter the Room Number you wish to delete the reservation of: ")
    room.strip()
    day = input("Please enter the Day the reservation is made on: ")
    day.strip()
    timeslot = input("Please enter the time slot the reservation is made on: ")
    timeslot.strip()
    return "5, {}, {}, {}".format(room, timeslot, day)


# The function for quiting the application
def quitapp():
    return "6"


# This acts like a switch function for whatever input the user gives regarding what they want to do
options = {0: days,
           1: rooms,
           2: timeslots,
           3: check,
           4: reserve,
           5: delete,
           6: quitapp
           }

while True:
    print("Please enter one of the following numbers regarding your reservation")
    print("0: Check what days a reservation can be made on")
    print("1: Check what rooms a reservation can be made on")
    print("2: Check what timeslots a reservation can be made on")
    print("3: Check the existing reservations for a room")
    print("4: Reserve a room at a specific timeslot")
    print("5: Delete an existing reservation")
    print("6: Quit from the Application\n\n")

    command = input("Please enter your command: ")

    # Go to the respective function for the command entered and get the message from that function
    sendingMessage = options[int(command)]()

    # Send the message that has was formatted for the respective commands (0 to 6), then print the message to console
    sentTime = time.time()
    clientSocket.sendto(sendingMessage.encode(), (address, int(port)))
    print("Message sent with the following: ", sendingMessage)

    # if the last command we sent was to quit, then exit from the application
    if sendingMessage == '6':
        sys.exit()

    # Otherwise, we can keep going ahead with our application
    try:
        # Receive response from Server, record the received time
        receivedMessage, serverAddress = clientSocket.recvfrom(int(port))
        receivedTime = time.time()

        # calculate round trip time from sent and received time captures, print the rtt to console
        rtt = str(receivedTime - sentTime)
        print("Got a response; it took {}Seconds".format(rtt))
        # received message is printed so the user can see if the server responded appropriately to what they requested
        print("Received Message is: ", receivedMessage.decode(), end="\n\n")

    except:
        # If a timeout occurs, then notify that a timeout occurred, request the user to retry that command.
        print("Request timed out, try this command again.", end="\n\n")
        pass