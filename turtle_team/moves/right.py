from .base import MoveCommand


class Right(MoveCommand):
    key = "5"
    description = "오른쪽으로 2초 이동"

    def run(self, node):
        node.get_logger().info("오른쪽으로 이동합니다")
        twist = self.make_twist(linear_x=2.0, angular_z= - 0.75)
        node.publish_for(twist, 2.0)

        
