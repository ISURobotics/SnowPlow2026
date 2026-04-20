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
