#!/bin/bash
#
sleep 60
python3 rs232monitor.py 0 &
sleep 5
python3 rs232monitor.py 1 &
sleep 5
python3 rs232monitor.py 2 &
