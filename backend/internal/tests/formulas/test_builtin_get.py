import pytest
from typing import NamedTuple

from backend.internal.expression_tree import Node, Mul, Add, Numeric, Symbol, Pow
from backend.internal.math_builtins.lookups import BuiltIns


class Case(NamedTuple):
    name: str
    formula_name: str
    root: Node
    param: Node
    expected: Node


CASES_BUILTIN_GET: list[Case] = [
    Case(
        name="Product Power Rule",
        formula_name="product_power_rule",
        root=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
    Case(
        name="Product Power Rule nested lhs",
        formula_name="product_power_rule",
        root=Add(
            Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
            Symbol("b"),
        ),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
    Case(
        name="Product Power Rule nested rhs",
        formula_name="product_power_rule",
        root=Add(
            Symbol("b"),
            Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        ),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
]


@pytest.mark.parametrize("case", CASES_BUILTIN_GET, ids=lambda c: c.name)
def test_builtin_get(case: Case) -> None:
    result = BuiltIns.get(case.formula_name, case.root, case.param)
    assert result == case.expected
