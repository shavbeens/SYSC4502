# Server for Hotel Reservation
# UDP_Pinger_Server.py from Lab 1 was used as the Framework for the communication side of the server

# Written by: Shaviyo Marasinghe 101019133
# SYSC 4502: Aassignment 1

import random
import sys
from socket import *

# Get Port number from Parameter
port = sys.argv[1]


# Generic function for getting and returning Lines from a text file, Returns a String list
def getlines(filename):
    with open(filename) as f:
        linelist = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    linelist = [x.strip() for x in linelist]
    return linelist


# Function for getting the reservable rooms from rooms.txt file, Function required by Assignment
def rooms():
    roomlist = getlines("rooms.txt")
    return roomlist, True


# Function for getting the reservable days from the days.txt file, Function required by Assignment
def days():
    dayslist = getlines("days.txt")
    return dayslist, True


# Function for getting the reservable timeslots from the timeslots.txt file, Function required by Assignment
def timeslots():
    timeslotlist = getlines("timeslots.txt")
    return timeslotlist, True


# Function for getting all the current reservations from the reservations.txt file
def reservations():
    reservationlist = getlines("reservations.txt")
    return reservationlist


# Function to check if the day passed in the parameter is a reservable day
def checkdays(day):
    if day in days()[0]:
        return True
    return False


# Function to check if the timeslot passed in the parameter is a reservable timeslot
def checktimeslots(timeslot):
    if timeslot in timeslots()[0]:
        return True
    return False


# Function to get the reservations which were made for the room passed in the parameter, Function required by Assignment
def check(room):
    if room in rooms()[0]:
        currentreservations = reservations()
        reservationlist = []
        isempty = True
        index = 0
        for item in currentreservations:
            if room in item:
                reservationlist.insert(index, item)
                index = index + 1
                isempty = False
        return reservationlist, isempty
    else:
        return "This room does not exist", True


# Function to reserve a room in the given day at the given timeslot, Function required by Assignment
def reserve(room, timeslot, day):
    currentreservations = check(room)
    if not checkdays(day):
        return "This day is invalid for a reservation", False
    if not checktimeslots(timeslot):
        return "This timeslot is invalid for a reservation", False
    reservationsfile = open("reservations.txt", "a")
    if currentreservations[1]:
        # this room doesn't exist in the check function, so a reservation can be made but check if this room is real
        if room in rooms():
            reservationsfile.write("{} {} {}\n".format(room, timeslot, day))
            reservationsfile.close()
            return "A reservation was made", True
        else:
            return "This room does not exist", False

    else:
        # Check the currentreservations list to see if the timeslot for this reservation is in the list
        reservationslist = currentreservations[0]
        for index in reservationslist:
            if day not in index:
                reservationsfile.write("{} {} {}\n".format(room, timeslot, day))
                reservationsfile.close()
                return "A reservation was made", True
            else:
                if timeslot not in index:
                    reservationsfile.write("{} {} {}\n".format(room, timeslot, day))
                    reservationsfile.close()
                    return "A reservation was made", True
                else:
                    reservationsfile.close()
                    return "Could not make this reservation, check if this timeslot is available", False


# Function to delete a reservation for a given room, on a given day, at a given time, Function required by Assignment
def delete(room, timeslot, day):
    currentreservations = check(room)
    if currentreservations[1]:
        # this reservation never existed to delete
        return "Reservation doesn't exist", False

    else:
        reservationslist = currentreservations[0]
        for index in reservationslist:
            reservation = str(index).split(' ')
            if day == reservation[2]:
                if timeslot == reservation[1]:
                    # This means this room, Day, and timeslot exists. So now remove
                    with open("reservations.txt", "r") as f:
                        lines = f.readlines()
                    with open("reservations.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != "{} {} {}".format(room, timeslot, day):
                                f.write(line)
                    return "Reservation was Removed", True
        # There is no reservation that matches the given parameters
        return "This reservation doesn't exist", False


# Function to quit the application, Function required by Assignment
def quitapp():
    sys.exit()
    # return "quitappnow", False


# Chooses which function to go for given the command that was given by the client
def sortmessage(messagearray):
    # Default failsafe, if anything doesn't work right, default will ask the client to try again
    retrunmessage = "Something has gone wrong, Try again"

    # For commands 0-2, all we have to do is call the function that was defined above. Just reads the files
    if messagearray[0] == "0":
        returnmessage = days()
    elif messagearray[0] == "1":
        returnmessage = rooms()
    elif messagearray[0] == "2":
        returnmessage = timeslots()
    # Command 3 is check function, should have 2 arguments. The command and which room needs to be checked
    elif messagearray[0] == "3":
        if len(messagearray) == 2:
            returnmessage = check(messagearray[1])
        # If command 3 was called without 2 arguments, then it's an error, return right away
        else:
            returnmessage = "Something has gone wrong, Try again"
    # Command 4 is reserve, should have 4 arguments. The command, Room, Time slot, and Day.
    elif messagearray[0] == "4":
        if len(messagearray) == 4:
            returnmessage = reserve(messagearray[1], messagearray[2], messagearray[3])
        else:
            returnmessage = "Something has gone wrong, Try again"
    # Command 5 is delete, should have 4 arguments. The command, Room, Time slot, and Day.
    elif messagearray[0] == "5":
        if len(messagearray) == 4:
            returnmessage = delete(messagearray[1], messagearray[2], messagearray[3])
        else:
            returnmessage = "Something has gone wrong, Try again"
    # Command 6 is Quitting the application
    elif messagearray[0] == "6":
        returnmessage = quitapp()

    return returnmessage


# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', int(port)))
print("Waiting for Packet to arrive...")

while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    message2 = message.decode("utf-8")

    # Split the message according to ',' and store in List
    splitmessage = str(message2).split(',')
    # Remove any accidental white spaces
    splitmessage = [x.strip(' ') for x in splitmessage]
    # Print to console just so we can see if the correct message was received
    print(splitmessage, end="\n\n")

    # Call sortmessage function which will take the list, and return a correct message for the commands
    returnarray = str(sortmessage(splitmessage))

    # Respond to the client with the correct message
    serverSocket.sendto(returnarray.encode(), address)
