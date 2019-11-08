import serial
import datetime
import os
import csv
import deepdish as dd
from mintsXU4 import mintsDefinitions as mD
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import netifaces as ni
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
