
## Install Oracle Virtual Box
When configuring use ubuntu 22.04, ensure to set user name and vm name to jetson. 
Check the box for Install guest additions to be able to enable copy and paste functionality.

## For virtual machine we need this to access sudo. 
This is not needed on Jetson installations as sudo is available by default. After setting up the oracle vm with ubuntu 22.04, decline the update to 24.04. Open terminal and enable sudo:
su -
nano /etc/sudoers

```
su -
```
```
usermod -a -G sudo jetson
nano /etc/sudoers
```
add the following:
```
jetson ALL=(ALL:ALL) ALL
```
[CTRL]+[x] to write out. [Y] to confirm.

Close the terminal and open a new one not in sudo mode.
## If reinstalling on the jetson baremetal, you can use this:
```
### can be used for easy QoL items such as browswer and ide of choice.
# wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash
```

## The following can be exectuted from a terminal to install the dependencies for ROS 2 / Nav 2
```
sudo apt-get update
sudo apt-get upgrade -y


# Installs ROS2
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale  # verify settings
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update
sudo apt upgrade-y
sudo apt install ros-humble-desktop
sudo mkdir -p /home/jetson/Desktop/ros2_ws/src/
cd /home/jetson/Desktop/ros2_ws/src/
sudo apt-get update && sudo apt-get install git -y
sudo apt-get update && sudo apt-get install python3-colcon-common-extensions -y
sudo rm -rf /var/lib/apt/lists/*

# Create some folders for our files.
sudo mkdir -p /home/jetson/Desktop/Sandbox/
git clone https://github.com/ISURobotics/SnowPlow2026 /home/jetson/Desktop/Sandbox/  
cp src /home/jetson/Desktop/ros2_ws/src/

# Get some stuff, env, python etc.
sudo apt-get update && apt-get install git -y
sudo apt-get update && apt-get install wget -y
sudo apt-get update && apt-get install curl -y
sudo apt-get update && apt-get install python3-pip -y
sudo apt-get update && apt-get install software-properties-common -y
sudo apt-get update && apt-get install ros-dev-tools -y
sudo rm -rf /var/lib/apt/lists/*
. /opt/venv/bin/activate && pip install jinja2 typeguard numpy ros2_numpy pandas matplotlib setuptools==58.2.0 colcon-common-extensions numpy
sudo apt-get update
sudo apt-get install -y

# More Ros2 stuff. See Nav2 video series on youtube.
sudo apt-get install ros-humble-desktop -y
sudo apt-get install ros-humble-control* -y
sudo apt-get install ros-humble-ros2-control* -y
sudo apt-get install ros-humble-moveit* -y
sudo apt-get install ros-humble-ros-ign* -y
sudo apt-get install ros-humble-joint-state-publisher-gui -y
sudo apt-get install ros-humble-kinematics-interface-kdl -y
sudo apt-get install ros-humble-rqt-joint-trajectory-controller -y
sudo apt-get install ~nros-humble-rqt* -y
sudo apt-get install ignition-fortress -y
sudo apt-get update
sudo apt-get install curl lsb-release gnupg
rm -rf /var/lib/apt/lists/* -y
apt-get update && apt-get upgrade -y
apt autoremove -y
echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc
sudo rosdep fix-permissions -y
rosdep update -y
apt install ros-humble-navigation2 -y
apt install ros-humble-nav2-bringup -y
apt update -y
apt-get install ros-humble-sick-scan-xd -y  
apt update -y
apt-get install nano -y

# Close terminal and open a new one. This time not as root. 
# ROS2 humble should be sourced. We can test a few commands.

ros2 topic list
ros2 pkg list
ros2 run rviz2 rviz2
```
## This should give a good starting place for working with the ROS 2 / Nav 2 Stack.