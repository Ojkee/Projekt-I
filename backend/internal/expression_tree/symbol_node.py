from backend.internal.expression_tree import Node, FlattenNode

class Symbol(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __repr__(self):
        return self.name

    def __str__(self) -> str:
        return self.flatten().__str__()

    def flatten(self) -> FlattenNode:
        return FlattenSymbol(self.name)

class FlattenSymbol(FlattenNode):
    PRECEDENCE = 999
    def __init__(self, name: str) -> None:
        self.name = name

    def constant_fold(self) -> FlattenNode:
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, FlattenSymbol)
            and self.name == other.name
            )

    def precedence(self):
        return self.PRECEDENCE
