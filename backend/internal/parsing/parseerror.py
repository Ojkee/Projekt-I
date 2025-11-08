from typing import Any


class StackFrame:
    def __init__(self, name: str, *args) -> None:
        self._name: str = name
        self._args: tuple[Any] = args

    def __repr__(self) -> str:
        args = ", ".join(map(str, self._args))
        return f"{self._name}({args})"


class ParseErr:
    def __init__(self, user_msg: str, msg: str) -> None:
        self._user_msg = user_msg
        self._msg = msg
        self._frames: list[StackFrame] = []

    def __str__(self) -> str:
        return self._user_msg

    def __repr__(self) -> str:
        if self._frames:
            lines = "\n".join(f"{repr(frame):>60}" for frame in self._frames)
            return f"{lines}\n{self._msg:>60}"
        return self._msg

    def __eq__(self, other) -> bool:
        if not isinstance(other, ParseErr):
            return False
        return self._msg == other._msg

    def append(self, frame: str, *args) -> None:
        self._frames.append(StackFrame(frame, args))
