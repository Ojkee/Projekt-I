from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod

from backend.internal.expressions import Expression, Infix, Number, Prefix, Identifier
from backend.internal.tokens.token import Token, TokenType


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

    def __pow__(self, other):
        return Pow(self, other)

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
    __match_args__ = ("left", "right")

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
            # 0 * (0 ^ x) => 0 * (0 ^ x) for x > 0
            case Numeric(0), Pow(Numeric(0), Numeric(b)) if b < 0:
                return Mul(left, right)

            # 0*x or x*0 => 0
            case (Numeric(0), _) | (_, Numeric(0)):
                return Numeric(0)

            # 1*x or x*1  => x
            case (Numeric(1), other) | (other, Numeric(1)):
                return other

            case Numeric(lhs), Numeric(rhs):
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
    __match_args__ = ("value",)

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Numeric) and self.value == other.value

    def __repr__(self):
        return str(self.value)

    def reduce(self) -> Node:
        return self


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
        return "(" + repr(self.base) + "^" + str(self.exponent) + ")"

    def reduce(self) -> Node:
        base = self.base.reduce()
        exponent = self.exponent.reduce()

        match base, exponent:
            # x^0 => 1
            case _, Numeric(0):
                return Numeric(1)

            # x^1 => x
            case _, Numeric(1):
                return base

            case Numeric(a), Numeric(b) if 0 < a:
                return Numeric(a**b)

        return Pow(base, exponent)


def convert_to_expression_tree(expression: Optional[Expression]) -> Optional[Node]:
    if expression is None:
        return None

    match expression:
        case Infix(_op=Token(TokenType.PLUS), _lhs=left, _rhs=right):
            lhs = convert_to_expression_tree(left)
            rhs = convert_to_expression_tree(right)
            assert lhs and rhs, "lhs and rhs must be not None"
            return Add(lhs, rhs)
        case Infix(_op=Token(TokenType.MINUS), _lhs=left, _rhs=right):
            lhs = convert_to_expression_tree(left)
            rhs = convert_to_expression_tree(right)
            assert rhs, "rhs must be not None"
            negation = Mul(rhs, Numeric(-1))
            assert lhs and negation, "lhs and rhs must be not None"
            return Add(lhs, negation)
        case Infix(_op=Token(TokenType.ASTERISK), _lhs=left, _rhs=right):
            lhs = convert_to_expression_tree(left)
            rhs = convert_to_expression_tree(right)
            assert lhs and rhs, "lhs and rhs must be not None"
            return Mul(lhs, rhs)
        case Infix(_op=Token(TokenType.SLASH), _lhs=left, _rhs=right):
            lhs = convert_to_expression_tree(left)
            inverse_base = convert_to_expression_tree(right)
            assert inverse_base, "inverse base must be not None"
            rhs = Pow(inverse_base, Numeric(-1))
            assert lhs and rhs, "lhs and rhs must be not None"
            return Mul(lhs, rhs)
        case Infix(_op=Token(TokenType.CARET), _lhs=left, _rhs=right):
            base = convert_to_expression_tree(left)
            exponent = convert_to_expression_tree(right)
            assert base and exponent, "base and exponent must be not None"
            return Pow(base, exponent)

        case Prefix(_op=Token(TokenType.MINUS), _expr=expr):
            inner_mul = convert_to_expression_tree(expr)
            assert inner_mul
            return Mul(inner_mul, Numeric(-1))

        case Number(value=value):
            return Numeric(value)

        case Identifier(name=Token(_, literal)):
            return Symbol(literal)

    return None
