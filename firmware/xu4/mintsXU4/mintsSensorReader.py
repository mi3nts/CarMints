import serial
import datetime
import os
import csv
from mintsXU4 import mintsDefinitions as mD
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import math

dataFolder    = mD.dataFolder
macAddress    = mD.macAddress
latestOff     = mD.latestOff


def dataSplit(dataString,dateTime):
    dataOut   = dataString.split('!')
    if(len(dataOut) == 2):
        tag       = dataOut[0]
        dataQuota = dataOut[1]
        sensorSplit(dataQuota,dateTime)



def sensorSplit(dataQuota,dateTime):
    dataOut    = dataQuota.split('>')
    if(len(dataOut) == 2):
        sensorID   = dataOut[0]
        sensorData = dataOut[1]
        sensorSend(sensorID,sensorData,dateTime)






def sensorFinisher(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    print(writePath)
    if(not(latestOff)):
       mL.writeHDF5Latest(writePath,sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    print(sensorDictionary)




def sensorFinisherIP(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePathIP(sensorName,dateTime)
    exists = directoryCheck(writePath) 
    writeCSV2(writePath,sensorDictionary,exists)
    print(writePath)
    if(not(latestOff)):
       mL.writeHDF5Latest(writePath,sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    print(sensorDictionary)



def sensorSend(sensorID,sensorData,dateTime):
    if(sensorID=="2B-O3"):
        ozoneMonitorWrite(sensorData,dateTime)
    if(sensorID=="2B-NOX"):
        noxMonitorWrite(sensorData, dateTime)
    if(sensorID=="2B-BC"):
        blackCarbonMonitorWrite(sensorData, dateTime)
    if(sensorID=="LICOR"):
        licorMonitorWrite(sensorData, dateTime)
    



# 2B Technologies Ozone Monitor
def ozoneMonitorWrite(sensorData, dateTime):
    dataOut = sensorData.split(',')
    sensorName = "2B-O3"
    dataLength = 5 # the ozone monitor outputs additional date and time making total length 6
    if(len(dataOut) == (dataLength + 1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("ozone"  ,dataOut[0]), #
            	("temperature"     ,dataOut[1]),
                ("pressure"     ,dataOut[2]),
            	("voltage"     ,dataOut[3]),
            	("sensorTime"     ,(str(dataOut[4])+','+str(dataOut[5]).replace('\r', '')) ),
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def noxMonitorWrite(sensorData, dateTime):
    dataOut = sensorData.split(',')
    sensorName = "2B-NOX"
    dataLength = 13  # total length is 14 but data and time are separate outputs
    if(len(dataOut) == (dataLength + 1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("NO2"  ,dataOut[0]),
        		("NO"  ,dataOut[1]),
        		("NOX"  ,dataOut[2]),
        		("temperature"  ,dataOut[3]),
        		("pressure"  ,dataOut[4]),
        		("flow"  ,dataOut[5]),
        		("O3-flow"  ,dataOut[6]),
        		("voltage"  ,dataOut[7]),
        		("O3-voltage"  ,dataOut[8]),
        		("scrubber-temperature"  ,dataOut[9]),
        		("error-byte"  ,dataOut[10]),
        		("sensorTime"  ,dataOut[11]),
        		("status"  ,dataOut[13].replace('\r', '')),
            	("sensorTime"     ,(str(dataOut[11])+','+str(dataOut[12])) ),
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)
 
def blackCarbonMonitorWrite(sensorData, dateTime):
    dataOut = sensorData.split(',')
    sensorName = "2B-BC"
    dataLength = 15  # total length is 17 but data and time are separate outputs and the first entry is just hte log number
    if(len(dataOut) == (dataLength + 2)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("Extinction-880nm"  ,dataOut[1]),
        		("Extinction-405nm"  ,dataOut[2]),
        		("BC"  ,dataOut[3]),
        		("PM"  ,dataOut[4]),
        		("temperature"  ,dataOut[5]),
        		("pressure"  ,dataOut[6]),
        		("humidity"  ,dataOut[7]),
        		("flow-temperature"  ,dataOut[8]),
        		("voltage-880nm"  ,dataOut[9]),
        		("voltage-405nm"  ,dataOut[10]),
        		("current-405nm"  ,dataOut[13]),
        		("current-405nm"  ,dataOut[14]),
        		("status"  ,dataOut[15].replace('\r', '')),
            	("sensorTime"     ,(str(dataOut[11])+','+str(dataOut[12])) ),
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def licorMonitorWrite(sensorData, dateTime):
    dataOut = sensorData.split(' ') # space separated, NOT comma separated
    sensorName = "LICOR"
    sensorDictionary = OrderedDict([
        ("dateTime", str(dateTime)),
        ("cellTemp", dataOut[0]),
        ("cellPressure", dataOut[1]),
        ("CO2", dataOut[2]),
        ("CO2_abs", dataOut[3]),
        ("H2O", dataOut[4]),
        ("H2O_abs", dataOut[5]),
        ("H2O_dewpoint", dataOut[6]),
        ("ivolt", dataOut[7]),
        ("CO2_raw", dataOut[8]),
        ("CO2_raw_ref", dataOut[9]),
        ("H2O_raw", dataOut[10]),
        ("H2O_raw_ref", dataOut[11]),
    ])
    if len(dataOut) == 13:
        sensorDictionary["flowrate"] = dataOut[12]

    sensorFinisher(dateTime, sensorName, sensorDictionary)



#-----------------GPS CODE-------------------------------------

def getDeltaTime(beginTime,deltaWanted):
    return (time.time() - beginTime)> deltaWanted



def getLatitudeCords(latitudeStr,latitudeDirection):
    print(latitudeStr)
    latitude = float(latitudeStr)
    latitudeCord      =  math.floor(latitude/100) +(latitude - 100*(math.floor(latitude/100)))/60
    if(latitudeDirection=="S"):
        latitudeCord = -1*latitudeCord
    return latitudeCord

def getLongitudeCords(longitudeStr,longitudeDirection):
    longitude = float(longitudeStr)
    longitudeCord      =  math.floor(longitude/100) +(longitude - 100*(math.floor(longitude/100)))/60
    if(longitudeDirection=="W"):
        longitudeCord = -1*longitudeCord
    return longitudeCord

def GPSGPGGAWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	     ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def GPSGPGGA2Write(dataString,dateTime):
    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    latitudeCordinate = getLatitudeCords(sensorData.lat,sensorData.lat_dir)

    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA2"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitudeCoordinate" ,getLatitudeCords(sensorData.lat,sensorData.lat_dir)),
                ("longitudeCoordinate",getLongitudeCords(sensorData.lon,sensorData.lon_dir)),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPSGPRMCWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.status=='A'):
        sensorName = "GPSGPRMC"
        sensorDictionary = OrderedDict([
                ("dateTime"             ,str(dateTime)),
                ("timestamp"            ,sensorData.timestamp),
                ("status"               ,sensorData.status),
                ("latitude"             ,sensorData.lat),
                ("latitudeDirection"    ,sensorData.lat_dir),
                ("longitude"            ,sensorData.lon),
                ("longitudeDirection"   ,sensorData.lon_dir),
                ("speedOverGround"      ,sensorData.spd_over_grnd),
                ("trueCourse"           ,sensorData.true_course),
                ("dateStamp"            ,sensorData.datestamp),
                ("magVariation"         ,sensorData.mag_variation),
                ("magVariationDirection",sensorData.mag_var_dir)
                 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPSGPRMC2Write(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.status=='A'):
        sensorName = "GPSGPRMC2"
        sensorDictionary = OrderedDict([
                ("dateTime"             ,str(dateTime)),
                ("timestamp"            ,sensorData.timestamp),
                ("status"               ,sensorData.status),
                ("latitudeCoordinate"    ,getLatitudeCords(sensorData.lat,sensorData.lat_dir)),
                ("longitudeCoordinate"   ,getLongitudeCords(sensorData.lon,sensorData.lon_dir)),
                ("latitude"             ,sensorData.lat),
                ("latitudeDirection"    ,sensorData.lat_dir),
                ("longitude"            ,sensorData.lon),
                ("longitudeDirection"   ,sensorData.lon_dir),
                ("speedOverGround"      ,sensorData.spd_over_grnd),
                ("trueCourse"           ,sensorData.true_course),
                ("dateStamp"            ,sensorData.datestamp),
                ("magVariation"         ,sensorData.mag_variation),
                ("magVariationDirection",sensorData.mag_var_dir)
                 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)


#-----------------GPS CODE-------------------------------------







def writeCSV2(writePath,sensorDictionary,exists):
    keys =  list(sensorDictionary.keys())
    with open(writePath, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # print(exists)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)



def getWritePathIP(labelIn,dateTime):
    #Example  : MINTS_0061.csv
    writePath = dataFolder+"/"+macAddress+"/"+"MINTS_"+ macAddress+ "_IP.csv"
    return writePath;


def getWritePathSnaps(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/snaps/MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) + "_" +str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2)+ "_" +str(dateTime.second).zfill(2) +".png"
    return writePath;



def getWritePath(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) +".csv"
    return writePath;

def getListDictionaryFromPath(dirPath):
    print("Reading : "+ dirPath)
    reader = csv.DictReader(open(dirPath))
    reader = list(reader)

def fixCSV(keyIn,valueIn,currentDictionary):
    editedList       = editDictionaryList(currentDictionary,keyIn,valueIn)
    return editedList

def editDictionaryList(dictionaryListIn,keyIn,valueIn):
    for dictionaryIn in dictionaryListIn:
        dictionaryIn[keyIn] = valueIn

    return dictionaryListIn

def getDateDataOrganized(currentCSV,nodeID):
    currentCSVName = os.path.basename(currentCSV)
    nameOnly = currentCSVName.split('-Organized.')
    dateOnly = nameOnly[0].split(nodeID+'-')
    print(dateOnly)
    dateInfo = dateOnly[1].split('-')
    print(dateInfo)
    return dateInfo


def getFilePathsforOrganizedNodes(nodeID,subFolder):
    nodeFolder = subFolder+ nodeID+'/';
    pattern = "*Organized.csv"
    fileList = [];
    for path, subdirs, files in os.walk(nodeFolder):
        for name in files:
            if fnmatch(name, pattern):
                fileList.append(os.path.join(path, name))
    return sorted(fileList)


def getLocationList(directory, suffix=".csv"):
    filenames = listdir(directory)
    dateList = [ filename for filename in filenames if filename.endswith( suffix ) ]
    return sorted(dateList)


def getListDictionaryCSV(inputPath):
    # the path will depend on the node ID
    reader = csv.DictReader(open(inputPath))
    reader = list(reader)
    return reader

def writeCSV(reader,keys,outputPath):
    directoryCheck(outputPath)
    csvWriter(outputPath,reader,keys)

def directoryCheck(outputPath):
    exists = os.path.isfile(outputPath)
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
    return exists

def csvWriter(writePath,organizedData,keys):
    with open(writePath,'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(organizedData)


def gainDirectoryInfo(dailyDownloadLocation):
    directoryPaths = []
    directoryNames = []
    directoryFiles = []
    for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
        directoryPaths.extend(dirpath)
        directoryNames.extend(dirnames)
        directoryFiles.extend(filenames)

    return directoryPaths,directoryNames,directoryFiles;
