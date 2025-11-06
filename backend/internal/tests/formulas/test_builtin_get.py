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


CASES_BUILTIN_GET_REPLACEMENT_POWERS: list[Case] = [
    # "a^r * a^s = a^(r + s)",
    Case(
        name="Product Power Rule",
        formula_name="product_of_powers",
        root=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
    Case(
        name="Product Power Rule nested lhs",
        formula_name="product_of_powers",
        root=Add(
            Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
            Symbol("b"),
        ),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
    Case(
        name="Product Power Rule nested rhs",
        formula_name="product_of_powers",
        root=Add(
            Symbol("b"),
            Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        ),
        param=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
        expected=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
    ),
    Case(
        name="Product Power Rule nested Wildnode lhs",
        formula_name="product_of_powers",
        root=Add(
            Mul(
                Pow(Symbol("a"), Mul(Symbol("x"), Numeric(2.0))),
                Pow(Symbol("a"), Numeric(3.0)),
            ),
            Symbol("b"),
        ),
        param=Mul(
            Pow(Symbol("a"), Mul(Symbol("x"), Numeric(2.0))),
            Pow(Symbol("a"), Numeric(3.0)),
        ),
        expected=Pow(Symbol("a"), Add(Mul(Symbol("x"), Numeric(2.0)), Numeric(3.0))),
    ),
    # "(a^r)^s = a^(r * s)",
    Case(
        name="Power of a Power Rule",
        formula_name="power_of_a_power",
        root=Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b")),
        param=Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b")),
        expected=Pow(Symbol("x"), Mul(Symbol("a"), Symbol("b"))),
    ),
    Case(
        name="Power of a Power Rule nested lhs",
        formula_name="power_of_a_power",
        root=Pow(Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b")), Numeric(33.0)),
        param=Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b")),
        expected=Pow(Symbol("x"), Mul(Symbol("a"), Symbol("b"))),
    ),
    Case(
        name="Power of a Power Rule nested rhs",
        formula_name="power_of_a_power",
        root=Pow(Numeric(33.0), Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b"))),
        param=Pow(Pow(Symbol("x"), Symbol("a")), Symbol("b")),
        expected=Pow(Symbol("x"), Mul(Symbol("a"), Symbol("b"))),
    ),
    Case(
        name="Power of a Power Rule nested lhs",
        formula_name="power_of_a_power",
        root=Pow(
            Pow(Pow(Symbol("x"), Add(Numeric(1.0), Symbol("a"))), Symbol("b")),
            Numeric(33.0),
        ),
        param=Pow(Pow(Symbol("x"), Add(Numeric(1.0), Symbol("a"))), Symbol("b")),
        expected=Pow(Symbol("x"), Mul(Add(Numeric(1.0), Symbol("a")), Symbol("b"))),
    ),
]

CASES_BUILTIN_GET_REPLACEMENT_POWERS_REVERSED: list[Case] = [
    Case(
        name="Reversed Product Power Rule",
        formula_name="product_of_powers",
        root=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
    Case(
        name="Reversed Product Power Rule nested lhs",
        formula_name="product_of_powers",
        root=Add(
            Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
            Symbol("b"),
        ),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
    Case(
        name="Reversed Product Power Rule nested rhs",
        formula_name="product_of_powers",
        root=Add(
            Symbol("b"),
            Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        ),
        param=Pow(Symbol("a"), Add(Numeric(2.0), Numeric(3.0))),
        expected=Mul(Pow(Symbol("a"), Numeric(2.0)), Pow(Symbol("a"), Numeric(3.0))),
    ),
    Case(
        name="Reversed Product Power Rule nested Wildnode lhs",
        formula_name="product_of_powers",
        root=Add(
            Pow(Symbol("a"), Add(Mul(Symbol("x"), Numeric(2.0)), Numeric(3.0))),
            Symbol("b"),
        ),
        param=Pow(Symbol("a"), Add(Mul(Symbol("x"), Numeric(2.0)), Numeric(3.0))),
        expected=Mul(
            Pow(Symbol("a"), Mul(Symbol("x"), Numeric(2.0))),
            Pow(Symbol("a"), Numeric(3.0)),
        ),
    ),
]

CASES_BUILTIN_GET_REPLACEMENT_UT: list[Case] = []
CASES_BUILTIN_GET_REPLACEMENT_UT.extend(CASES_BUILTIN_GET_REPLACEMENT_POWERS)
CASES_BUILTIN_GET_REPLACEMENT_UT.extend(CASES_BUILTIN_GET_REPLACEMENT_POWERS_REVERSED)


@pytest.mark.parametrize("case", CASES_BUILTIN_GET_REPLACEMENT_UT, ids=lambda c: c.name)
def test_builtin_get(case: Case) -> None:
    assert BuiltIns.is_present(case.formula_name)
    replacement = BuiltIns.get_replacement(case.formula_name, case.root, case.param)
    assert replacement == case.expected
