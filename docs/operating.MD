## Snow Plow General Functionality and Operability

## Quick Start Guide:
## 1. Lidar IP Configuration:
Before the lidar will function, IP configuration must be complete or the Lidar will not be able to receive packets. The current implementation 
involves using the sick_scan_xd packages that "publish" data over a ROS2 topic. This data is retrieved from the topic and used to map the snowplow to a grid. 
More or less we scan once at startup, then generate a map on an x,y and ultimately use Dijkstra's in conjunction with motor control for path planning.

To ensure proper configuration, double check the following items and run the command:

```
nc -z -v -w5 192.168.1.2 2112
```

If improperly configured, it will fail with the message Network is unreachable. No progress can be made until this connects. The configuration was saved but it does not always stay saved over extended periods of storage.

If network is unreachable view and follow the steps for IP configuration. 
-Lidar: [Lidar Overview](lidar.MD)

Otherwise proceed with:

```
# Source the environment
source /opt/ros/humble/setup.bash

# Change Directory to launch folder
cd /opt/ros/humble/share/sick_scan_xd/launch

# run sick scan
ros2 run sick_scan_xd sick_generic_caller sick_lms_5xx.launch
hostname:=192.168.1.2
```

## 2. Additional Sensor Data Publishing to ROS2 Topic:

```
# Detect which sensor maps to each dev ie ACM0, ACM1 and use the logic pathing and main.py
source /opt/ros/humble/setup.bash
python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Serial_Detect.py 

# Start the nodes with the data
source /opt/ros/humble/setup.bash
/home/jetson/Desktop/Sandbox/SnowPlow/src/Arduino_Node.py
```

 IMU: [IMU Overview](IMU.MD), Motor: [Motor Overview](motors.MD)

```
# Each data source should have a topic. Confirm data is being collected at the following locations:
# IMU = '/imu/magnetometer', GPS = '/gps_pose', Lidar = '/cloud', Motors = '/left_motor/speed', '/right_motor/speed'
source /opt/ros/humble/setup.bash
ros2 topic list
```
## 3. Start the GPS node:
GPS: [GPS Overview](GPS.MD)

Real Time Kinematic Data: Currently the Raspberry PI runs a python script that collects RTK data from a second source and pipes that back over usb to zed gps. The scripts are located in a gps folder in this repository. There are several options for this however the current implementation is this.

The Only Device that requires Wifi is the RPI.
Wifi is currently set to: Network: iBrick (2), Password: password. This can be changed to match the hotspot the team uses.

Run the desktop script that is needed. Only one should be used.

- [Ames, Iowa](../rpi/AmesCorrectionData.sh)
- [St Paul, Minnesota](../rpi/StPaulCorrectionData.sh)

Then,

```
source /opt/ros/humble/setup.bash
python3 /home/jetson/Desktop/Sandbox/SnowPlow/test/GPS_Node.py
```

## 3. Complete Any Preflight Checklists and Safety Measures:

## 4. Start the Machine:
Running In Operational Mode with Movement:
(Before running the main function, we need all sensor data publishing.)

> [!WARNING] 
> THIS COMMAND STARTS THE MOTORS.

```
# Misc Notes

# Identify device mapping and ports and log to txt file
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Serial_Detect.py
# Start the GPS
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/GPS_Node.py
# Start Arduino Node
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Arduino_Node.py
# Start Lidar
# ros2 run sick_scan_xd sick_generic_caller sick_scan_xd_test.launch

# Start the robot with actual GPS, IMU and LIDAR attached and clear view of the sky:
# Alternatively you can use startup.sh in the root directory of this repository.
# (Use This Outside Only after familiarizing yourself with the main.py script)
source /opt/ros/humble/setup.bash
python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Arduino_Node.py & python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/GPS_Node.py & ros2 run sick_scan_xd sick_generic_caller /home/jetson/Desktop/Sandbox/SnowPlow/sick_scan_xd_test.launch

# This will initialize the robot and lidar, create the object map with lidar data,
# and begin motion of the robot:
source /opt/ros/humble/setup.bash
python3 src/main.py

```
