from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dummy_rc_package',
            namespace='dummy_rc_node',
            executable='dummy_rc_node',
            name='rc'
        )
        Node(
            package='dummy_gps_package',
            namespace='dummy_gps_node',
            executable='dummy_gps_node',
            name='gps'
        ),
        Node(
            package='dummy_imu_package',
            namespace='dummy_imu_node',
            executable='dummy_imu_node',
            name='imu'
        ),
        Node(
            package='dummy_lidar_package',
            namespace='dummy_lidar_node',
            executable='dummy_lidar_node',
            name='lidar'
        )
    ])