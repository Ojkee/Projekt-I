from backend.internal.expression_tree import Node, FlattenNode


class Numeric(Node):
    __match_args__ = ("value",)

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Numeric) and self.value == other.value

    def __repr__(self):
        return str(self.value)

    def __str__(self) -> str:
        return self.flatten().__str__()

    def flatten(self) -> FlattenNode:
        return FlattenNumeric(self.value)

    def reduce(self) -> Node:
        return self


class FlattenNumeric(FlattenNode):
    PRECEDENCE = 999
    __match_args__ = ("value",)

    def __init__(self, value: float) -> None:
        self.value = value

    def constant_fold(self) -> FlattenNode:
        return self

    def __eq__(self, other):
        return isinstance(other, FlattenNumeric) and self.value == other.value

    def __str__(self):
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)

    def unflatten(self) -> Numeric:
        return Numeric(self.value)

    def precedence(self):
        return self.PRECEDENCE

