from backend.internal.expression_tree import Node


class WildNode(Node):
    tag: str

    def __init__(self, tag: str) -> None:
        super().__init__()
        self.tag = tag

    def __eq__(self, other) -> bool:
        _ = other
        return True

    def __repr__(self) -> str:
        return f"WILDNODE({self.tag!r})"

    def reduce(self) -> Node:
        return self
