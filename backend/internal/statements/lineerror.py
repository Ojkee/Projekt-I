from backend.internal.statements import Statement


class LineError(Statement):
    def __init__(self, err) -> None:
        self._err = err

    def __str__(self) -> str:
        return str(self._err)

    def __repr__(self) -> str:
        if self._err.stack():
            lines = map(lambda line: f"{line:>40}", self._err.stack())
            return "\n".join(lines)
        return str(self._err)
