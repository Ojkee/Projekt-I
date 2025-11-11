from abc import ABC, abstractmethod
from typing import Generator
from backend.internal.expression_tree import Node, Add, Numeric, Mul, Pow
from backend.internal.objects import Object
from backend.internal.tokens import Token
from backend.internal.tokens.token import TokenType


class TransformObject(Object, ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass


class AtomTransformObject(TransformObject):
    def __init__(self, operator: Token, transform: Node) -> None:
        super().__init__()
        self.operator = operator
        self.transform = transform

    def __iter__(self) -> Generator[Node]:
        match self.operator.ttype:
            case TokenType.PLUS:
                yield Add(Numeric(0), self.transform)
            case TokenType.MINUS:
                yield Add(Numeric(0), Mul(self.transform, Numeric(-1)))
            case TokenType.ASTERISK:
                yield Mul(Numeric(1), self.transform)
            case TokenType.SLASH:
                yield Mul(Numeric(1), Pow(self.transform, Numeric(-1)))
            case TokenType.CARET:
                yield Pow(self.transform, Numeric(1))

        yield from ()

    def __repr__(self) -> str:
        return f"ATOM({repr(self.operator)}, {repr(self.transform)})"


class FormulaObject(TransformObject):
    def __init__(self, name: Token, params: list[Node]) -> None:
        super().__init__()
        self.name = name
        self.params: list[Node] = params

    def __repr__(self) -> str:
        params_repr = ", ".join(map(repr, self.params))
        return f"{repr(self.name)}({params_repr})"

    def __iter__(self) -> Generator[Node]:
        return (param for param in self.params)
