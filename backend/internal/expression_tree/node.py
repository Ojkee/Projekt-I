from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod

from backend.internal.expressions import Expression, Infix, Number, Prefix, Identifier
from backend.internal.tokens.token import Token, TokenType

class Node(ABC):
    def __init__(self) -> None:
        super().__init__()

    def __add__(self, other):
        from backend.internal.expression_tree import Add
        return Add(self, other)

    def __sub__(self, other):
        from backend.internal.expression_tree import Add, Mul, Numeric
        return Add(self, Mul(Numeric(-1), other))

    def __mul__(self, other):
        from backend.internal.expression_tree import Mul
        return Mul(self, other)

    def __truediv__(self, other):
        from backend.internal.expression_tree import Mul, Numeric, Pow
        return Mul(self, Pow(other, Numeric(-1)))

    def __pow__(self, other):
        from backend.internal.expression_tree import Pow
        return Pow(self, other)

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def reduce(self) -> Node: # Will be removed and implemented in FlattenNode
        pass

    @abstractmethod
    def flatten(self) -> FlattenNode:
        pass


class FlattenNode(ABC):
    #@abstractmethod
    #def canonicical_form(self)
    #    pass`

    @abstractmethod
    def __str__(self) -> str:
        pass    

    @abstractmethod
    def constant_fold(self) -> FlattenNode:
        """
        Performs constant folding on the expression tree node.

        - If the node has child nodes that can be constant folded, it recursively
          applies constant folding to those child nodes.

        - If the node represents a numeric operation (e.g., addition, multiplication)
          and both operands are numeric constants, it computes the result and
          replaces the node with a single numeric constant node.
        
        Example:
            For an addition node with two numeric children (3 + 5 + 12), it will replace
            the addition node with a single numeric node representing the value 20.

        Returns:
            FlattenNode: A new FlattenNode that represents the constant-folded expression.
        """
        pass

#    @abstractmethod
#    def reduce(self):
#        pass

#    @abstractmethod
#    def simplify(self):
#        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def precedence(self) -> int:
        pass


def convert_to_expression_tree(expression: Optional[Expression]) -> Optional[Node]:
    from backend.internal.expression_tree import Mul, Numeric, Add, Pow, Symbol
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
