from backend.internal.statements import Statement
from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class AtomTransform(Statement):
    def __init__(self, operator: Token, expr: Expression) -> None:
        self._op = operator
        self._exrp = expr

    def to_str(self) -> str:
        return self._op.literal + self._exrp.pretty_str()
