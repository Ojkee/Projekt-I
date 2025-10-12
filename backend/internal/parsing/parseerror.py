from typing import Any


class StackFrame:
    def __init__(self, name: str, *args) -> None:
        self._name: str = name
        self._args: tuple[Any] = args

    def __str__(self) -> str:
        args = ", ".join(map(str, self._args))
        return f"{self._name}({args})"


class ParseErr:
    def __init__(self, msg: str) -> None:
        self._msg = msg
        self._frames: list[StackFrame] = []

    def __str__(self) -> str:
        return self._msg

    def append(self, frame: str, *args) -> None:
        self._frames.append(StackFrame(frame, args))

    def stack(self) -> list[str]:
        return list(map(str, self._frames))
