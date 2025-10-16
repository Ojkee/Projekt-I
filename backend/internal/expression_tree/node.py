from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod

from backend.internal.expressions import Expression, Infix, Number, Prefix, Identifier


class Node(ABC):
    def __init__(self) -> None:
        super().__init__()

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Add(self, Mul(other, Numeric(-1)))

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Mul(self, Pow(other, Numeric(-1)))

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def reduce(self) -> Node:
        pass


class Add(Node):
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


class Mul(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            isinstance(other, Mul)
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        return "(" + repr(self.left) + "*" + repr(self.right) + ")"

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


class Symbol(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __repr__(self):
        return self.name

    def reduce(self) -> Node:
        return self


class Numeric(Node):
    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Numeric) and self.value == other.value

    def __repr__(self):
        return str(self.value)

    def reduce(self) -> Node:
        return self


class Pow(Node):
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
        return "(" + repr(self.base) + "^" + str(self.exponent) + ")"

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


# TODO: refactor
def convert_to_expression_tree(expression: Optional[Expression]) -> Optional[Node]:
    if expression is None:
        return None

    root: Optional[Node] = None

    if isinstance(expression, Infix):
        operator = expression.operator().literal
        match operator:
            case "+":
                lhs = convert_to_expression_tree(expression.left())
                rhs = convert_to_expression_tree(expression.right())
                assert lhs and rhs, "lhs and rhs must be not None"
                root = Add(lhs, rhs)
            case "-":
                lhs = convert_to_expression_tree(expression.left())
                rhs = convert_to_expression_tree(expression.right())
                assert rhs, "rhs must be not None"
                negation = Mul(rhs, Numeric(-1))
                assert lhs and negation, "lhs and rhs must be not None"
                root = Add(lhs, negation)
            case "*":
                lhs = convert_to_expression_tree(expression.left())
                rhs = convert_to_expression_tree(expression.right())
                assert lhs and rhs, "lhs and rhs must be not None"
                root = Mul(lhs, rhs)
            case "/":
                lhs = convert_to_expression_tree(expression.left())
                inverse_base = convert_to_expression_tree(expression.right())
                assert inverse_base, "inverse base must be not None"
                rhs = Pow(inverse_base, Numeric(-1))
                assert lhs and rhs, "lhs and rhs must be not None"
                root = Mul(lhs, rhs)
            case "^":
                base = convert_to_expression_tree(expression.left())
                exponent = convert_to_expression_tree(expression.right())
                assert base and exponent, "base and exponent must be not None"
                root = Pow(base, exponent)
            case _:
                raise ValueError(f"Unknown operator: {expression.operator().literal}")

    if isinstance(expression, Prefix):
        match expression.operator().literal:
            case "-":
                inner_mul = convert_to_expression_tree(expression._expr)
                assert inner_mul
                root = Mul(inner_mul, Numeric(-1))
            case _:
                raise ValueError(f"Unknown operator: {expression.operator().literal}")

    if isinstance(expression, Number):
        root = Numeric(expression.value)

    if isinstance(expression, Identifier):
        root = Symbol(str(expression))

    return root
