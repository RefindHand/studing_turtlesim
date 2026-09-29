"""moves 폴더의 이동 기능들을 자동으로 찾아서 등록합니다.

이 파일은 수정할 필요가 없습니다.
새 기능을 추가하려면 이 폴더에 새 .py 파일만 만들면
프로그램이 알아서 찾아냅니다.
"""

import importlib
import inspect
import pkgutil

from .base import MoveCommand


def load_commands():
    """moves 폴더 안의 모든 MoveCommand 하위 클래스를 수집합니다.

    반환값: {key: MoveCommand 인스턴스} 형태의 딕셔너리
    """
    commands = {}
    problems = []

    for module_info in pkgutil.iter_modules(__path__):
        name = module_info.name
        if name in ("base",) or name.startswith("_"):
            continue

        try:
            module = importlib.import_module(f".{name}", package=__name__)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"  [{name}.py] 불러오기 실패: {exc}")
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, MoveCommand) or obj is MoveCommand:
                continue
            # 다른 모듈에서 import 해온 클래스는 건너뜁니다
            if obj.__module__ != module.__name__:
                continue

            if obj.key is None:
                problems.append(f"  [{name}.py] {obj.__name__}: key 가 없습니다")
                continue

            key = str(obj.key)
            if key in commands:
                existing = type(commands[key]).__name__
                problems.append(
                    f"  [{name}.py] 번호 '{key}' 중복 "
                    f"({obj.__name__} vs {existing})"
                )
                continue

            commands[key] = obj()

    return commands, problems