#!/bin/bash
#
# note, rs232monitor.py uses command line flag to specify
# rs232 device.
#
#
sleep 120
if -z ps aux | grep 'rs232monitor.py 0'
then
    exit
else
    python3 rs232monitor.py 0 &
    sleep 5
fi

if -z ps aux | grep 'rs232monitor.py 1'
then
    exit
else
    python3 rs232monitor.py 1 &
    sleep 5
fi

if -z ps aux | grep 'rs232monitor.py 2'
then
    exit
else
    python3 rs232monitor.py 2 &
    sleep 5
fi

if -z ps aux | grep 'licorMonitor.py'
then
    exit
else
    python3 licorMonitor.py &
    sleep 5
fi

if -z ps aux | grep 'GPSReader.py'
then
    exit
else
    python3 GPSReader.py &
    sleep 5
fi


# Old Version
# python3 rs232monitor.py 0 &
# sleep 5
# python3 rs232monitor.py 1 &
# sleep 5
# python3 rs232monitor.py 2 &
# sleep 5
# python3 licorMonitor.py &
# sleep 5
# python3 GPSReader.py



