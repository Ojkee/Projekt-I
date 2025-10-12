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

    def to_str(self) -> str:
        return self._expr.pretty_str()
    

