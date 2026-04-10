import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import random

class SpawnTarget(Node):

    def __init__(self):
        super().__init__('spawn_target')

        self.client = self.create_client(Spawn, '/spawn')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service en attente...')

        self.spawn_target()

    def spawn_target(self):
        request = Spawn.Request()
        request.x = random.uniform(1.0, 10.0)
        request.y = random.uniform(1.0, 10.0)
        request.theta = 0.0
        request.name = 'turtle_target'

        future = self.client.call_async(request)
        future.add_done_callback(self.callback)

    def callback(self, future):
        response = future.result()
        self.get_logger().info(f'Cible spawn à x={response.name}')

def main():
    rclpy.init()
    node = SpawnTarget()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()