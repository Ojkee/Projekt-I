from collections.abc import Mapping
from backend.internal.math_builtins.formula_handler import FORMULA_MAP
from backend.internal.math_builtins.formula_entry import FormulaEntry
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Pow, Mul, Add, Numeric


_FORMULAS_BINOMIAL_IDENTITIES: Mapping[str, FormulaEntry] = {
    "square_of_a_sum": FormulaEntry(
        "Square of a sum",
        r"(a + b)^2 = a^2 + 2ab + b^2",
        Pow(
            Add(WildNode("a"), WildNode("b")),
            Numeric(2),
        ),
        Add(
            Add(
                Pow(WildNode("a"), Numeric(2)),
                Mul(Mul(Numeric(2), WildNode("a")), WildNode("b")),
            ),
            Pow(WildNode("b"), Numeric(2)),
        ),
    ),
    "square_of_a_difference": FormulaEntry(
        "Square of a difference",
        r"(a - b)^2 = a^2 - 2ab + b^2",
        Pow(
            Add(WildNode("a"), Mul(WildNode("b"), Numeric(-1))),
            Numeric(2),
        ),
        Add(
            Add(
                Pow(WildNode("a"), Numeric(2)),
                Mul(
                    Mul(Mul(Numeric(2), WildNode("a")), WildNode("b")),
                    Numeric(-1),
                ),
            ),
            Pow(WildNode("b"), Numeric(2)),
        ),
    ),
    "cube_of_a_sum": FormulaEntry(
        "Cube of a sum",
        r"(a + b)^3 = a^3 + 3a^2b + 3ab^2 + b^3",
        Pow(
            Add(WildNode("a"), WildNode("b")),
            Numeric(3),
        ),
        Add(
            Add(
                Add(
                    Pow(WildNode("a"), Numeric(3)),
                    Mul(Mul(Numeric(3), Pow(WildNode("a"), Numeric(2))), WildNode("b")),
                ),
                Mul(Mul(Numeric(3), WildNode("a")), Pow(WildNode("b"), Numeric(2))),
            ),
            Pow(WildNode("b"), Numeric(3)),
        ),
    ),
    "cube_of_a_difference": FormulaEntry(
        "Cube of a difference",
        r"(a - b)^3 = a^3 - 3a^2b + 3ab^2 - b^3",
        Pow(
            Add(WildNode("a"), Mul(WildNode("b"), Numeric(-1))),
            Numeric(3),
        ),
        Add(
            Add(
                Add(
                    Pow(WildNode("a"), Numeric(3)),
                    Mul(
                        Mul(
                            Mul(Numeric(3), Pow(WildNode("a"), Numeric(2))),
                            WildNode("b"),
                        ),
                        Numeric(-1),
                    ),
                ),
                Mul(Mul(Numeric(3), WildNode("a")), Pow(WildNode("b"), Numeric(2))),
            ),
            Mul(Pow(WildNode("b"), Numeric(3)), Numeric(-1)),
        ),
    ),
    "difference_of_squares": FormulaEntry(
        "Difference of squares",
        r"a^2 - b^2 = (a - b)(a + b)",
        Add(
            Pow(WildNode("a"), Numeric(2)),
            Mul(Pow(WildNode("b"), Numeric(2)), Numeric(-1)),
        ),
        Mul(
            Add(WildNode("a"), Mul(WildNode("b"), Numeric(-1))),
            Add(WildNode("a"), WildNode("b")),
        ),
    ),
    "sum_of_cubes": FormulaEntry(
        "Sum of cubes",
        r"a^3 + b^3 = (a + b)(a^2 - ab + b^2)",
        Add(
            Pow(WildNode("a"), Numeric(3)),
            Pow(WildNode("b"), Numeric(3)),
        ),
        Mul(
            Add(WildNode("a"), WildNode("b")),
            Add(
                Add(
                    Pow(WildNode("a"), Numeric(2)),
                    Mul(Mul(WildNode("a"), WildNode("b")), Numeric(-1)),
                ),
                Pow(WildNode("b"), Numeric(2)),
            ),
        ),
    ),
    "difference_of_cubes": FormulaEntry(
        "Difference of cubes",
        r"a^3 - b^3 = (a - b)(a^2 + ab + b^2)",
        Add(
            Pow(WildNode("a"), Numeric(3)),
            Mul(Pow(WildNode("b"), Numeric(3)), Numeric(-1)),
        ),
        Mul(
            Add(WildNode("a"), Mul(WildNode("b"), Numeric(-1))),
            Add(
                Add(
                    Pow(WildNode("a"), Numeric(2)),
                    Mul(WildNode("a"), WildNode("b")),
                ),
                Pow(WildNode("b"), Numeric(2)),
            ),
        ),
    ),
}


@FORMULA_MAP.formula_category("Binomial Identities")
def formula_powers_fn() -> Mapping[str, FormulaEntry]:
    return _FORMULAS_BINOMIAL_IDENTITIES
