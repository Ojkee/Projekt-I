from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Infix(Expression):
    def __init__(self, operator: Token, lhs: Expression, rhs: Expression) -> None:
        super().__init__()
        self._op = operator
        self._lhs = lhs
        self._rhs = rhs

    def __eq__(self, other):
        return (
            isinstance(other, Infix)
            and self._op == other._op
            and self._lhs == other._lhs
            and self._rhs == other._rhs
        )

    def __repr__(self) -> str:
        return f"INFIX({repr(self._op)} {repr(self._lhs)} {repr(self._rhs)})"

    def __str__(self) -> str:
        buffer: list[str] = [
            "(",
            str(self._lhs),
            self._op.literal,
            str(self._rhs),
            ")",
        ]
        return "".join(buffer)

    def operator(self) -> Token:
        return self._op
