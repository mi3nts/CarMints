import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder  = mD.dataFolder
ozonePort    = mD.ozonePort



def main():
    if(ozonePort[0]): # make sure you can find the ozone port
        ser = serial.Serial(
            port = ozonePort[1],
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
                    dataString = "ozoneMonitor>"+dataString
                    dataString = "~#mints0!" + dataString
                    print(dataString)
                    dt = datetime.datetime.now()
                    mSR.dataSplit(dataString, dt)
                    line = []

    else:
        print("Error: Ozone Monitor not found. Check USB ports.")

if __name__ == "__main__":
   main()
