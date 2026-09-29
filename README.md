# studing_turtlesim

터틀심 팀 협업 실습. 터미널에 번호를 입력하면 거북이가 움직입니다.

각자 **파일 하나씩** 만들어서 기능을 추가합니다. 서로 다른 파일을 만들기
때문에 머지 충돌이 나지 않습니다. 공용 파일(`controller.py`,
`moves/__init__.py`, `moves/base.py`)은 **수정하지 마세요.**

---

## 담당 배정

| 담당자 | 번호 | 기능 | 만들 파일 |
|---|---|---|---|
| 김선욱 | 0 | (예제) 앞으로 2초 이동 | `moves/example_forward.py` — 작성 완료, 참고용 |
| 박준선 | 1 | 왼쪽 — 제자리에서 반시계 방향 90도 회전 | `moves/move_left.py` |
| 조안정 | 2 | 오른쪽 — 제자리에서 시계 방향 90도 회전 | `moves/move_right.py` |
| 이태경 | 3 | 위쪽 — 앞으로 2초 이동 | `moves/move_up.py` |
| 김반석 | 4 | 아래쪽 — 뒤로 2초 이동 | `moves/move_down.py` |

방향키 조작과 같은 방식입니다. 위/아래는 전진·후진, 좌/우는 제자리 회전입니다.
---

## 처음 한 번만 하는 준비

### 1. 저장소 받기

```bash
cd ~/ros2_ws/src
git clone https://github.com/RefindHand/studing_turtlesim.git
```

### 2. 빌드

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select turtle_team
source install/setup.bash
```

`--symlink-install` 을 쓰면 파이썬 파일을 고칠 때마다 다시 빌드하지
않아도 됩니다.

### 3. 실행해 보기

터미널 2개가 필요합니다.

```bash
# 터미널 1
ros2 run turtlesim turtlesim_node
```

```bash
# 터미널 2
source ~/ros2_ws/install/setup.bash
ros2 run turtle_team controller
```

메뉴가 뜨고 `1` 을 누르면 거북이가 앞으로 갑니다. 여기까지 되면 준비 끝.

---

## 작업 순서

### 1. 최신 코드 받기

```bash
git switch main
git pull origin main
```

작업 시작 전에 **항상** 합니다.

### 2. 브랜치 만들기

```bash
git switch -c feature/backward
```

브랜치 이름은 `feature/<기능이름>` 으로 통일합니다.

### 3. 파일 만들기

`turtle_team/moves/` 폴더에 자기 파일을 만듭니다. `example_forward.py`
를 복사해서 고치는 게 가장 빠릅니다.

```python
# turtle_team/moves/backward.py
from .base import MoveCommand


class Backward(MoveCommand):
    key = "2"
    description = "뒤로 2초 이동"

    def run(self, node):
        node.get_logger().info("뒤로 이동합니다")
        twist = self.make_twist(linear_x=-2.0)
        node.publish_for(twist, 2.0)
```

지켜야 할 것은 세 가지입니다.

- `MoveCommand` 를 상속받는다
- `key` 와 `description` 을 채운다
- `run(self, node)` 를 구현한다

나머지는 자유입니다. 파일을 저장하면 프로그램이 알아서 찾아서 메뉴에
띄웁니다. 등록하는 코드를 어디에 추가할 필요가 없습니다.

### 4. 직접 테스트

```bash
cd ~/ros2_ws && colcon build --symlink-install --packages-select turtle_team
source install/setup.bash
ros2 run turtle_team controller
```

자기 번호를 눌러서 의도대로 움직이는지 확인합니다. **동작을 확인하지
않은 코드는 push 하지 마세요.**

### 5. 커밋과 푸시

```bash
git add turtle_team/moves/backward.py
git commit -m "feat: 뒤로 이동 기능 추가"
git push origin feature/backward
```

`git add .` 대신 파일을 지정하는 습관을 들이면 실수로 다른 파일을
올리는 일이 없습니다.

### 6. Pull Request

GitHub 저장소 페이지에 "Compare & pull request" 버튼이 뜹니다. 누르고
제목과 설명을 적어서 PR을 엽니다.

설명에 이 정도만 적어주세요.

```
- 담당: 2번 뒤로 이동
- 추가한 파일: turtle_team/moves/backward.py
- 테스트: 실행해서 거북이가 뒤로 가는 것 확인
```

팀장이 확인 후 main 에 머지합니다.

---

## 쓸 수 있는 함수

`run(self, node)` 안에서 이것들을 씁니다.

| 쓰는 법 | 하는 일 |
|---|---|
| `self.make_twist(linear_x=2.0)` | 앞으로 가는 명령 만들기 (음수면 뒤로) |
| `self.make_twist(angular_z=1.5)` | 회전 명령 만들기 (양수 반시계, 음수 시계) |
| `node.publish_for(twist, 2.0)` | 2초 동안 그 명령 보내고 정지 |
| `node.publish(twist)` | 한 번만 보내기 |
| `node.stop()` | 즉시 정지 |
| `node.get_logger().info("...")` | 로그 출력 |

### 회전 각도 계산

`angular_z` 는 초당 회전하는 **라디안** 값입니다. 90도는 약 1.5708
라디안이므로, 속도 1.5708 로 1초 돌리면 90도입니다.

```python
import math

