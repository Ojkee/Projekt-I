from backend.internal.statements import Statement


class LineError(Statement):
    def __init__(self, err) -> None:
        self._err = err

    def __str__(self) -> str:
        buffer: list[str] = [
            "error `",
            str(self._err),
            "`",
        ]
        return "".join(buffer)

    def __repr__(self) -> str:
        lines = map(lambda line: f"{line:>40}", self._err.stack())
        return "\n".join(lines)
