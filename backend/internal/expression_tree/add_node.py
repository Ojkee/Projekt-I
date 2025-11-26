from __future__ import annotations
from .node import Node, FlattenNode
from backend.internal.expression_tree.numeric_node import FlattenNumeric, Numeric
from backend.internal.expression_tree.mul_node import FlattenMul


class Add(Node):
    __match_args__ = ("left", "right")

    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            isinstance(other, Add)
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        return "(" + repr(self.left) + "+" + repr(self.right) + ")"

    def __str__(self) -> str:
        return self.flatten().__str__()

    def flatten(self) -> FlattenAdd:
        children: list[FlattenNode] = []

        def _flat_node(n: Node) -> None:
            if isinstance(n, Add):
                flat = n.flatten()
                children.extend(flat.children)
            else:
                children.append(n.flatten())

        _flat_node(self.left)
        _flat_node(self.right)

        return FlattenAdd(children)

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        match left, right:
            # 0 + x or x + 0 => x
            case (Numeric(0), other) | (other, Numeric(0)):
                return other

            case Numeric(a), Numeric(b):
                return Numeric(a + b)

        return Add(left, right)


class FlattenAdd(FlattenNode):
    PRECEDENCE = 1

    def __init__(self, chidren: list[FlattenNode]) -> None:
        self.children = chidren

    def constant_fold(self):
        numeric_sum = 0.0
        new_children = []

        for child in self.children:
            folded = child.constant_fold()

            if isinstance(folded, FlattenNumeric):
                numeric_sum += folded.value
            else:
                new_children.append(folded)

        if numeric_sum != 0 or not new_children:
            new_children.append(FlattenNumeric(numeric_sum))

        if len(new_children) == 1:
            return new_children[0]

        return FlattenAdd(new_children)

    def __str__(self) -> str:
        parts = []
        for c in self.children:
            if isinstance(c, FlattenNumeric) and c.value < 0:
                parts.append(f"- {abs(c.value)}")
            elif isinstance(c, FlattenMul) and c.children[0] == FlattenNumeric(-1):
                parts.append(f"- {c}")
            elif c.precedence() < self.PRECEDENCE:
                parts.append(f"({c})")
            else:
                parts.append(f"+ {c}")

        result = " ".join(parts).strip()
        if result.startswith("+ "):
            result = result[2:]

        return result

    def __eq__(self, other):
        return isinstance(other, FlattenAdd) and self.children == other.children

    def precedence(self):
        return self.PRECEDENCE
