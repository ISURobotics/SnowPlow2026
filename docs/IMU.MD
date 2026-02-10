## Autonomous Snow Plow - IMU (Gyro)
The Snow Plow currently has multiple IMU. We use a separate BNO055 as opposed to the IMU in the Sick Scan Lidar currently. The details of the wiring can be found in the [wiring diagram](assembly.MD). If the sketch is uploaded and the wires are connected to the correct place then the sensor scripts will recognize the device. The IMU is wired to an ardruino via jumper wires and the arduino is connected via usb to the Jetson. The serial detect script detects each usb device and maps them into the logic for the pathing. It is important that the usb and sensors be connected before powering on the Snow Plow and that the Serial_ Detect.py is run before proceeding further.

[Inertial Measurement Unit Data Sheet](./adafruit-bno055-absolute-orientation-sensor.pdf)

Currently we use the roll pitch and yaw values from the gyro read over serial.

```
# Set baud and scan
# Scan the appropriate port to ensure communication via serial
stty -F /dev/ttyUSB0 115200
cat /dev/ttyUSB0

# Detect which sensor maps to each dev ie ACM0, ACM1 and use the logic pathing and main.py
source /opt/ros/humble/setup.bash
python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Serial_Detect.py 

# Each data source should have a topic. Confirm data is being collected at the following locations:
IMU = '/imu/magnetometer'

# Starting Arduino_Node.py after running serial detect prepares this for main.py
python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Arduino_Node.py

source /opt/ros/humble/setup.bash
ros2 topic list
```

For more information see [Operating Procedure](./docs/operating.MD).
