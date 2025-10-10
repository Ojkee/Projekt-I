from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Prefix(Expression):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._expr = expr

    def debug_str(self) -> str:
        buffer: list[str] = [
            "PREFIX(",
            self._op.literal,
            self._expr.debug_str(),
            ")",
        ]
        return "".join(buffer)

    def pretty_str(self) -> str:
        return self._op.literal + self._expr.pretty_str()
