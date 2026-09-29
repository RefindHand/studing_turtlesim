from .base import MoveCommand


class MoveUp(MoveCommand):
    key = "3"
    description = "위쪽 — 앞으로 2초 이동"

    def run(self, node):
        node.get_logger().info("앞으로 이동합니다")
        node.publish_for(self.make_twist(linear_x=2.0), 2.0)
