"""모든 이동 기능이 따라야 하는 공통 규격.

각자 파일을 만들 때 이 파일의 MoveCommand 를 상속받으면 됩니다.
이 파일은 수정하지 마세요. (수정하면 머지 충돌이 납니다)
"""

from geometry_msgs.msg import Twist


class MoveCommand:
    """이동 기능 하나를 나타내는 클래스.

    하위 클래스에서 채워야 하는 것:
        key         : 터미널에 입력할 번호 (문자열)
        description : 메뉴에 표시될 설명
        run(node)   : 실제 동작. node 는 TurtleController 인스턴스.

    node 에서 쓸 수 있는 것:
        node.publish(twist)          : cmd_vel 로 Twist 메시지 1회 발행
        node.publish_for(twist, sec) : sec 초 동안 반복 발행 후 정지
        node.stop()                  : 정지 명령 발행
        node.get_logger().info(...)  : 로그 출력
    """

    key = None
    description = "설명 없음"

    def run(self, node):
        raise NotImplementedError(
            f"{self.__class__.__name__} 에 run() 이 구현되지 않았습니다."
        )

    # --- 아래는 편의 함수입니다. 그대로 쓰면 됩니다 ---

    @staticmethod
    def make_twist(linear_x=0.0, angular_z=0.0):
        """Twist 메시지를 간단히 만들어 줍니다.

        linear_x  : 앞뒤 속도 (m/s). 양수면 전진, 음수면 후진
        angular_z : 회전 속도 (rad/s). 양수면 반시계, 음수면 시계 방향
        """
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        return msg