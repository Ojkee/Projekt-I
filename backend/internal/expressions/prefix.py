from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Prefix(Expression):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._expr = expr

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Prefix)
            and self._op.ttype == other._op.ttype
            and self._op.literal == other._op.literal
            and self._expr == other._expr
        )

    def __repr__(self) -> str:
        return f"PREFIX({repr(self._op)}, {repr(self._expr)}\n)"

    def __str__(self) -> str:
        return self._op.literal + str(self._expr)

    def operator(self) -> Token:
        return self._op
