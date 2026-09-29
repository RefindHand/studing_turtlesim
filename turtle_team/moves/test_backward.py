from .base import MoveCommand


class Backward(MoveCommand):
    key = "2"
    description = "뒤로 2초 이동"

    def run(self, node):
        node.get_logger().info("뒤로 이동합니다")
        node.publish_for(self.make_twist(linear_x=-2.0), 2.0)