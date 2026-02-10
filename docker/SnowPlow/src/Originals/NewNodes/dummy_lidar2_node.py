import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DummyLidar2Publisher(Node):
    def __init__(self):
        super().__init__('dummy_lidar2_node')
        self.publisher_ = self.create_publisher(String, 'dummy_lidar2_node', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.lines = self.read_file('/home/jetson/Desktop/ros2_ws/src/Originals/NewNodes/dummy_lidar2_data.txt') # Read file on init
        self.line_index = 0

    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()

    def timer_callback(self):
        if self.line_index < len(self.lines):
            msg = String()
            msg.data = self.lines[self.line_index].strip()
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing: "{msg.data}"')
            self.line_index += 1
        else:
            self.line_index = 0

def main(args=None):
    rclpy.init(args=args)
    node = DummyLidar2Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()