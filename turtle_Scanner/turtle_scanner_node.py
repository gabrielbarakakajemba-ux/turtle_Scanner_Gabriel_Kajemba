import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool
import math

class TurtleScanner(Node):

   def __init__(self):
        super().__init__('turtle_scanner')
        
        self.pose_scanner = None
        self.pose_target = None

        self.sub_scanner = self.create_subscription(Pose,'/turtle1/pose',self.callback_scanner,10)
        self.sub_target = self.create_subscription(Pose,'/turtle_target/pose',self.callback_target,10)

   def callback_scanner(self, msg):
        self.pose_scanner = msg
        self.get_logger().info(
           f"Scanner -> x={msg.x:.2f}, y={msg.y:.2f}"
        )

   def callback_target(self, msg):
       self.pose_target = msg
       self.get_logger().info(
           f"Target -> x={msg.x:.2f}, y={msg.y:.2f}"
       )
def main():
   rclpy.init()
   node = TurtleScanner()
   rclpy.spin(node)
   rclpy.shutdown()

if __name__ == '__main__':
   main()