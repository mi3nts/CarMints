#!/usr/bin/env python3
import time
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder  = mD.dataFolder
partectorPort    = mD.partectorPort
print(partectorPort[1])

def main():
    if(partectorPort[0]):
        ser = serial.Serial(
            port = partectorPort[1],
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0)

        print("Connection successful!")
        time.sleep(5)
        line = []
        while True:
            try:
                for c in ser.read():
                    line.append(chr(c))
                    if(chr(c)=='\n'):
                        dataString     = (''.join(line))
                        # get rid of end line and carriage return characters if they exist
                        dataString = dataString.replace('\n', '')
                        dataString = dataString.replace('\r', '')
                        dt = datetime.datetime.now()
                        mSR.partectorWrite(dataString, dt)
                        line = []
            except:
                print("Incomplete string read. Something may be wrong with the Partector")
                line = []
if __name__ == "__main__":
    main()
