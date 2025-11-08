from backend.internal.statements import Statement


class LineError(Statement):
    def __init__(self, err) -> None:
        self._err = err

    def __str__(self) -> str:
        return str(self._err)

    def __eq__(self, other, /) -> bool:
        if not isinstance(other, LineError):
            return False
        return self._err == other._err

    def __repr__(self) -> str:
        if self._err.stack():
            lines = (f"{line:>40}" for line in self._err.stack())
            return f"{"\n".join(lines)}\n{str(self._err):>40}"
        return str(self._err)
