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

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.Kp_ang = 5.0
        self.Kp_lin = 4.0
        self.tolerance = 0.1
        

        self.waypoints = self.generate_serpentin()
        self.current_wp = 0

        self.timer = self.create_timer(0.05, self.scan_step)

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
    def compute_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def compute_angle(self, x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)

    def generate_serpentin(self):
        waypoints = []

        x_min, x_max = 1.0, 10.0
        y = 1.0
        y_step = 2.0
        nb_lignes = 5

        for i in range(nb_lignes):
            if i % 2 == 0:
                waypoints.append((x_max, y))
            else:
                waypoints.append((x_min, y))
            y += y_step

        return waypoints

    def scan_step(self):
        if self.pose_scanner is None:
            return

        if self.current_wp >= len(self.waypoints):
            self.stop()
            self.get_logger().info("Balayage terminé")
            return

        target_x, target_y = self.waypoints[self.current_wp]

        dist = self.compute_distance(
            self.pose_scanner.x,
            self.pose_scanner.y,
            target_x,
            target_y
        )

        if dist < self.tolerance:
            self.current_wp += 1
            return

        desired_angle = self.compute_angle(
            self.pose_scanner.x,
            self.pose_scanner.y,
            target_x,
            target_y
        )

        error = desired_angle - self.pose_scanner.theta
        error = math.atan2(math.sin(error), math.cos(error))

        cmd = Twist()
        cmd.linear.x = min(self.Kp_lin * dist, 2.0)
        cmd.angular.z = self.Kp_ang * error

        self.cmd_pub.publish(cmd)
  
    def stop(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

def main():
   rclpy.init()
   node = TurtleScanner()
   rclpy.spin(node)
   rclpy.shutdown()

if __name__ == '__main__':
   main()