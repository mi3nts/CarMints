#!/bin/bash
#
# note, rs232monitor.py uses command line flag to specify
# rs232 device.
#
#
sleep 120
python3 rs232monitor.py 0 &
sleep 5
python3 rs232monitor.py 1 &
sleep 5
python3 rs232monitor.py 2 &
sleep 5
python3 licorMonitor.py &
# sleep 5
# python3 GPSReader.py
