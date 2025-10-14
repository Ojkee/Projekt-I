from backend.internal.expressions import Expression
from backend.internal.statements import Statement


class Subject(Statement):
    def __init__(self, expr: Expression) -> None:
        super().__init__()
        self._expr = expr

    def __eq__(self, other):
        return isinstance(other, Subject) and self._expr == other._expr

    def __repr__(self) -> str:
        return f"Subject({repr(self._expr)})"

    def __str__(self) -> str:
        return str(self._expr)

    @property
    def expr(self) -> Expression:
        return self._expr
