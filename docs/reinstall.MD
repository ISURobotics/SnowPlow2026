## Installation:

In the event of a need for a complete reinstallation, the following process should help.

## Jetson Installation

The Jetson Nano getting started guide is located here: [Getting Started with the Jetson Nano](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)

## Ros2 Installation:

Upon successful installation of 22.04 for Jetson, proceed to the ROS2 humble installation:

- [ROS2](https://docs.ros.org/en/humble/Installation.html) 
- Go through talker and listener to confirm ROS2 install is complete.

## Clone this repository:
- Create a folder on the desktop named 'Sandbox' and clone this repository into it. This will maintain the file structure written into many of the scripts.

## Configure permissions:
 - Configure dialout group and pip install serial, pyserial etc. to confirm you can read over usb.
 - Useful commands are as follows:

```
sudo adduser $USER dialout
```


## GPS Installation

 Most configuration for the GPS is completed in the U-Center software on a windows machine.

 For GPS Info: [Global Positioning System](./docs/GPS.MD)

## Lidar Installation
Connect the lidar to a 24v power supply and attach the ethernet.
To ensure proper configuration:

```
nc -z -v -w5 192.168.1.2 2112
```

If the IP address is improperly configured, it will fail with the message Network is unreachable. No progress can be made until the connection can be established.

### Installation is: 

```
sudo apt update
sudo apt-get install ros-humble-sick-scan-xd
```

Quick Start Guide:
##### 1. IP Configuration Must Be Completed First:
Set IP for Lidar through Sopas on Windows to 192.168.1.2

##### 2. Set IP for Jetson nano and disable WiFi. On Jetson, terminal command: 

```
ifconfig 
# Produces the following output:
enP8p1s0:Realtek Semiconductor Co.\, Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller
wlP1p1s0:Realtek Semiconductor Co.\, Ltd. RTL8822CE 802.11ac PCIe Wireless Network Adapter
# Look through devices for ID of Ethernet
enP8p1s0
ifconfig enP8p1s0
nmcli con add con-name "static-enP8p1s0" ifname enP8p1s0 type ethernet ip4 192.168.1.1/16 gw4 192.168.1.1
nmcli con up "static-enP8p1s0"
```

See More at: [Lidar](lidar.MD)

## Motor Arduino Installation

 - Upload Arduino sketch via Arduino IDE using the Motor.ino sketch

```
# ACM port is detected on plug in and will most likely be in 0-2 range unless replugging devices
# using the correct ACM port cat the line like this:
cat /dev/ttyACM0 > output.txt
# or 
cat /dev/ttyACM0
# Do this to confirm data is being read
```

## IMU Arduino Installation

 - Upload Arduino sketch via Arduino IDE using the IMU.ino sketch

```
# ACM port is detected on plug in and will most likely be in 0-2 range unless replugging devices
# using the correct ACM port cat the line like this:
cat /dev/ttyACM0 > output.txt
# or 
cat /dev/ttyACM0
# Do this to confirm data is being read

```


