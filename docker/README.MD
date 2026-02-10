## Snow Plow Docker

## Download and install Docker Desktop:

Windows: [Docker Desktop](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module&_gl=1*cujuf*_gcl_au*MTQyMTExNjg3MS4xNzY1MjI2NTg2*_ga*MjYxNjQ2MjIzLjE3NjUyMjY1ODY.*_ga_XJWPQMJYHQ*czE3NjgyNzQ4MzAkbzIkZzEkdDE3NjgyNzgwMDIkajI4JGwwJGgw)

Linux: [Docker Desktop](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)

## Deploy Snow Plow Local

#### Build it:

Open folder 'SnowPlow' and right click open terminal

In folder: ./SnowPlowDockerized/SnowPlow/

```
docker build -t snowplow .
```

#### Deploy it:

In folder: ./SnowPlowDockerized/SnowPlow/

```
docker run -it -d -p 8080:80 --name snowplow snowplow
```

```
64daa8381517a99de0609b24fdeee0b8c07c5a8475c689e9e18cbefe9116fac2
...SnowPlowDockerized\SnowPlow> docker ps
CONTAINER ID   IMAGE      COMMAND                  CREATED         STATUS         PORTS                                     NAMES
64daa8381517   snowplow   "/ros_entrypoint.sh …"   6 seconds ago   Up 5 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   snowplow
...Sandbox\SnowPlowDockerized\SnowPlow>
```

#### Use it:

```
docker exec -it snowplow /bin/bash
```

```
cd /home/jetson/Desktop/Sandbox
ls
```
Shows the contents of our github repository:

or start using ros2 commands:

```
# Sources the environment
source /opt/ros/humble/setup.bash
# Lists the topics
ros2 topic list
```



Produces:

```
/home/jetson/Desktop/Sandbox# ros2 topic list
/parameter_events
/rosout
```

Below Example is for starting dummy nodes and then running the prior teams implementation of ROS2. 

TODO:
Update the stream of info coming from sensors to ensure they publish data correctly to the topic/node that the main pathing logic references. These references are contained in main.py and the scripts it uses. All are located in the src folder of the prior years git.

```
source /opt/venv/bin/activate
cd Originals/PriorYear/
nohup ros2 run gps_package gps_node &
nohup ros2 run imu_package imu_node &
python3 main.py
```

This container is a fully sourced demo of the snowplow framework. 

It contains:

ros-humble-desktop, ros-humble-control, ros-humble-ros2-control, ros-humble-moveit, ros-humble-ros-ign, ros-humble-joint-state-publisher-gui, ros-humble-kinematics-interface-kdl, ros-humble-rqt-joint-trajectory-controller, ros-humble-navigation2, ros-humble-nav2-bringup, ros-humble-sick-scan-xd

All nodes and topics are pre-configured with dummy data showing examples of: GPS, IMU, Lidar, Magnetometer and RC Controller.

#### Remove it:
When you are done:

List active containers:

```
docker ps
```

Locate the container name and kill:

```
docker kill f12a459ae0cb
```

Verify no containers running:

```
docker ps
```


