#!/usr/bin/env python3
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder  = mD.dataFolder
devices    = mD.rs232_devices



def readPort(port):
    ser = serial.Serial(
        port = port,
        baudrate = 2400,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=0
    )

    print("Connected to: {0}".format(ser.portstr))

    line = [] # used to store a line of data
    while True: # continuously check for data
        for c in ser.read():
            line.append(chr(c)) # add character to line
            if chr(c) == '\n': # line ends at newline character
                dataString = ''.join(line)
                dataString = dataString.replace('\n', '')
                # make the dataString take the proper mints format
                dataString = formatForDeviceType(dataString, ser)
                print(dataString)
                dt = datetime.datetime.now()
                mSR.dataSplit(dataString, dt)
                line = []


def formatForDeviceType(dataString, ser):
    data = dataString.split(',')
    if (len(data) == 6):
        # ozone monitor
        dataString = "2B-O3>"+dataString

    elif(len(data) == 14):
        # NOX monitor
        dataString = "2B-NOX>"+dataString

    elif(len(data) == 17):
        # NOX monitor
        dataString = "2B-BC>"+dataString

    else:
        print("Device not recognized!")
        ser.write("<li850><rs232><strip>true</strip></rs232></li850>".encode())
        return dataString

    dataString = "~#mints0!" + dataString
    return dataString



if __name__ == "__main__":
    import sys
    portNum = int(sys.argv[1])
    print("Num of rs232 device: {0}".format(len(devices)))
    print("monitoring device on port: {0}".format(devices[portNum]))
    readPort(devices[portNum])
