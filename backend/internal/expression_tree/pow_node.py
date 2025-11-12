from __future__ import annotations
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
        return str(self.flatten())

    def flatten(self) -> FlattenPow:
        return FlattenPow(self.base.flatten(), self.exponent.flatten())

    def reduce(self) -> Node:
        base = self.base.reduce()
        exponent = self.exponent.reduce()

        match base, exponent:
            case Numeric(a), Numeric(b) if a < 0 and b == int(b):
                return Numeric(a**b)
            case Numeric(0), Numeric(b) if 0 < b:
                return Numeric(0)
            case Numeric(a), Numeric(b) if 0 < a:
                return Numeric(a**b)

            # x^0 => 1
            case _, Numeric(0):
                return Numeric(1)

            # x^1 => x
            case _, Numeric(1):
                return base

        return Pow(base, exponent)


class FlattenPow(FlattenNode):
    PRECEDENCE = 3

    def __init__(self, base: FlattenNode, exponent: FlattenNode) -> None:
        self.base = base
        self.exponent = exponent

    def constant_fold(self) -> FlattenNode:
        self.base.constant_fold()
        self.exponent.constant_fold()

        match self.base, self.exponent:
            case (FlattenNumeric(lv), FlattenNumeric(rv)):
                return FlattenNumeric(lv**rv)

            case (_, FlattenNumeric(0)):
                return FlattenNumeric(1)

            case (_, FlattenNumeric(1)):
                return self.base

        return self

    def __str__(self) -> str:
        base_str = str(self.base)
        if hasattr(self.base, "PRECEDENCE") and self.base.PRECEDENCE < self.PRECEDENCE:
            base_str = f"({base_str})"

        exponent_str = str(self.exponent)
        if (
            hasattr(self.exponent, "PRECEDENCE")
            and self.exponent.PRECEDENCE < self.PRECEDENCE
        ):
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
