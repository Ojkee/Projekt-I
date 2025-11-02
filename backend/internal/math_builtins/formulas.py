from typing import NamedTuple
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Node, Pow, Mul, Add


class FormulaEntry(NamedTuple):
    latex_str: str
    lhs: Node
    rhs: Node


FORMULA_MAP: dict[str, FormulaEntry] = {
    "product_power_rule": FormulaEntry(
        r"a^r \cdot a^s = a^{r + s}",
        Mul(Pow(WildNode("a"), WildNode("r")), Pow(WildNode("a"), WildNode("s"))),
        Pow(WildNode("a"), Add(WildNode("r"), WildNode("s"))),
    ),
    "power_product_rule": FormulaEntry(
        r"(a^r)^s = a^{r \cdot s}",
        Pow(Pow(WildNode("a"), WildNode("r")), WildNode("s")),
        Pow(WildNode("a"), Mul(WildNode("r"), WildNode("s"))),
    ),
    # "quotient_power_rule": FormulaEntry(
    #     r"\frac{ a^r }{ a^s }", WildNode("TODO"), WildNode("TODO")
    # ),
    "power_of_product_rule": FormulaEntry(
        r"( a \cdot b) ^ r",
        Pow(Mul(WildNode("a"), WildNode("b")), WildNode("r")),
        Mul(Pow(WildNode("a"), WildNode("r")), Pow(WildNode("b"), WildNode("r"))),
    ),
    # "power_quotient_rule": FormulaEntry(
    #     r"\frac{ a^r }{ a^s }", WildNode("TODO"), WildNode("TODO")
    # ),
}


def get_implemented_formulas() -> list[tuple[str, str]]:
    return [(name, entry.latex_str) for name, entry in FORMULA_MAP.items()]
