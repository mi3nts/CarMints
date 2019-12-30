#!/usr/bin/env python3
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict


dataFolder = mD.dataFolder
# duePort    = mD.duePort
gpsPort    =  mD.gpsPort
#




def main():

    reader = pynmea2.NMEAStreamReader()
    ser = serial.Serial(
    port= gpsPort,\
    baudrate=9600,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    lastGPRMC = time.time()
    lastGPGGA = time.time()


    delta  = 2
    print("connected to: " + ser.portstr)

    #this will store the line
    line = []
    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                if chr(c) == '\n':
                    dataString     = (''.join(line))
                    dateTime  = datetime.datetime.now()
                    if (dataString.startswith("$GPGGA") and mSR.getDeltaTime(lastGPGGA,delta)):
                        mSR.GPSGPGGA2Write(dataString,dateTime)
                        lastGPGGA = time.time()
                    if (dataString.startswith("$GPRMC") and mSR.getDeltaTime(lastGPGGA,delta)):
                        mSR.GPSGPRMC2Write(dataString,dateTime)
                        lastGPRMC = time.time()
                    line = []
                    break
        except:
            print("Incomplete String Read")
            line = []

    ser.close()



if __name__ == "__main__":
   main()
