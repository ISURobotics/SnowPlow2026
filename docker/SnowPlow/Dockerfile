FROM ros:humble-ros-base

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        python3-pip \
        python3-venv \
        ros-humble-navigation2 \
        ros-humble-nav2-bringup \
        ros-humble-joint-state-publisher-gui \
        ros-humble-sick-scan-xd \
    && rm -rf /var/lib/apt/lists/*

COPY src/Originals/NewNodes/ /tmp/new_nodes/

RUN mkdir -p /app/src \
    && source /opt/ros/humble/setup.bash \
    && cd /app/src \
    && for node in gps dummy_gps imu dummy_imu rc dummy_rc dummy_lidar dummy_lidar2; do \
         package="${node}_package"; \
         ros2 pkg create --build-type ament_python --node-name "${node}_node" "${package}"; \
         cp "/tmp/new_nodes/${node}_node.py" "/app/src/${package}/${package}/${node}_node.py"; \
         chmod +x "/app/src/${package}/${package}/${node}_node.py"; \
       done \
    && cd /app \
    && colcon build --symlink-install \
    && rm -rf /tmp/new_nodes

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
