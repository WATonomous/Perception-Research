from re import template
import rclpy
from rclpy.node import Node
import numpy as np

class Template(Node):
    def __init__(self):
        super().__init__('template_node')

def main(args=None):
    rclpy.init(args=args)
    template_node = Template()
    rclpy.spin(template_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    template.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()