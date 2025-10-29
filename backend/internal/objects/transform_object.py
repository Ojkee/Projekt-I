from abc import ABC, abstractmethod
from backend.internal.expression_tree import Node
from backend.internal.objects import Object
from backend.internal.tokens import Token


class TransformObject(Object, ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass


class AtomTransformObject(TransformObject):
    def __init__(self, operator: Token, transform: Node) -> None:
        super().__init__()
        self.operator = operator
        self.transform = transform

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
