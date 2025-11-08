from backend.internal.parsing.parseerror import ParseErr
from backend.internal.statements import LineError
from backend.internal.statements import Statement


def wrap(msg: str) -> LineError:
    return LineError(ParseErr(msg, msg))


class AnyNonError(Statement):
    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Statement) -> bool:
        if isinstance(other, LineError):
            return False
        return True
