from abc import ABC
from typing import Optional

from backend.internal.expressionTree import Node


class Object(ABC):
    pass


class TransformObject(Object):
    operator: str
    transform: Node

    def __init__(self, operator: str, transform: Node) -> None:
        self.operator = operator
        self.transform = transform

    def __repr__(self) -> str:
        return f"Transform({self.operator}, {repr(self.transform)})"


class SubjectObject(Object):
    lhs: Node
    rhs: Optional[Node]

    def __init__(self, lhs: Node, rhs: Optional[Node]) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        if self.is_equation():
            return f"{repr(self.lhs)} = {repr(self.rhs)}"
        return f"{repr(self.lhs)}"

    def __str__(self) -> str:
        if self.is_equation():
            return f"{str(self.lhs)} = {str(self.rhs)}"
        return f"{str(self.lhs)}"

    def is_equation(self) -> bool:
        return self.rhs is not None

    def transform(self, operator: str, transform: Node) -> None:
        match operator:
            case "+":
                self.lhs += transform
                if self.is_equation():
                    self.rhs += transform
            case "-":
                self.lhs -= transform
                if self.is_equation():
                    self.rhs -= transform
            case "*":
                self.lhs *= transform
                if self.is_equation():
                    self.rhs *= transform
            case "/":
                self.lhs /= transform
                if self.is_equation():
                    self.rhs /= transform
            case _:
                raise ValueError(f"Unknown operator: {operator}")
