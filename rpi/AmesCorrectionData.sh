#!/usr/bin/env bash

SERIAL_PORT="/dev/ttyUSB0"

while ! [ -c "$SERIAL_PORT" ]; do
	echo "Error: Serial port not found"
	sleep 1	
done

echo "Serial port found"

str2str -in ntrip://ISU_Robotics:robotrobot@165.206.203.10:10000/RTCM3_NEAR -out serial://ttyUSB0:9600:8:n:1 -n 10000 -p 42.02098600 -93.64804333 270.600


