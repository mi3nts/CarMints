#!/bin/bash
#
# note, rs232monitor.py uses command line flag to specify
# rs232 device.
#
#

sleep 120

# RS232 Readers

if pgrep -f 'python3 rs232monitor.py 0' > /dev/null
then
    exit
else
    python3 rs232monitor.py 0 &
    sleep 5
fi

if pgrep -f 'python3 rs232monitor.py 1' > /dev/null
then
    exit
else
    python3 rs232monitor.py 1 &
    sleep 5
fi

if pgrep -f 'python3 rs232monitor.py 2' > /dev/null
then
    exit
else
    python3 rs232monitor.py 2 &
    sleep 5
fi

#GPS Readers
if pgrep -f 'python3 GPSReaderRaw.py 2' > /dev/null
then
    exit
else
    python3 GPSReaderRaw.py 2 &
    sleep 5
fi

if pgrep -f 'python3 GPSReader1.py 1' > /dev/null
then
    exit
else
    python3 GPSReader1.py 1 &
    sleep 5
fi

if pgrep -f 'python3 GPSReader2.py 0' > /dev/null
then
    exit
else
    python3 GPSReader2.py 0 &
    sleep 5
fi


if pgrep -f 'python3 licorMonitor.py' > /dev/null
then
    exit
else
    python3 licorMonitor.py &
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



