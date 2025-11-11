from backend.internal.expression_tree import Node, FlattenNode
from backend.internal.expression_tree.numeric_node import FlattenNumeric, Numeric


class Mul(Node):
    __match_args__ = ("left", "right")

    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

        self.childrens = []

    def __eq__(self, other):
        return (
            isinstance(other, Mul)
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        print(repr(self.left), type(self.left))
        return "(" + repr(self.left) + "*" + repr(self.right) + ")"

    def flatten(self) -> FlattenNode:
        childrens = []

        def _flat_node(n: Node) -> list[FlattenNode]:
            if isinstance(n, Mul):
                flat = n.flatten()
                childrens.extend(flat.childrens)
            else:
                childrens.append(n.flatten())

        _flat_node(self.left)
        _flat_node(self.right)

        return FlattenMul(childrens)

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        match left, right:
            # 0*x or x*0 => 0
            case (Numeric(value=0), _) | (_, Numeric(value=0)):
                return Numeric(0)

            # 1*x or x*1  => x
            case (Numeric(value=1), other) | (other, Numeric(value=1)):
                return other

            case Numeric(value=lhs), Numeric(value=rhs):
                return Numeric(lhs * rhs)

        return Mul(left, right)

class FlattenMul(FlattenNode):
    PRECEDENCE = 2
    def __init__(self, childrens: list[FlattenNode]) -> None:
        self.childrens = childrens

    def constant_fold(self) -> FlattenNode:
        numeric_product = 1.0
        childrens_to_remove = []

        for child in self.childrens:
            child.constant_fold()
            if isinstance(child, FlattenNumeric):
                numeric_product *= child.value
                childrens_to_remove.append(child)

        for child in childrens_to_remove:
            self.childrens.remove(child)

        self.childrens.append(FlattenNumeric(numeric_product))

        if len(self.childrens) == 1:
            return self.childrens[0]

        return self

    def __str__(self) -> str:
        parts = []
        is_negative = (isinstance(self.childrens[0], FlattenNumeric) and self.childrens[0] == FlattenNumeric(-1))
        start = 1 if is_negative else 0
    
        for c in self.childrens[start:]:
            print(type(c), c)
            if is_negative and isinstance(c, FlattenNumeric) and c.value < 0: # example case: x - (-3)
                parts.append(f"({c.value})")
            elif c.precedence() < self.PRECEDENCE:
                parts.append(f"({c})")
            else:
                parts.append(f"{c}")
        

        return " * ".join(parts)

    def __eq__(self, other):
        return (isinstance(other, FlattenMul) and self.childrens == other.childrens)

    def precedence(self):
        return self.PRECEDENCE