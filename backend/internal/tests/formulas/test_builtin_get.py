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


CASES_BUILTIN_GET_REPLACEMENT: list[Case] = [
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

CASES_BUILTIN_GET_REPLACEMENT_REVERSED: list[Case] = [
    Case(
        name="Reversed Product Power Rule",
        formula_name="product_power_rule",
        root=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
    Case(
        name="Reversed Product Power Rule nested lhs",
        formula_name="product_power_rule",
        root=Add(
            Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
            Symbol("b"),
        ),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
    Case(
        name="Reversed Product Power Rule nested rhs",
        formula_name="product_power_rule",
        root=Add(
            Symbol("b"),
            Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        ),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
]

CASES_BUILTIN_GET_REPLACEMENT_UT: list[Case] = []
CASES_BUILTIN_GET_REPLACEMENT_UT.extend(CASES_BUILTIN_GET_REPLACEMENT)
CASES_BUILTIN_GET_REPLACEMENT_UT.extend(CASES_BUILTIN_GET_REPLACEMENT_REVERSED)


@pytest.mark.parametrize("case", CASES_BUILTIN_GET_REPLACEMENT_UT, ids=lambda c: c.name)
def test_builtin_get(case: Case) -> None:
    replacement = BuiltIns.get_replacement(case.formula_name, case.root, case.param)
    assert replacement == case.expected
