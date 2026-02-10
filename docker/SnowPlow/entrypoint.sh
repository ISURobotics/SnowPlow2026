#!/bin/bash

# Source the main ROS 2 setup
source /opt/ros/$ROS_DISTRO/setup.bash

# Source your workspace setup
source /app/install/setup.bash

# Execute the command given to the container
exec "$@"
