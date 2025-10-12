from __future__ import annotations
from backend.internal.statements import Statement
from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class AtomTransform(Statement):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._expr = expr

    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, AtomTransform)
            and self._op == value._op
            and self._expr == value._expr
        )

    def __repr__(self) -> str:
        return f"AtomTransform({repr(self._op)} {repr(self._expr)})"

    def __str__(self) -> str:
        return self._op.literal + self._expr.pretty_str()
