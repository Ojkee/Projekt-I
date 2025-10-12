from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Infix(Expression):
    def __init__(self, operator: Token, lhs: Expression, rhs: Expression) -> None:
        super().__init__()
        self._op = operator
        self._lhs = lhs
        self._rhs = rhs

    def __eq__(self, other):
        if not isinstance(other, Infix):
            return False
        return (
            self._op.ttype == other._op.ttype
            and self._op.literal == other._op.literal
            and self._lhs == other._lhs
            and self._rhs == other._rhs
        )
    
    def __repr__(self) -> str:
        return f"INFIX({repr(self._op)} {repr(self._lhs)} {repr(self._rhs)})"

    def pretty_str(self) -> str:
        buffer: list[str] = [
            "(",
            self._lhs.pretty_str(),
            self._op.literal,
            self._rhs.pretty_str(),
            ")",
        ]
        return "".join(buffer)
