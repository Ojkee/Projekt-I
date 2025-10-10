from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Infix(Expression):
    def __init__(self, operator: Token, lhs: Expression, rhs: Expression) -> None:
        super().__init__()
        self._op = operator
        self._lhs = lhs
        self._rhs = rhs

    def debug_str(self) -> str:
        buffer: list[str] = [
            "INFIX(",
            self._lhs.debug_str(),
            self._op.literal,
            self._rhs.debug_str(),
            ")",
        ]
        return "".join(buffer)

    def pretty_str(self) -> str:
        buffer: list[str] = [
            "(",
            self._lhs.pretty_str(),
            self._op.literal,
            self._rhs.pretty_str(),
            ")",
        ]
        return "".join(buffer)
