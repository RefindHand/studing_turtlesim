"""예제: 앞으로 이동 (팀장 작성 — 참고용)

이 파일을 그대로 복사해서 자기 기능을 만들면 됩니다.
"""

from .base import MoveCommand


class Forward(MoveCommand):
    key = "0"
    description = "(예제) 앞으로 2초 이동"

    def run(self, node):
        node.get_logger().info("앞으로 이동합니다")
        twist = self.make_twist(linear_x=2.0)
        node.publish_for(twist, 2.0)