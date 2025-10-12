from backend.internal.statements import Statement
from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class AtomTransform(Statement):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._expr = expr
    
    def __eq__(self, other):
        return isinstance(other, AtomTransform) and self._op == other._op and self._expr == other._expr

    def __repr__(self) -> str:
        return f"AtomTransform({repr(self._op)} {repr(self._expr)})"

    def to_str(self) -> str:
        return self._op.literal + self._expr.pretty_str()
