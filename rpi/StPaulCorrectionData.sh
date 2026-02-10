#!/usr/bin/env bash

SERIAL_PORT="/dev/ttyUSB0"

while ! [ -c "$SERIAL_PORT" ]; do
	echo "Error: Serial port not found"
	sleep 1	
done

echo "Serial port found"

str2str -in "ntrip://IowaSU/RyanM:robotrobot@mncors.dot.state.mn.us:9000/RTCM_32_NAD83(2011)" -out serial://ttyUSB0:9600:8:n:1 -n 10000 -p 44.97316528 -93.29112555 250.000


