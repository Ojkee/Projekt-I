from typing import Optional
from backend.internal.objects import Object
from backend.internal.expression_tree.node import Node


class ExpressionObject(Object):
    expr: Node

    def __init__(self, value: Node) -> None:
        super().__init__()
        self.value = value


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
                if self.rhs:
                    self.rhs += transform
            case "-":
                self.lhs -= transform
                if self.rhs:
                    self.rhs -= transform
            case "*":
                self.lhs *= transform
                if self.rhs:
                    self.rhs *= transform
            case "/":
                self.lhs /= transform
                if self.rhs:
                    self.rhs /= transform
            case _:
                raise ValueError(f"Unknown operator: {operator}")


class ErrorObject(Object):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg
