from typing import Optional
from abc import ABC, abstractmethod

from backend.internal.statements.subject import Subject
from backend.internal.expressions import Expression, Infix, Number, Prefix, Identifier


class Node(ABC):
    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Add(self, Mul(other, -1))

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Mul(self, Pow(other, Numeric(-1)))

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def reduce(self):
        pass

class Add(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Add) and self.left == other.left and self.right == other.right

    def __repr__(self):
        return "(" + repr(self.left) + "+" + repr(self.right) + ")"

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        # x + 0 = x
        if isinstance(left, Numeric) and left.value == 0:
            return right

        # 0 + x = x
        if isinstance(right, Numeric) and right.value == 0:
            return left

        if isinstance(left, Numeric) and isinstance(right, Numeric):
            return Numeric(left.value + right.value)

        return Add(left, right)


class Mul(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Mul) and self.left == other.left and self.right == other.right

    def __repr__(self):
        return "(" + repr(self.left) + "*" + repr(self.right) + ")"
    
    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        # x * 0 -> 0
        if isinstance(left, Numeric) and left.value == 0:
            return Numeric(0)

        # 0 * x -> 0
        if isinstance(right, Numeric) and right.value == 0:
            return Numeric(0)

        # x * 1 -> x
        if isinstance(left, Numeric) and left.value == 1:
            return right

        # 1 * x -> x
        if isinstance(right, Numeric) and right.value == 1:
            return left

        # 2 + 2 -> 4
        if isinstance(left, Numeric) and isinstance(right, Numeric):
            return Numeric(left.value * right.value)

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
        return isinstance(other, Pow) and self.base == other.base and self.exponent == other.exponent

    def __repr__(self):
        return "(" + repr(self.base) + "^" + str(self.exponent) + ")"
    
    def reduce(self) -> Node:
        base = self.base.reduce()
        exponent = self.exponent.reduce()

        # x^0 -> 1
        if isinstance(exponent, Numeric) and exponent.value == 0:
            return Numeric(1)
        # x^1 -> x
        if isinstance(exponent, Numeric) and exponent.value == 1:
            return base

        return Pow(base, exponent)


def convert_to_expression_tree(expression: Expression) -> Node:
    if Subject is None:
        return None

    root: Optional[Node] = None
    if expression is None:
        return None

    if isinstance(expression, Infix):
        operator = expression.operator().literal
        match operator:
            case '+':
                root = Add(convert_to_expression_tree(expression.left()), convert_to_expression_tree(expression.right()))
            case '-':
                root = Add(convert_to_expression_tree(expression.left()), Mul(convert_to_expression_tree(expression.right()), Numeric(-1)))
            case '*':
                root = Mul(convert_to_expression_tree(expression.left()), convert_to_expression_tree(expression.right()))
            case '/':
                root = Mul(convert_to_expression_tree(expression.left()), Pow(convert_to_expression_tree(expression.right()), Numeric(-1)))
            case '^':
                root = Pow(convert_to_expression_tree(expression.left()), convert_to_expression_tree(expression.right()))
            case _:
                raise ValueError(f"Unknown operator: {expression.operator().literal}")
    
    if isinstance(expression, Prefix):
        match expression.operator().literal:
            case '-':
                root = Mul(convert_to_expression_tree(expression._expr), Numeric(-1))
            case _:
                raise ValueError(f"Unknown operator: {expression.operator().literal}")
    
    if isinstance(expression, Number):
       root = Numeric(expression.value)
    
    if isinstance(expression, Identifier):
        root = Symbol(expression.pretty_str())

    return root
