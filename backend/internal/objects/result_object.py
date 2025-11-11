from abc import ABC, abstractmethod
from typing import Callable, Generator, NamedTuple
from backend.internal.math_builtins import BuiltIns
from backend.internal.expression_tree import Node, Add, Mul, Pow
from backend.internal.math_builtins.builtins_error import BuiltinsError
from backend.internal.objects import TransformObject, AtomTransformObject
from backend.internal.objects import Object
from backend.internal.objects.transform_object import FormulaObject
from backend.internal.tokens.token import TokenType


TransformFn = Callable[[Node, TransformObject], Node | None]


class SubjectObject(Object, ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __iter__(self) -> Generator[Node]:
        pass

    @abstractmethod
    def apply(self, t_obj: TransformObject) -> None:
        pass

    def _get_transformer(self, t_obj: TransformObject) -> TransformFn:
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
            case TokenType.CARET:
                return (value) ** (atom.transform)
            case _:
                assert False, "Unreachable"

    def _handle_formula(self, value: Node, formula: TransformObject) -> Node | None:
        assert isinstance(formula, FormulaObject)

        ParamToReplace = NamedTuple(
            "ParamToReplace",
            [
                ("param", Node),
                ("replacement", Node),
            ],
        )
        replacements = BuiltIns.get_replacements(
            formula.name.literal,
            value,
            formula.params,
            lambda p, r: ParamToReplace(p, r),
        )

        if isinstance(replacements, BuiltinsError):
            return None

        def dfs_replace(node: Node, param: Node, replacement: Node) -> Node:
            if node == param:
                return replacement
            match node:
                case (
                    Add(left=lhs, right=rhs)
                    | Mul(left=lhs, right=rhs)
                    | Pow(base=lhs, exponent=rhs) as N
                ):
                    return type(N)(
                        dfs_replace(lhs, param, replacement),
                        dfs_replace(rhs, param, replacement),
                    )
            return node

        def replace(param: Node, replacement: Node) -> None:
            nonlocal value
            value = dfs_replace(value, param, replacement)

        for replacement in replacements:
            replace(*replacement)

        return value


class ExpressionObject(SubjectObject):
    value: Node

    def __init__(self, value: Node) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"EXPR({repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    def __iter__(self) -> Generator[Node]:
        return (i for i in (self.value,))

    def apply(self, t_obj: TransformObject) -> None:
        transformer = self._get_transformer(t_obj)
        if result := transformer(self.value, t_obj):
            self.value = result
        else:
            raise ValueError(f"Can't transform {str(t_obj)} on {str(self)}")


class EquationObject(SubjectObject):
    lhs: Node
    rhs: Node

    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        return f"EQUATION({repr(self.lhs)} = {repr(self.rhs)})"

    def __str__(self) -> str:
        return f"{str(self.lhs)} = {str(self.rhs)}"

    def __iter__(self) -> Generator[Node]:
        return (i for i in (self.lhs, self.rhs))

    def apply(self, t_obj: TransformObject) -> None:
        transformer = self._get_transformer(t_obj)

        result_lhs = transformer(self.lhs, t_obj)
        result_rhs = transformer(self.rhs, t_obj)

        if not (result_lhs or result_rhs):
            raise ValueError(f"Can't transform {str(t_obj)} on {str(self)}")

        if result_lhs:
            self.lhs = result_lhs
        if result_rhs:
            self.rhs = result_rhs


class ErrorObject(SubjectObject):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def __repr__(self) -> str:
        return f"ERROR: {self.msg}"

    def __str__(self) -> str:
        return self.msg

    def __eq__(self, value, /) -> bool:
        return isinstance(value, ErrorObject) and self.msg == value.msg

    def __iter__(self) -> Generator[Node]:
        yield from ()

    def apply(self, t_obj: TransformObject) -> None:
        _ = t_obj
        assert False, "Can't transform error"
