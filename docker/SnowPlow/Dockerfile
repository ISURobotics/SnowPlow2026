# Used Humble Base
FROM ros:humble

# Set Working Directory
WORKDIR /home/jetson/Desktop/ros2_ws/src/

# Install Dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Create The Directory
RUN mkdir -p /home/jetson/Desktop/Sandbox/

# Clone The Repo
RUN git clone https://github.com/ISURobotics/SnowPlow2026 /home/jetson/Desktop/Sandbox/
COPY src /home/jetson/Desktop/ros2_ws/src/

# Install Dependencies
RUN apt-get update && apt-get install -y \
    git wget curl python3-pip software-properties-common ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python Packages
RUN pip3 install --no-cache-dir setuptools==58.2.0 colcon-common-extensions numpy

# Add Gazebo Repository
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install ROS2 Packages
RUN apt-get update && apt-get install -y \
    ros-humble-desktop \
    ros-humble-control* \
    ros-humble-ros2-control* \
    ros-humble-moveit* \
    ros-humble-ros-ign* \
    ros-humble-joint-state-publisher-gui \
    ros-humble-kinematics-interface-kdl \
    ros-humble-rqt-joint-trajectory-controller \
    ~nros-humble-rqt* \
    ignition-fortress \
    && rm -rf /var/lib/apt/lists/*

# Update & Upgrade
RUN apt-get update && apt-get upgrade -y

# Used To Ensure Environment Is Sourced Every Time
RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc
RUN rosdep update

# Install Nav2
RUN sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3* -y
RUN sudo apt update

# Install Sick Scan Driver With Ros2 Support
RUN apt-get install ros-humble-sick-scan-xd -y
RUN sudo apt update

# Install IDE
RUN apt-get install nano

# Build GPS Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name gps_node gps_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/gps_node.py /home/jetson/Desktop/ros2_ws/src/gps_package/gps_package/gps_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/gps_package/gps_package/gps_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/gps_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/gps_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/gps_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/gps_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/gps_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build Dummy GPS Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name dummy_gps_node dummy_gps_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_gps_node.py /home/jetson/Desktop/ros2_ws/src/dummy_gps_package/dummy_gps_package/dummy_gps_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_gps_package/dummy_gps_package/dummy_gps_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_gps_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_gps_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_gps_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_gps_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/dummy_gps_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build IMU Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name imu_node imu_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/imu_node.py /home/jetson/Desktop/ros2_ws/src/imu_package/imu_package/imu_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/imu_package/imu_package/imu_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/imu_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/imu_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/imu_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/imu_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/imu_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build Dummy IMU Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name dummy_imu_node dummy_imu_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_imu_node.py /home/jetson/Desktop/ros2_ws/src/dummy_imu_package/dummy_imu_package/dummy_imu_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_imu_package/dummy_imu_package/dummy_imu_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_imu_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_imu_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_imu_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_imu_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/dummy_imu_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build RC Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name rc_node rc_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/rc_node.py /home/jetson/Desktop/ros2_ws/src/rc_package/rc_package/rc_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/rc_package/rc_package/rc_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/rc_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/rc_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/rc_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/rc_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/rc_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build Dummy RC Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name dummy_rc_node dummy_rc_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_rc_node.py /home/jetson/Desktop/ros2_ws/src/dummy_rc_package/dummy_rc_package/dummy_rc_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_rc_package/dummy_rc_package/dummy_rc_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_rc_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_rc_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_rc_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_rc_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/dummy_rc_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build Dummy Lidar Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name dummy_lidar_node dummy_lidar_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_lidar_node.py /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package/dummy_lidar_package/dummy_lidar_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package/dummy_lidar_package/dummy_lidar_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/dummy_lidar_package/install/local_setup.bash" >> /etc/bash.bashrc

# Build Dummy Lidar2 Node (Create Node > Update Permissions > Source It To Include In The Environment)
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python --node-name dummy_lidar2_node dummy_lidar2_package"
RUN /bin/bash -c "cp /home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_lidar2_node.py /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package/dummy_lidar2_package/dummy_lidar2_node.py"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package/dummy_lidar2_package/dummy_lidar2_node.py"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package && colcon build"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package"
RUN /bin/bash -c "source /opt/ros/humble/setup.bash"
RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package && source /opt/ros/humble/setup.bash && source install/local_setup.bash && source install/setup.bash"
RUN /bin/bash -c "chmod u+x /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package/install/local_setup.bash"
RUN echo "source /home/jetson/Desktop/ros2_ws/src/dummy_lidar2_package/install/local_setup.bash" >> /etc/bash.bashrc

# # Build Functions Interface (Create Interface > Update Permissions > Source It To Include In The Environment)
# RUN /bin/bash -c "cd /home/jetson/Desktop/ros2_ws/src && source /opt/ros/humble/setup.bash && ros2 pkg create --build-type ament_python py_srvcli --dependencies rclpy functions_interface"

RUN apt install python3.10-venv -y
RUN python3 -m venv /opt/venv
RUN python3 -m pip install --upgrade pip

# Install dependencies:
# COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install numpy ros2_numpy pandas matplotlib

# RUN . /opt/venv/bin/activate

# Run the application:
# CMD . /opt/venv/bin/activate && exec python myapp.py

