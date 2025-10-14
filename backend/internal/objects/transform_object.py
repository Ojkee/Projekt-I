from backend.internal.expression_tree import Node
from backend.internal.objects import Object
from backend.internal.tokens import Token


class TransformObject(Object):
    pass


class AtomTransformObject(TransformObject):
    def __init__(self, operator: Token, transform: Node) -> None:
        super().__init__()
        self.operator = operator
        self.transform = transform

    def __repr__(self) -> str:
        return f"Transform({repr(self.operator)}, {repr(self.transform)})"
