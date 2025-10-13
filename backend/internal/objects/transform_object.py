from backend.internal.expression_tree import Node
from backend.internal.objects import Object


class TransformObject(Object):
    operator: str
    transform: Node

    def __init__(self, operator: str, transform: Node) -> None:
        self.operator = operator
        self.transform = transform

    def __repr__(self) -> str:
        return f"Transform({self.operator}, {repr(self.transform)})"
