#!/usr/bin/env python3
import time
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder  = mD.dataFolder
licorPort    = mD.licorPort
print(licorPort[1])

def main():
    if(licorPort[0]):
        ser = serial.Serial(
            port = licorPort[1],
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0)

        print("Connection successful!")
        ser.write("<li850><rs232><strip>true</strip></rs232></li850>".encode('utf-8'))
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
                        dataString = "~#mints0!LICOR>" + dataString
                        dt = datetime.datetime.now()
                        print(dataString)
                        mSR.dataSplit(dataString, dt)
                        line = []
            except:
                print("Incomplete string read. Something may be wrong with the Licor sensor")
                line = []
if __name__ == "__main__":
    main()



