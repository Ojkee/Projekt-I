from typing import NamedTuple

from backend.internal.expression_tree import Node


class FormulaEntry(NamedTuple):
    display_name: str
    latex_str: str
    lhs: Node
    rhs: Node
