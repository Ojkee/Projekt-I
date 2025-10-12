from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Identifier(Expression):
    def __init__(self, name: Token) -> None:
        super().__init__()
        self.name = name

    def __eq__(self, other) -> bool:
        return isinstance(other, Identifier) and self.name == other.name

    def __repr__(self) -> str:
        return f"IDENT({repr(self.name)})"

    def pretty_str(self) -> str:
        return self.name.literal
