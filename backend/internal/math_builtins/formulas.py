from typing import NamedTuple
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Node, Pow, Mul, Add


class FormulaEntry(NamedTuple):
    display_name: str
    latex_str: str
    lhs: Node
    rhs: Node


FORMULA_MAP: dict[str, FormulaEntry] = {
    "product_of_powers": FormulaEntry(
        "Product of powers rule",
        r"a^r \cdot a^s = a^{r + s}",
        Mul(Pow(WildNode("a"), WildNode("r")), Pow(WildNode("a"), WildNode("s"))),
        Pow(WildNode("a"), Add(WildNode("r"), WildNode("s"))),
    ),
    "power_of_a_power": FormulaEntry(
        "Power of a power rule",
        r"(a^r)^s = a^{r \cdot s}",
        Pow(Pow(WildNode("a"), WildNode("r")), WildNode("s")),
        Pow(WildNode("a"), Mul(WildNode("r"), WildNode("s"))),
    ),
    "quotient_of_powers": FormulaEntry(
        "Quotient of Powers",
        r"\frac{ a^r }{ a^s }",
        WildNode("TODO"),
        WildNode("TODO"),
    ),
    "power_of_a_product": FormulaEntry(
        "Power of a Product rule",
        r"( a \cdot b) ^ r",
        Pow(Mul(WildNode("a"), WildNode("b")), WildNode("r")),
        Mul(Pow(WildNode("a"), WildNode("r")), Pow(WildNode("b"), WildNode("r"))),
    ),
    # "power_of_a_quotient": FormulaEntry(
    #     r"\frac{ a^r }{ a^s }", WildNode("TODO"), WildNode("TODO")
    # ),
}
