from backend.internal.expressions import Expression
from backend.internal.tokens import Token


class Identifier(Expression):
    def __init__(self, name: Token) -> None:
        super().__init__()
        self.name = name

    def debug_str(self) -> str:
        buffer: list[str] = ["IDENT(", self.name.literal, ")"]
        return "".join(buffer)

    def pretty_str(self) -> str:
        return self.name.literal