from .base import MoveCommand


class TurnLeft(MoveCommand):
    key = "3"
    description = "왼쪽으로 90도 회전"

    def run(self, node):
        twist = self.make_twist(angular_z=math.pi / 2)  # 초당 90도
        node.publish_for(twist, 1.0)                    # 1초 → 90도
```

터틀심은 정확한 각도 제어가 아니라 속도 명령이라 오차가 조금 생깁니다.
정확히 맞추고 싶으면 `/turtle1/pose` 토픽을 구독해서 현재 각도를 읽는
방법이 있는데, 그건 여유 있을 때 도전해 보세요.

### 여러 동작 이어 붙이기

```python
import math

from .base import MoveCommand


class Square(MoveCommand):
    key = "5"
    description = "사각형 그리기"

    def run(self, node):
        for _ in range(4):
            node.publish_for(self.make_twist(linear_x=2.0), 2.0)
            node.publish_for(self.make_twist(angular_z=math.pi / 2), 1.0)
```
### 방향별 구현 힌트

```python
# 위쪽 (전진)
node.publish_for(self.make_twist(linear_x=2.0), 2.0)

# 아래쪽 (후진)
node.publish_for(self.make_twist(linear_x=-2.0), 2.0)

# 왼쪽 (반시계 회전) — math.pi / 2 는 초당 90도
node.publish_for(self.make_twist(angular_z=math.pi / 2), 1.0)

# 오른쪽 (시계 회전) — 음수면 반대 방향
node.publish_for(self.make_twist(angular_z=-math.pi / 2), 1.0)
```

회전을 쓰려면 파일 맨 위에 `import math` 를 추가하세요.
---

## 규칙

- **공용 파일은 건드리지 않습니다.** `controller.py`,
  `moves/__init__.py`, `moves/base.py` 를 고치면 충돌이 납니다. 고쳐야
  할 이유가 생기면 팀에 먼저 이야기하세요.
- **`key` 번호가 겹치지 않게 합니다.** 위 표를 확인하세요. 겹치면
  프로그램이 실행될 때 경고를 띄우고 하나를 무시합니다.
- **main 브랜치에 직접 push 하지 않습니다.** 반드시 브랜치를 만들어
  PR로 올립니다.
- **`build/`, `install/`, `log/` 는 올리지 않습니다.** `.gitignore` 에
  이미 들어 있으니 신경 안 써도 되지만, `git status` 에 보이면 뭔가
  잘못된 것입니다.

---

## 막혔을 때

**메뉴에 내 기능이 안 보임**
→ 파일이 `turtle_team/moves/` 폴더 안에 있는지, `MoveCommand` 를
상속했는지, `key` 를 채웠는지 확인하세요. 실행할 때 `[주의]` 로
시작하는 메시지가 뜨면 거기에 이유가 적혀 있습니다.

**`ros2 run` 이 패키지를 못 찾음**
→ `source ~/ros2_ws/install/setup.bash` 를 했는지 확인하세요. 터미널을
새로 열 때마다 필요합니다.

**거북이가 잠깐 움직이다 멈춤**
→ 터틀심은 약 1초간 명령이 없으면 스스로 멈춥니다. `publish` 대신
`publish_for` 를 쓰세요.

**pull 했더니 충돌이 남**
→ 공용 파일을 고쳤을 가능성이 높습니다. 팀장에게 문의하세요.