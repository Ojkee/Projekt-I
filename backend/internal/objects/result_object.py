from abc import ABC, abstractmethod
from backend.internal.objects import Object
from backend.internal.expression_tree.node import Node


class SubjectObject(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def transform(self, operator: str, transform: Node) -> None:
        pass


class ExpressionObject(SubjectObject):
    value: Node

    def __init__(self, value: Node) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"EXPR({repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    def transform(self, operator: str, transform: Node) -> None:
        match operator:
            case "+":
                self.value += transform
            case "-":
                self.value -= transform
            case "*":
                self.value *= transform
            case "/":
                self.value /= transform
            case _:
                raise ValueError(f"Unknown operator: {operator}")


class EquationObject(SubjectObject):
    lhs: Node
    rhs: Node

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        return f"EQUATION({repr(self.rhs)} = {repr(self.lhs)})"

    def __str__(self) -> str:
        return f"{str(self.lhs)} = {str(self.rhs)}"

    def transform(self, operator: str, transform: Node) -> None:
        match operator:
            case "+":
                self.lhs += transform
                self.rhs += transform
            case "-":
                self.lhs -= transform
                self.rhs -= transform
            case "*":
                self.lhs *= transform
                self.rhs *= transform
            case "/":
                self.lhs /= transform
                self.rhs /= transform
            case _:
                raise ValueError(f"Unknown operator: {operator}")


class ErrorObject(SubjectObject):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def __repr__(self) -> str:
        return f"ERROR: {self.msg}"

    def __str__(self) -> str:
        return self.msg

    def transform(self, operator: str, transform: Node) -> None:
        _ = operator
        _ = transform
        pass
