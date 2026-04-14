# main_program.py
import pathing
# Used to enable/disable main loop [1 = Manual Drive, 2 = Autonomous Mode]
control_mode = 1
# Used to enable/disable main loop [0 = Serial Read to Vals, 1 = Ros topics on]
ros_toggle = 0
command_direction = "Forward"

# This value is set at
lidar_thinks_I_am_here = [0,0]
# This value is set at
imu_and_gps_think_I_am_here = [0,0]
cone1degrees=0
cone1hypotenuse=0
cone2degrees=0
cone2hypotenuse=0
cone3degrees=0
cone3hypotenuse=0

# degrees between -90 and positive 90. Straight forward is 0. hypotenuse represents distance to cone.
cones_are_at=[[cone1degrees,cone1hypotenuse],[cone2degrees,cone2hypotenuse],[cone3degrees,cone3hypotenuse]]

#####################################################################################################################
# Full testing of this code requires that ROS2 be running on the network. In it's fully enabled version,
# it reads from a controller, applies mathematical functions and broadcasts the motor position in an array.
# If enabled, this would start motor movement. To prevent unexpected movement, portions are disabled by default.
# A message is displayed to show that the micro_service.py file is connected. It can be modded at the respective file location.
# This program has been implemented as microservices. Examples of this are in the below paragraph.
# It is able to broadcast data via ROS topic or log to websocket. The format used was the standardized format we use with NVIDIA
# frameworks: When sending a packet to isaac sim all motor positions are sent in a standard array format in degrees:
# [j0,j1,j2,...]. When using sensors a second packet is created and can be published to ROS2 topic as well as logged to a file
# for publishing to websocket. In many cases Data is "returned" for immediate use and pushed to ROS for use in Isaac Simulator.
# This initial portion of the code handles reading from controller and getting data to ROS2.
# This currently requires ROS2 running on the local network. Bridge to API to follow.
#####################################################################################################################

# Used to organize detected sensors
sensor_array = [0,0,0,0,0,0,0]

simple_map = [
    ['###', '##', '##','##', '##', '##', '##','##', '##', '##', '##', '##', '##', '##','##', '##', '##', '##', '##','##', '##', '##', '###'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['|| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '| ', '||'],
    ['###', '##', '##','##', '##', '##', '##','##', '##', '##', '##', '##', '##', '##','##', '##', '##', '##', '##','##', '##', '##', '###']
]
# y,x
current_position = (10 , 10)

# Using Limit Configuration:
if __name__ == '__main__':
    while control_mode == 1:

    # Scan Sensors
        # sensors_connect.scanLidar()
        # cones_are_at = sensors_connect.scanLidar
        # update lidar_thinks_I_am_here = [0, 0]
        # update cone_location_array

        # sensors_connect.scanGPS()
        # sensors_connect.scanIMU()
        # update imu_and_gps_think_I_am_here = [0, 0]


    # Check Status for safety and other logic
        #checkTriggered.aware()

        pathing.display_map(simple_map, current_position)

        # Get user input (requires pressing Enter)
        command = input().strip().lower()

        if command == 'q':
            break
        command_direction = command
        new_position = pathing.move(simple_map, current_position, command)
        if new_position != current_position:
            current_position = new_position

    # Write to Motors:

    #     write me later
    #     motors_connect.writeMotors()
