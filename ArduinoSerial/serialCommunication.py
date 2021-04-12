# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 13:52:37 2021

@author: Justas
"""

import serial
from time import sleep



def readValues(cmdString):
    cmd = cmdString + '\r\n'  # adds enter at the end of line
    
    emptyLines = 0  # counter of empty lines
    ser.write(cmd.encode('ascii'))

    loop = True
    while loop:
        arduinoData = ser.readline().decode().split('\r\n')
        print(arduinoData[0])
        
        # Reads data until it reaches empty line
        if arduinoData[0] == '':
            emptyLines += 1
            if emptyLines == numEmptyLines:  # counting empty lines
                loop = False
    # sleep(2)
    ser.flushInput()


def sendCommand(string):
    command = string + '\r\n'
    ser.write(command.encode('ascii'))
    
    arduinoData = ser.readline().decode().split('\r\n')
    print(arduinoData[0])
    
    ser.flushInput()


def readFromFile(filename):
    cmdList = open(filename, 'r').read().split('\n')  # reading data from file
    # Use data from text file to send commands to serial
    for i in range(len(cmdList)):
            command = cmdList[i]
        
            if command == '?' or command == 'help':
                readValues(command)
            
            else:
                sendCommand(command)
    
    print('Finished reading a file.')



ser = serial.Serial(port='COM5', baudrate=38400, timeout=.1)
sleep(1)
print('Serial opened.')
ser.flushInput()  # flush input at the beginning to get rid of 'Squarewave driver' - allows to see if 1st command is bad

numEmptyLines = 3  # maximum number of empty lines for 'readValues' function

loop = True  # variable to enable while loop

while loop:
    
    userInput = input('Enter command (or "read file"): ')
    
    if userInput == '?' or userInput == 'help':
        readValues(userInput)
    
    elif userInput == 'end':
        loop = False
        ser.close()
    
    elif userInput == 'read file':
        userInputFilename = input('Type a name of file: ')
        filename = userInputFilename# + '.txt'
        readFromFile(filename)
    
    else:
        sendCommand(userInput)

print('Serial closed.')