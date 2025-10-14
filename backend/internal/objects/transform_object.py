from backend.internal.expression_tree import Node
from backend.internal.objects import Object


class TransformObject(Object):
    pass


class AtomTransformObject(TransformObject):
    def __init__(self, operator: str, transform: Node) -> None:
        super().__init__()
        self.operator = operator
        self.transform = transform

    def __repr__(self) -> str:
        return f"Transform({self.operator}, {repr(self.transform)})"
