## Autonomous Snowplow - Pathing
## About Pathing

This represents the general mapping logic:

Pathing utilizes almost all files in the src folder. The logic is based on [Dijkstras](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) which calculates the corners of the map and plots the shortest path through those eight points while detecting any cones and labeling them as obstacles that need to be avoided. The corners are labeled as start1, end1, end2...end7. 

Prior team note:
"The basic concept is that x is the direction the robot is facing when the script starts. The height of the cone's bounding box is the distance from the cone edge to the edge of the bounding box."

There are cone height and width variables declared for adjusting the parameter.

[main.py](../src/main.py)

This logic is dependent on data recieved from the sensors via the following files:

```
# Identify device mapping and ports and log to txt file
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Serial_Detect.py
# Start the GPS
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/GPS_Node.py
# Start Arduino Node
# python3 /home/jetson/Desktop/Sandbox/SnowPlow/src/Arduino_Node.py
# Start Lidar
# ros2 run sick_scan_xd sick_generic_caller sick_scan_xd_test.launch
```
This sensor data is funneled to [main.py](../src/main.py).

If you think of a 1 x 2 piece of paper driving around a large piece 8.5 x 11 paper (map) placed underneath. The axis of the smaller paper (representing the snowplow) will change everytime the plow turns. This should help with visualization of the transforms.  Logical next steps might include organization of the topics and nodes and completing the port to NAV2. This would involve implementing the logic currently contained in main.py. Previous versions of snow plow used hector slam for navigation which is deprecated as of ROS2 humble and the team briefly discussed a transition to [Nav2](https://docs.nav2.org/getting_started/index.html). A test bench has been established that allows the team to quickly deploy ros2 in a dockerized container and test logic without needing to be on campus or connect hardware. The container install ros2-humble, nav2, and this git to a dockerized container. If time permits, it would be nice to add end points for dummy data. Examples of data retrieved from our devices are located in this repository.


For more information see [Operating Procedure](./docs/operating.MD).
