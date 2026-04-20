import rclpy
import time
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py.point_cloud2 import read_points
import numpy as np


class PointCloudSubscriber(Node):
    def __init__(self):
        super().__init__('point_cloud_subscriber')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/cloud',  # Change this to your topic name
            self.listener_callback,
            10)
        self.get_logger().info('PointCloud subscriber initialized.')

    def listener_callback(self, msg):
        points = list(read_points(msg, skip_nans=True))

        if len(points) == 0:
            self.get_logger().info("Received empty point cloud.")
            return

        points_array = np.array(points)

        if points_array.ndim == 1:
            # handle tuple structure
            x_coords = np.array([p[0] for p in points])
            print(f"start scan:")
            for p in points:
                print(f"points: {p[0]}, {p[1]}")

            x_coords = np.round(x_coords,2)
            y_coords = np.array([p[1] for p in points])
            y_coords = np.round(y_coords, 2)

            if len(points[0]) > 2:
                z_coords = np.array([p[2] for p in points])
            else:
                z_coords = np.zeros(len(points))

        else:
            x_coords = points_array[:, 0]
            y_coords = points_array[:, 1]
            z_coords = points_array[:, 2] if points_array.shape[1] > 2 else np.zeros(len(points_array))


        #Search all coords to find cones
        filtered_points = []
        prev_in_range = False

        for i in range(len(x_coords)):
            in_range = (0 < y_coords[i] < 6.5) and (0 < x_coords[i] < 10)

            if in_range and not prev_in_range:
                filtered_points.append((x_coords[i], y_coords[i]))

            prev_in_range = in_range

        print("Filtered points:")
        print(filtered_points)

        cone_points = []

        for f in filtered_points:
            x, y = f  # unpack tuple

            distance = np.sqrt(x**2 + y**2)
            angle = np.arctan2(y, x)

            cone_points.append((x, y, distance, angle))




        # self.get_logger().info(f"Received {len(x_coords)} points")
        # self.get_logger().info(f"First point: x={x_coords}, y={y_coords}")
        time.sleep(1)

# Convert a SickScanCartesianPointCloudMsg to points
# def pySickScanCartesianPointCloudMsgToXYZ(pointcloud_msg):
# 	print("hello")
# 	# get point cloud fields
# 	num_fields = pointcloud_msg.fields.size
# 	msg_fields_buffer = pointcloud_msg.fields.buffer
# 	field_offset_x = -1
# 	field_offset_y = -1
# 	field_offset_z = -1
# 	for n in range(num_fields):
# 		field_name = ctypesCharArrayToString(msg_fields_buffer[n].name)
# 		field_offset = msg_fields_buffer[n].offset
# 		if field_name == "x":
# 			field_offset_x = msg_fields_buffer[n].offset
# 		elif field_name == "y":
# 			field_offset_y = msg_fields_buffer[n].offset
# 		elif field_name == "z":
# 			field_offset_z = msg_fields_buffer[n].offset
# 	# Extract x,y,z
# 	cloud_data_buffer_len = (pointcloud_msg.row_step * pointcloud_msg.height) # length of polar cloud data in byte
# 	assert(pointcloud_msg.data.size == cloud_data_buffer_len and field_offset_x >= 0 and field_offset_y >= 0 and field_offset_z >= 0)
# 	cloud_data_buffer = bytearray(cloud_data_buffer_len)
# 	for n in range(cloud_data_buffer_len):
# 		cloud_data_buffer[n] = pointcloud_msg.data.buffer[n]
# 	points_x = np.zeros(pointcloud_msg.width * pointcloud_msg.height, dtype = np.float32)
# 	points_y = np.zeros(pointcloud_msg.width * pointcloud_msg.height, dtype = np.float32)
# 	points_z = np.zeros(pointcloud_msg.width * pointcloud_msg.height, dtype = np.float32)
# 	point_idx = 0
# 	for row_idx in range(pointcloud_msg.height):
# 		for col_idx in range(pointcloud_msg.width):
# 			# Get lidar point in polar coordinates (range, azimuth and elevation)
# 			pointcloud_offset = row_idx * pointcloud_msg.row_step + col_idx * pointcloud_msg.point_step
# 			points_x[point_idx] = np.frombuffer(cloud_data_buffer, dtype = np.float32, count = 1, offset = pointcloud_offset + field_offset_x)[0]
# 			points_y[point_idx] = np.frombuffer(cloud_data_buffer, dtype = np.float32, count = 1, offset = pointcloud_offset + field_offset_y)[0]
# 			points_z[point_idx] = np.frombuffer(cloud_data_buffer, dtype = np.float32, count = 1, offset = pointcloud_offset + field_offset_z)[0]
# 			point_idx = point_idx + 1
# 	print(points_x)
# 	return points_x, points_y, points_z

def main(args=None):
    rclpy.init(args=args)
    point_cloud_subscriber = PointCloudSubscriber()
    rclpy.spin(point_cloud_subscriber)
    # pySickScanCartesianPointCloudMsgToXYZ(point_cloud_subscriber)
    point_cloud_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()




	

