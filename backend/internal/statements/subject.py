from backend.internal.expressions import Expression
from backend.internal.statements import Statement


class Subject(Statement):
    def __init__(self, expr: Expression) -> None:
        super().__init__()
        self._expr = expr

    def to_str(self) -> str:
        return self._expr.pretty_str()
