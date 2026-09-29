"""터틀심 조종 메인 프로그램.

터미널에 번호를 입력하면 해당 기능이 실행됩니다.
기능은 moves/ 폴더에서 자동으로 불러옵니다.

이 파일은 수정하지 마세요. 기능 추가는 moves/ 에 새 파일을 만들면 됩니다.
"""

import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

from .moves import load_commands


class TurtleController(Node):
    """cmd_vel 토픽으로 터틀을 움직이는 노드."""

    def __init__(self):
        super().__init__("turtle_controller")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.get_logger().info("turtle_controller 시작")

    def publish(self, twist):
        """Twist 메시지를 한 번 발행합니다."""
        self.publisher.publish(twist)

    def publish_for(self, twist, duration_sec, rate_hz=20.0):
        """duration_sec 동안 반복 발행한 뒤 정지합니다.

        터틀심은 약 1초간 명령이 없으면 스스로 멈추기 때문에,
        일정 시간 움직이려면 반복해서 보내야 합니다.
        """
        period = 1.0 / rate_hz
        end_time = time.time() + duration_sec

        while time.time() < end_time:
            self.publisher.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)

        self.stop()

    def stop(self):
        """정지 명령을 발행합니다."""
        self.publisher.publish(Twist())


def print_menu(commands):
    print()
    print("=" * 40)
    print("  터틀심 조종기")
    print("=" * 40)
    for key in sorted(commands, key=lambda k: (len(k), k)):
        print(f"  {key}. {commands[key].description}")
    print("  q. 종료")
    print("=" * 40)


def main(args=None):
    commands, problems = load_commands()

    if problems:
        print("[주의] 일부 기능을 불러오지 못했습니다:")
        for line in problems:
            print(line)
        print()

    if not commands:
        print("실행할 수 있는 기능이 없습니다. moves/ 폴더를 확인하세요.")
        return

    rclpy.init(args=args)
    node = TurtleController()

    try:
        while True:
            print_menu(commands)
            try:
                choice = input("번호 입력: ").strip()
            except EOFError:
                break

            if choice.lower() in ("q", "quit", "exit"):
                break

            command = commands.get(choice)
            if command is None:
                print(f"'{choice}' 는 없는 번호입니다.")
                continue

            try:
                command.run(node)
            except Exception as exc:  # noqa: BLE001
                # 한 사람의 기능이 터져도 프로그램 전체는 살아있게 합니다
                node.get_logger().error(
                    f"[{type(command).__name__}] 실행 중 오류: {exc}"
                )
                node.stop()

    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        print("\n종료합니다.")


if __name__ == "__main__":
    main()