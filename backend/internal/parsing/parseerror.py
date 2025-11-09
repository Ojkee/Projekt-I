from typing import Any

from backend.internal.parsing.error_msgs import ErrorPrecedence


class StackFrame:
    def __init__(self, name: str, *args) -> None:
        self._name: str = name
        self._args: tuple[Any] = args

    def __repr__(self) -> str:
        args = ", ".join(map(str, self._args))
        return f"{self._name}({args})"


class ParseErr:
    def __init__(
        self,
        user_msg: str,
        msg: str,
        precedence: ErrorPrecedence = ErrorPrecedence.LOWEST,
    ) -> None:
        self._user_msg = user_msg
        self._msg = msg
        self._frames: list[StackFrame] = []
        self._precedence = precedence

    def __str__(self) -> str:
        return self._user_msg

    def __repr__(self) -> str:
        if self._frames:
            lines = "\n".join(f"|{repr(frame):>60}|" for frame in self._frames)
            return f"{lines}\n|{self._msg:>60}|\n| STR:{str(self._user_msg):>55}|"
        return self._msg

    def __eq__(self, other) -> bool:
        if not isinstance(other, ParseErr):
            return False
        return self._msg == other._msg

    def append(self, frame: str, *args) -> None:
        self._frames.append(StackFrame(frame, args))

    def more_precise_user_msg(self, msg: str, precedence: ErrorPrecedence) -> None:
        if precedence > self._precedence:
            self._user_msg = msg
