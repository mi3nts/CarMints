from getmac import get_mac_address
import serial.tools.list_ports

def findPort(find):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p)
        if(currentPort.endswith(find)):
            return(currentPort.split(" ")[0])


def findOzonePort():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p[2]) # get the USB VID
        outPort   =  str(p)
        print(currentPort)
        if(currentPort.find("PID=067B")>=0): # check the USB VID to make sure it's the ozone sensor
            print("Found")
            return True,p[0]; # if it's there, return true and the port location ex: /dev/ttyUSB0

    return False, "xxx";



def findMacAddress():
    macAddress= get_mac_address(interface="eth0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="docker0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp1s0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    return "xxxxxxxx"



dataFolder            = "/home/teamlary/mintsData/raw"
ozonePort             = findOzonePort()
macAddress            = findMacAddress()

latestOff             = True
gpsPort               = findPort("GPS/GNSS Receiver")


if __name__ == "__main__":
    print("dataFolder: {0}".format(dataFolder))
    print("ozonePort: {0}".format(ozonePort))
    print("latestOff: {0}".format(latestOff))
    print("gpsPort: {0}".format(gpsPort))




























