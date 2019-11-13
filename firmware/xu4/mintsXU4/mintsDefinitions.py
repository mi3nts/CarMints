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
            return True,p[0] # if it's there, return true and the port location ex: /dev/ttyUSB0

    return False, "xxx";



# NOTE: this is my hokey fix to deal with devices that need to use RS232 - USB Converters since
#       they all have the same UBS VID
#
#       Linux users can see attached usb devices using the lsusb command in the terminal
def findRS232Devices():
    ports = list(serial.tools.list_ports.comports())
    devices = [] # list to hold all ports using RS232-USB Converter
    for p in ports:
        currentPort = str(p[2]) # get the USB VID
        if(currentPort.find("PID=067b")):
            devices.append(p[0])
    return devices


def findLicorCO2H20Port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p[2]) # check for unique USB VID
        if(currentPort.find("PID=0a07")):
            print("Found")
            return True, p[0]


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

rs232_devices         = findRS232Devices()

licorPort             = findLicorCO2H20Port()

if __name__ == "__main__":
    # the following code is for debugging
    # to make sure everything is working run python3 mintsDefinitions.py 

    print("dataFolder: {0}".format(dataFolder))
    print("ozonePort: {0}".format(ozonePort))
    print("latestOff: {0}".format(latestOff))
    print("gpsPort: {0}".format(gpsPort))
    #-------------------------------------------#
    print("RS232 Devices:")
    for dev in rs232_devices:
        print("\t{0}".format(dev))

    print("Licor Port: {0}".format(licorPort))
























