from dataclasses import dataclass
import pytest

from backend.internal.expression_tree import Node, Numeric, Add, Mul, Symbol, Pow
from backend.internal.math_builtins import BuiltIns
from backend.internal.math_builtins.formula_node import WildNode


@dataclass
class Case:
    name: str
    input: Node
    to_match: Node
    expected: dict[str, Node]


BIND_WILDNODES_CASES: list[Case] = [
    Case(
        name="Single shallow node",
        input=Numeric(4.0),
        to_match=WildNode("a"),
        expected={"a": Numeric(4.0)},
    ),
    Case(
        name="Multiple shallow nodes",
        input=Add(Numeric(5.0), Numeric(6.0)),
        to_match=Add(WildNode("a"), WildNode("b")),
        expected={"a": Numeric(5.0), "b": Numeric(6.0)},
    ),
    Case(
        name="Deep Expression of multiple shallow nodes",
        input=Add(
            Add(Numeric(1.0), Pow(Symbol("h"), Numeric(3.0))),
            Mul(Add(Symbol("x"), Symbol("y")), Numeric(4.0)),
        ),
        to_match=Add(
            Add(WildNode("a"), Pow(WildNode("b"), Numeric(3.0))),
            Mul(Add(WildNode("c"), Symbol("y")), WildNode("d")),
        ),
        expected={
            "a": Numeric(1.0),
            "b": Symbol("h"),
            "c": Symbol("x"),
            "d": Numeric(4.0),
        },
    ),
    Case(
        name="Single 2 level node",
        input=Add(Numeric(1.0), Numeric(2.0)),
        to_match=WildNode("a"),
        expected={"a": Add(Numeric(1.0), Numeric(2.0))},
    ),
    Case(
        name="Single 3 level node",
        input=Add(Add(Numeric(1.0), Numeric(2.0)), Numeric(2.0)),
        to_match=WildNode("a"),
        expected={"a": Add(Add(Numeric(1.0), Numeric(2.0)), Numeric(2.0))},
    ),
    Case(
        name="Reused wildnode - same binding",
        input=Add(Numeric(5.0), Numeric(5.0)),
        to_match=Add(WildNode("a"), WildNode("a")),
        expected={"a": Numeric(5.0)},
    ),
    Case(
        name="Reused wildnode in nested structure",
        input=Mul(Add(Symbol("x"), Numeric(1.0)), Add(Symbol("x"), Numeric(1.0))),
        to_match=Mul(WildNode("expr"), WildNode("expr")),
        expected={"expr": Add(Symbol("x"), Numeric(1.0))},
    ),
    Case(
        name="Mixed concrete and wild nodes",
        input=Add(Mul(Numeric(2.0), Symbol("x")), Numeric(3.0)),
        to_match=Add(Mul(Numeric(2.0), WildNode("var")), Numeric(3.0)),
        expected={"var": Symbol("x")},
    ),
    Case(
        name="Wild node matching entire power expression",
        input=Add(Pow(Symbol("x"), Numeric(2.0)), Numeric(1.0)),
        to_match=Add(WildNode("power_expr"), Numeric(1.0)),
        expected={"power_expr": Pow(Symbol("x"), Numeric(2.0))},
    ),
    Case(
        name="Multiple levels of wild nodes",
        input=Mul(Add(Numeric(1.0), Numeric(2.0)), Pow(Symbol("x"), Numeric(3.0))),
        to_match=Mul(WildNode("sum"), WildNode("power")),
        expected={
            "sum": Add(Numeric(1.0), Numeric(2.0)),
            "power": Pow(Symbol("x"), Numeric(3.0)),
        },
    ),
    Case(
        name="Wild node in power base",
        input=Pow(Mul(Symbol("x"), Numeric(2.0)), Numeric(3.0)),
        to_match=Pow(WildNode("base"), Numeric(3.0)),
        expected={"base": Mul(Symbol("x"), Numeric(2.0))},
    ),
    Case(
        name="Wild node in power exponent",
        input=Pow(Symbol("x"), Add(Numeric(1.0), Numeric(2.0))),
        to_match=Pow(Symbol("x"), WildNode("exp")),
        expected={"exp": Add(Numeric(1.0), Numeric(2.0))},
    ),
    Case(
        name="Complex nested with multiple reused wilds",
        input=Add(Mul(Symbol("x"), Symbol("x")), Mul(Symbol("x"), Symbol("x"))),
        to_match=Add(
            Mul(WildNode("a"), WildNode("a")), Mul(WildNode("a"), WildNode("a"))
        ),
        expected={"a": Symbol("x")},
    ),
    Case(
        name="Deep nesting with single wild at bottom",
        input=Add(Mul(Pow(Symbol("y"), Numeric(2.0)), Numeric(3.0)), Numeric(1.0)),
        to_match=Add(
            Mul(Pow(WildNode("var"), Numeric(2.0)), Numeric(3.0)), Numeric(1.0)
        ),
        expected={"var": Symbol("y")},
    ),
    Case(
        name="All wild nodes",
        input=Mul(Numeric(7.0), Symbol("z")),
        to_match=Mul(WildNode("left"), WildNode("right")),
        expected={"left": Numeric(7.0), "right": Symbol("z")},
    ),
    Case(
        name="Wild matching complex expression in both sides",
        input=Add(
            Mul(Pow(Symbol("a"), Numeric(2.0)), Numeric(3.0)),
            Mul(Pow(Symbol("a"), Numeric(2.0)), Numeric(3.0)),
        ),
        to_match=Add(WildNode("term"), WildNode("term")),
        expected={"term": Mul(Pow(Symbol("a"), Numeric(2.0)), Numeric(3.0))},
    ),
]


@pytest.mark.parametrize("case", BIND_WILDNODES_CASES, ids=lambda c: c.name)
def test_bind_wildnodes(case: Case) -> None:
    result = BuiltIns._bind_wildnodes(case.input, case.to_match)
    assert result == case.expected
