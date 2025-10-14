from abc import ABC, abstractmethod
from backend.internal.expression_tree.node import Node
from backend.internal.objects import TransformObject, AtomTransformObject
from backend.internal.objects import Object
from backend.internal.tokens.token import TokenType


class SubjectObject(Object, ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def transform(self, t_obj: TransformObject) -> None:
        pass

    def _handle_atom_transform(self, value: Node, atom: AtomTransformObject) -> Node:
        match atom.operator.ttype:
            case TokenType.PLUS:
                return value + atom.transform
            case TokenType.MINUS:
                return value - atom.transform
            case TokenType.ASTERISK:
                return value * atom.transform
            case TokenType.SLASH:
                return value / atom.transform
            case _:
                raise ValueError(f"Unknown atom operator: {repr(atom.operator)}")


class ExpressionObject(SubjectObject):
    value: Node

    def __init__(self, value: Node) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"EXPR({repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    def transform(self, t_obj: TransformObject) -> None:
        match t_obj:
            case AtomTransformObject() as atom:
                self.value = self._handle_atom_transform(self.value, atom)
            case _:
                raise ValueError(f"Unimplemented transformation: {repr(t_obj)}")
        self.value.reduce()


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

    def transform(self, t_obj: TransformObject) -> None:
        match t_obj:
            case AtomTransformObject() as atom:
                self.lhs = self._handle_atom_transform(self.lhs, atom)
                self.rhs = self._handle_atom_transform(self.rhs, atom)
            case _:
                raise ValueError(f"Unimplemented transformation: {repr(t_obj)}")
        self.lhs.reduce()
        self.rhs.reduce()


class ErrorObject(SubjectObject):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def __repr__(self) -> str:
        return f"ERROR: {self.msg}"

    def __str__(self) -> str:
        return self.msg

    def transform(self, t_obj: TransformObject) -> None:
        _ = t_obj
        assert False, "Can't transform error"
