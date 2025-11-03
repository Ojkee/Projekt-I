import pytest
import copy
from backend.internal.expression_tree import Node, Add, Numeric, Symbol, Mul, Pow
from backend.internal.math_builtins import BuiltIns
from typing import Callable, NamedTuple


class Case(NamedTuple):
    name: str
    node: Callable | Node
    to_find: Node
    should_find: bool


FIND_MATCH_CASES = [
    Case(
        name="simple_lhs",
        node=lambda tf: Add(tf, Numeric(4.0)),
        to_find=Numeric(3.0),
        should_find=True,
    ),
    Case(
        name="simple_rhs",
        node=lambda tf: Add(Numeric(4.0), tf),
        to_find=Numeric(3.0),
        should_find=True,
    ),
    Case(
        name="simple_not_found",
        node=Add(Numeric(4.0), Numeric(3.0)),
        to_find=Numeric(5.0),
        should_find=False,
    ),
    Case(
        name="complex_lhs",
        node=lambda tf: Add(tf, Numeric(4.0)),
        to_find=Mul(Symbol("x"), Add(Symbol("y"), Numeric(5.0))),
        should_find=True,
    ),
    Case(
        name="complex_rhs",
        node=lambda tf: Add(Numeric(4.0), tf),
        to_find=Mul(Symbol("x"), Add(Symbol("y"), Numeric(5.0))),
        should_find=True,
    ),
    Case(
        name="complex_not_found",
        node=Add(Mul(Symbol("x"), Symbol("y")), Mul(Numeric(4.0), Numeric(3.0))),
        to_find=Numeric(5.0),
        should_find=False,
    ),
    Case(
        name="nested_deep_lhs",
        node=lambda tf: Add(Mul(tf, Numeric(2.0)), Numeric(4.0)),
        to_find=Symbol("x"),
        should_find=True,
    ),
    Case(
        name="nested_deep_rhs",
        node=lambda tf: Add(Numeric(4.0), Mul(Numeric(2.0), tf)),
        to_find=Symbol("x"),
        should_find=True,
    ),
    Case(
        name="power_base",
        node=lambda tf: Pow(tf, Numeric(2.0)),
        to_find=Symbol("x"),
        should_find=True,
    ),
    Case(
        name="power_exponent",
        node=lambda tf: Pow(Numeric(2.0), tf),
        to_find=Symbol("x"),
        should_find=True,
    ),
    Case(
        name="power_in_addition_lhs",
        node=lambda tf: Add(tf, Numeric(1.0)),
        to_find=Pow(Symbol("x"), Numeric(2.0)),
        should_find=True,
    ),
    Case(
        name="power_in_multiplication",
        node=lambda tf: Mul(tf, Symbol("y")),
        to_find=Pow(Symbol("x"), Numeric(3.0)),
        should_find=True,
    ),
    Case(
        name="nested_power",
        node=lambda tf: Pow(Pow(Symbol("x"), Numeric(2.0)), tf),
        to_find=Numeric(3.0),
        should_find=True,
    ),
    Case(
        name="complex_nested_three_levels",
        node=lambda tf: Add(Mul(Pow(tf, Numeric(2.0)), Symbol("y")), Numeric(1.0)),
        to_find=Symbol("x"),
        should_find=True,
    ),
    Case(
        name="similar_but_different_structure",
        node=Add(Mul(Symbol("x"), Numeric(2.0)), Numeric(1.0)),
        to_find=Mul(Symbol("y"), Numeric(2.0)),
        should_find=False,
    ),
    Case(
        name="same_values_different_symbols",
        node=Add(Symbol("x"), Numeric(1.0)),
        to_find=Symbol("y"),
        should_find=False,
    ),
    Case(
        name="empty_search_in_complex",
        node=Mul(Add(Symbol("x"), Numeric(1.0)), Pow(Symbol("y"), Numeric(2.0))),
        to_find=Symbol("z"),
        should_find=False,
    ),
    Case(
        name="deeply_nested_find_in_deeply_nested_input",
        node=lambda tf: Add(
            Mul(
                Pow(Add(Symbol("a"), Numeric(1.0)), Numeric(2.0)),
                Add(tf, Mul(Symbol("b"), Numeric(3.0))),
            ),
            Pow(
                Mul(Symbol("c"), Add(Numeric(4.0), Symbol("d"))),
                Add(Numeric(5.0), Symbol("e")),
            ),
        ),
        to_find=Mul(
            Pow(Symbol("x"), Numeric(2.0)),
            Add(Symbol("y"), Pow(Numeric(2.0), Symbol("z"))),
        ),
        should_find=True,
    ),
    Case(
        name="deeply_nested_almost_match_but_not_found",
        node=Add(
            Mul(
                Pow(Add(Symbol("a"), Numeric(1.0)), Numeric(2.0)),
                Add(
                    Mul(
                        Pow(Symbol("x"), Numeric(2.0)),
                        Add(Symbol("y"), Pow(Numeric(2.0), Symbol("z"))),
                    ),
                    Mul(Symbol("b"), Numeric(3.0)),
                ),
            ),
            Pow(
                Mul(Symbol("c"), Add(Numeric(4.0), Symbol("d"))),
                Add(Numeric(5.0), Symbol("e")),
            ),
        ),
        to_find=Mul(
            Pow(Symbol("x"), Numeric(3.0)),
            Add(Symbol("y"), Pow(Numeric(2.0), Symbol("z"))),
        ),
        should_find=False,
    ),
]


@pytest.mark.parametrize("case", FIND_MATCH_CASES, ids=lambda c: c.name)
def test_find_match(case: Case) -> None:
    to_find = case.to_find
    node = case.node(to_find) if callable(case.node) else case.node
    param = copy.deepcopy(to_find)

    result = BuiltIns._find_match(node, param)

    if case.should_find:
        assert result is to_find
    else:
        assert result is None
