from backend.internal.expression_tree import Node


class WildNode(Node):
    def __init__(self, tag: str) -> None:
        super().__init__()
        self.tag = tag

    __match_args__ = ("tag",)

    def __eq__(self, other: Node) -> bool:
        _ = other
        return True

    def __repr__(self) -> str:
        return f"WILDNODE({self.tag!r})"

    def reduce(self) -> Node:
        return self


class WildNodeFraction(Node):
    pass
