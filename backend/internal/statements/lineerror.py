from backend.internal.statements import Statement


class LineError(Statement):
    __match_args__ = ("perr",)

    def __init__(self, err) -> None:
        self._err = err

    def __eq__(self, other, /) -> bool:
        if not isinstance(other, LineError):
            return False
        return str(self._err) == str(other._err)

    def __str__(self) -> str:
        return str(self._err)

    def __repr__(self) -> str:
        return repr(self._err)

    @property
    def perr(self):
        return self._err
