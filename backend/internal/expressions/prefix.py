from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Prefix(Expression):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._expr = expr

    def __eq__(self, other) -> bool:
        if not isinstance(other, Prefix):
            return False
        return (
            self._op.ttype == other._op.ttype
            and self._op.literal == other._op.literal
            and self._expr == other._expr
        )

    def __repr__(self) -> str:
        return f"PREFIX({repr(self._op)}, {repr(self._expr)}\n)"

    def pretty_str(self) -> str:
        return self._op.literal + self._expr.pretty_str()
