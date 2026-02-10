# Autonomous Snowplow - GPS
## About GPS

## At a glance:

This is actual footage from our gps running on Windows. On Linux we read the data from python.

<img src="./GPSGIF.gif" width="720" height="486" />

This is sample output of longitude and latitude without RTK and default settings for U-Center.

- [Sample Output Text](../src/SampleUCenterLog.txt)

An basic example of reading from serial in python looks like this:

- [gps.py](../src/gps.py)
- [GPS Output](../src/gps.txt)

Snowplow's implementation is a little more complex. There are several methods of configuration for the Real Time Kinematic setup. One Zed-f9p is located on the snow plow. Real time kinematics involves an additional stationary gps base station that feeds correction data. This improves the accuracy to a point it is useable for competition. The normal method seen above recieves longitude and latitude but without thumbnail precision. In adding a second data source we are able to triangulate and further improve the accuracy. This is the reason the Raspberry PI is present currently. 

## Real Time Kinematic Data

Below is a picture of U-Center.

<img src="./Ublox.png" width="720" height="400" />


Below is a picture of the rpi running and aquiring rtk data.

<img src="./rpi.jpg" width="720" height="486" />

Currently the Raspberry PI runs a python script that collects RTK data from a second source and pipes that back over usb to zed gps. The scripts are located in a gps folder in this repository. There are several options for this however the current implementation is this.
The Only Device that requires Wifi is the RPI.

Wifi is currently set to: Network: iBrick (2), Password: password. This can be changed to match the hotspot the team uses.
.
- [Ames, Iowa](../rpi/AmesCorrectionData.sh)
- [St Paul, Minnesota](../rpi/StPaulCorrectionData.sh)

The RPI must be connected to a mobile hotspot on someones phone in order to be able to retrieve the correction data. Additionally one script needs to be run from the desktop. One is for Iowa and one is for Minnesota (competition location). Both scripts access publicly available gps data. Just connect to wifi and run the script. The bluetooth method has been tested but requires an app instead of a wifi hotspot.

For Registering Credentials:

[Minnesota](https://mncors.dot.state.mn.us/RegisterAccount.aspx)

Ames,IA script does not require credentials.
An easily identifiable way to ensure you are recieving RTK data is through confirmation of the lights on the device and a connection to U-Center. In U-Center (Windows) 3D/DGNSS is the desirable state. It is common to get 3D/DGNSS/Float which is less desirable. In attaching a metal plate to the underside of the GPS and configuring messages you can achieve an accuracy value in the 2d field of gps data seen in the image of ublox. In the screenshot shown it is blank.
After running the script on the raspberry pi with Ames correction data, you should be able to achieve connection to the correction data and pipe via usb to the zed-f9p. This is passed from the correction data source via internet > serial to uart >  zed f9p. There are several configuration options available including UBX-NAV-PVT. By right clicking the individual message types, you are able to disable messages and enable message types on the menu under View > Messages View. I believe this helps with validating the Real Time Kinematics and validating the accuracy. The previous team mentioned the goal being a value under 1 ie a decimal in the 2d field that can be seen in U-center. While on Snow Plow this is different because the zed is not connected to a Windows machine. In this case, the lights on the zed and the blinking light on the serial to uart can provide clues:

PWR/VIN (Power): Solid light indicates the module has power (via VIN pin or USB).

RTK: Off: No carrier solution or no RTCM corrections.

Flashing/Blinking: Receiving RTCM data (floating solution), but not a fixed solution yet.

Solid (On): RTK Fixed solution achieved (highest accuracy).

PPS (Pulse Per Second): Flashes once per second when a valid position/timing lock is achieved.

GEO (Geofence): Can be configured to indicate if the device is inside or outside a defined geofence area. 


- [RTK_Debug_Log](../logs/RTKDEBUGLOG.txt)


## The GPS used for this project is:

- [Product Specs](https://www.sparkfun.com/sparkfun-gps-rtk-sma-kit.html)

- [GPS Hookup Guide](https://learn.sparkfun.com/tutorials/gps-rtk2-hookup-guide)

- [Connect to a Correction Source](https://learn.sparkfun.com/tutorials/gps-rtk2-hookup-guide/connecting-the-zed-f9p-to-a-correction-source)

- [Setting up RTK2GO](http://rtk2go.com/how-to-connect/)

- [GPS info](http://monitor.use-snip.com/?hostUrl=rtk2go.com&port=2101)

- [Datasheet](./ZED-F9P-02B_DataSheet_UBX-21023276.pdf)

- [NMEA Sentence Structures](./NMEA_Format_v0.1.pdf)


## Our implementation and scripts that reference the GPS:

- [Schematic](./SparkFun-GPS-RTK-SMA-ZED-F9P-Schematic.pdf)

- [RobotGPS.py](../src/RobotGPS.py)

- [GPS_Node.py](../src/GPS_Node.py)

For more information see [Operating Procedure](./docs/operating.MD).

