from .base import MoveCommand


<<<<<<< HEAD
class Left(MoveCommand):
=======
class Forward(MoveCommand):
>>>>>>> 7719c9f05757011ebdb5ae2ef1860b4d040253d6
    key = "1"
    description = "왼쪽으로 1초 이동"

    def run(self, node):
        node.get_logger().info("왼쪽으로 이동합니다")
        twist = self.make_twist(linear_x=2.0, angular_z= -0.25)
        node.publish_for(twist, 1.0)
