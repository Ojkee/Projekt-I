from abc import ABC, abstractmethod
from typing import Callable
from backend.internal.expression_tree.node import Node
from backend.internal.objects import TransformObject, AtomTransformObject
from backend.internal.objects import Object
from backend.internal.objects.transform_object import FormulaObject
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

    def _get_transformer(
        self, t_obj: TransformObject
    ) -> Callable[[Node, TransformObject], Node]:
        match t_obj:
            case AtomTransformObject():
                return self._handle_atom_transform
            case FormulaObject():
                return self._handle_formula
            case _:
                raise NotImplementedError(f"{type(t_obj)} transform not implemented")

    def _handle_atom_transform(self, value: Node, atom: TransformObject) -> Node:
        assert isinstance(atom, AtomTransformObject)
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

    def _handle_formula(self, value: Node, formula: TransformObject) -> Node:
        assert isinstance(formula, FormulaObject)
        _ = value
        _ = formula
        raise NotImplementedError()


class ExpressionObject(SubjectObject):
    value: Node

    def __init__(self, value: Node) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"EXPR({repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    def transform(self, t_obj: TransformObject) -> None:
        transformer = self._get_transformer(t_obj)
        self.value = transformer(self.value, t_obj)
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
        transformer = self._get_transformer(t_obj)
        self.lhs = transformer(self.lhs, t_obj)
        self.rhs = transformer(self.rhs, t_obj)
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
