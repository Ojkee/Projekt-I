from backend.internal.statements import Statement


class LineError(Statement):
    def __init__(self, msg: str, stack: list[str]) -> None:
        self._msg = msg
        self._stack = stack

    def to_str(self) -> str:
        buffer: list[str] = [
            "error `",
            self._msg,
            "`",
        ]
        return "".join(buffer)

    def stack_str(self) -> str:
        lines = map(lambda line: f"{line:>40}", self._stack)
        return "\n".join(lines)
