from collections.abc import Mapping
from backend.internal.math_builtins.formula_handler import FORMULA_MAP
from backend.internal.math_builtins.formula_entry import FormulaEntry
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Pow, Mul, Add


_FORMULAS_POWER: Mapping[str, FormulaEntry] = {
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
        r"\frac{ a^r }{ a^s } = a^{r - s}",
        WildNode("TODO"),
        WildNode("TODO"),
    ),
    "power_of_a_product": FormulaEntry(
        "Power of a Product rule",
        r"( a \cdot b) ^ r",
        Pow(Mul(WildNode("a"), WildNode("b")), WildNode("r")),
        Mul(Pow(WildNode("a"), WildNode("r")), Pow(WildNode("b"), WildNode("r"))),
    ),
    "power_of_a_quotient": FormulaEntry(
        "Power of a Quotient",
        r"\frac{ a^r }{ a^s }",
        WildNode("TODO"),
        WildNode("TODO"),
    ),
}


@FORMULA_MAP.formula_category("Powers")
def formula_powers_fn() -> Mapping[str, FormulaEntry]:
    return _FORMULAS_POWER
