#!/usr/bin/env python3
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict
import sys

dataFolder = mD.dataFolder
gpsPorts    =  mD.gpsPorts
baudRate    = 9600

def main(portNum):

    reader = pynmea2.NMEAStreamReader()
    ser = serial.Serial(
    port= gpsPorts[portNum],\
    baudrate=baudRate,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    print("connected to: " + ser.portstr)
    line = []
    while True:
       try:
           for c in ser.read():
               line.append(chr(c))
               if chr(c) == '\n':
                   dataString     = (''.join(line))
                   dateTime  = datetime.datetime.now()
                   if dataString.startswith("$GPGGA"):
                       mSR.GPSGPGGA2Write(dataString,dateTime)
                       lastGPGGA = time.time()
                   if dataString.startswith("$GPRMC"):
                       mSR.GPSGPRMC2Write(dataString,dateTime)
                       lastGPRMC = time.time()
                   line = []
                   break
       except:
           print("Incomplete String Read")
           line = []

    ser.close()

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    portNum = int(sys.argv[1])
    print("Number of Arduino Nano devices: {0}".format(len(gpsPorts)))
    print("Monitoring Arduino Nano on port: {0}".format(gpsPorts[portNum]) + " with baudrate " + str(baudRate))
    main(portNum)

