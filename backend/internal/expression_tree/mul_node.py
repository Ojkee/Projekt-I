from __future__ import annotations
from backend.internal.expression_tree import Node, FlattenNode
from backend.internal.expression_tree.numeric_node import FlattenNumeric, Numeric
from backend.internal.expression_tree.pow_node import Pow


class Mul(Node):
    __match_args__ = ("left", "right")

    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

        self.children = []

    def __eq__(self, other):
        return (
            isinstance(other, Mul)
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        return "(" + repr(self.left) + "*" + repr(self.right) + ")"

    def flatten(self) -> FlattenMul:
        children = []

        def _flat_node(n: Node) -> None:
            if isinstance(n, Mul):
                flat = n.flatten()
                children.extend(flat.children)
            else:
                children.append(n.flatten())

        _flat_node(self.left)
        _flat_node(self.right)

        return FlattenMul(children)

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        match left, right:
            case Numeric(0), Pow(Numeric(0), Numeric(a)) if a < 1:
                pass

            # 0*x or x*0 => 0
            case (Numeric(0), _) | (_, Numeric(0)):
                return Numeric(0)

            # 1*x or x*1  => x
            case (Numeric(1), other) | (other, Numeric(1)):
                return other

            case Numeric(a), Numeric(b):
                return Numeric(a * b)

        return Mul(left, right)


class FlattenMul(FlattenNode):
    PRECEDENCE = 2

    def __init__(self, children: list[FlattenNode]) -> None:
        self.children = children

    def constant_fold(self) -> FlattenNode:
        numeric_product = 1.0
        new_children = []

        for child in self.children:
            folded = child.constant_fold()

            if isinstance(folded, FlattenNumeric):
                numeric_product *= folded.value
            else:
                new_children.append(folded)

        if numeric_product != 1 or not new_children:
            new_children.append(FlattenNumeric(numeric_product))

        if len(new_children) == 1:
            return new_children[0]

        return FlattenMul(new_children)


    def __str__(self) -> str:
        parts = []
        is_negative = isinstance(self.children[0], FlattenNumeric) and self.children[
            0
        ] == FlattenNumeric(-1)
        start = 1 if is_negative else 0

        for c in self.children[start:]:
            if (
                is_negative and isinstance(c, FlattenNumeric) and c.value < 0
            ):  # example case: x - (-3)
                parts.append(f"({c.value})")
            elif c is not None and c.precedence() < self.PRECEDENCE:
                parts.append(f"({c})")
            else:
                parts.append(f"{c}")

        return " * ".join(parts)

    def __eq__(self, other):
        return isinstance(other, FlattenMul) and self.children == other.children

    def precedence(self):
        return self.PRECEDENCE
