from typing import NamedTuple
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Node, Pow, Mul, Add


class FormulaEntry(NamedTuple):
    latex_str: str
    to_match: Node
    replacement: Node


FORMULA_MAP: dict[str, FormulaEntry] = {
    "product_power_rule": FormulaEntry(
        "a^x * a^y = a^{x + y}",
        Mul(Pow(WildNode("a"), WildNode("x")), Pow(WildNode("a"), WildNode("y"))),
        Pow(WildNode("a"), Add(WildNode("x"), WildNode("y"))),
    ),
}


def get_implemented_formulas() -> list[tuple[str, str]]:
    return [(name, entry.latex_str) for name, entry in FORMULA_MAP.items()]
