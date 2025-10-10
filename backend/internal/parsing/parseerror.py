from typing import Any


class StackFrame:
    def __init__(self, name: str, *args) -> None:
        self._name: str = name
        self._args: tuple[Any] = args

    def to_str(self) -> str:
        args = ", ".join(map(str, self._args))
        return f"{self._name}({args})"


class ParseErr:
    def __init__(self, msg: str) -> None:
        self._msg = msg
        self._stack: list[StackFrame] = []

    def error(self) -> str:
        return self._msg

    def append(self, frame: str, *args) -> None:
        self._stack.append(StackFrame(frame, args))

    def stack(self) -> list[str]:
        return list(map(lambda frame: frame.to_str(), self._stack))
