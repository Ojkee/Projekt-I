from backend.internal.expression_tree import Node, FlattenNode
from backend.internal.expression_tree.numeric_node import FlattenNumeric, Numeric

class Pow(Node):
    __match_args__ = ("base", "exponent")

    def __init__(self, base: Node, exponent: Node) -> None:
        self.base = base
        self.exponent = exponent

    def __eq__(self, other):
        return (
            isinstance(other, Pow)
            and self.base == other.base
            and self.exponent == other.exponent
        )

    def __repr__(self):
        return "(" + repr(self.base) + "^" + repr(self.exponent) + ")"

    def __str__(self) -> str:
        return self.flatten().__str__()

    def flatten(self) -> FlattenNode:
        return FlattenPow(self.base.flatten(), self.exponent.flatten())

    def reduce(self) -> Node:
        base = self.base.reduce()
        exponent = self.exponent.reduce()

        match exponent:
            # x^0 => 1
            case Numeric(value=0):
                return Numeric(1)

            # x^1 => x
            case Numeric(value=1):
                return base

        return Pow(base, exponent)


class FlattenPow(FlattenNode):
    PRECEDENCE = 3
    def __init__(self, base: Node, exponent: Node) -> None:
        self.base = base
        self.exponent = exponent

    def constant_fold(self) -> FlattenNode:
        self.base.constant_fold()
        self.exponent.constant_fold()

        if isinstance(self.base, FlattenNumeric) and isinstance(self.exponent, FlattenNumeric):
            base_value = self.base.value
            exponent_value = self.exponent.value
            folded_value = base_value ** exponent_value
            return FlattenNumeric(folded_value)

        return self

    def __str__(self) -> str:
        base_str = str(self.base)
        if hasattr(self.base, 'PRECEDENCE') and self.base.PRECEDENCE < self.PRECEDENCE:
            base_str = f"({base_str})"
        exponent_str = str(self.exponent)
        if hasattr(self.exponent, 'PRECEDENCE') and self.exponent.PRECEDENCE < self.PRECEDENCE:
            exponent_str = f"({exponent_str})"
        return f"{base_str} ^ {exponent_str}"

    def __eq__(self, other):
        return (
            isinstance(other, FlattenPow)
            and self.base == other.base
            and self.exponent == other.exponent
        )

    def precedence(self):
        return self.PRECEDENCE

