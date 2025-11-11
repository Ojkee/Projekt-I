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

    def flatten(self) -> FlattenNode:
        childrens: list[FlattenNode] = []

        def _flat_node(n: Node) -> list[FlattenNode]:
            if isinstance(n, Add):
                flat = n.flatten()
                childrens.extend(flat.childrens)
            else:
                childrens.append(n.flatten())

        _flat_node(self.left)
        _flat_node(self.right)

        return FlattenAdd(childrens)

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        match left, right:
            # 0 + x or x + 0 => x
            case (Numeric(value=0), other) | (other, Numeric(value=0)):
                return other

            case Numeric(value=lvalue), Numeric(value=rvalue):
                return Numeric(lvalue + rvalue)

        return Add(left, right)



class FlattenAdd(FlattenNode):
    PRECEDENCE = 1

    def __init__(self, childrens: list[FlattenNode]) -> None:
        self.childrens = childrens

    def constant_fold(self):
        numeric_sum = 0.0
        childrens_to_remove = []

        for child in self.childrens:
            child.constant_fold()
            if isinstance(child, FlattenNumeric):
                numeric_sum += child.value
                childrens_to_remove.append(child)

        for child in childrens_to_remove:
            self.childrens.remove(child)

        self.childrens.append(FlattenNumeric(numeric_sum))

        if len(self.childrens) == 1:
            return self.childrens[0]

        return self

    def __str__(self) -> str:
        parts = []
        for c in self.childrens:
            if isinstance(c, FlattenNumeric) and c.value < 0:
                parts.append(f"- {abs(c.value)}")
            elif isinstance(c, FlattenMul) and c.childrens[0] == FlattenNumeric(-1):
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
        return (isinstance(other, FlattenAdd) and self.childrens == other.childrens)

    def precedence(self):
        return self.PRECEDENCE