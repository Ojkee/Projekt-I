from dataclasses import dataclass
import pytest

from backend.internal.expression_tree import Node, Numeric, Add, Mul, Symbol, Pow
from backend.internal.math_builtins import BuiltIns
from backend.internal.math_builtins.builtins_error import NotMatchingFormula
from backend.internal.math_builtins.formula_node import WildNode


@dataclass
class Case:
    name: str
    input: Node
    to_match: Node


BIND_WILDNODES_CASES: list[Case] = [
    Case(
        name="Single shallow error",
        input=Add(Numeric(4.0), Numeric(5.0)),
        to_match=Add(WildNode("a"), WildNode("a")),
    ),
    Case(
        name="Single 2 level error",
        input=Add(Add(Numeric(1.0), Numeric(1.0)), Add(Numeric(1.0), Numeric(2.0))),
        to_match=Add(WildNode("a"), WildNode("a")),
    ),
    Case(
        name="Binomial Expansion Formula error",
        input=Pow(Add(Symbol("a"), Symbol("b")), Numeric(3.0)),
        to_match=Pow(Add(WildNode("x"), WildNode("y")), Numeric(2.0)),
    ),
    Case(
        name="Type mismatch - Add vs Mul",
        input=Add(Numeric(1.0), Numeric(2.0)),
        to_match=Mul(WildNode("a"), WildNode("b")),
    ),
    Case(
        name="Type mismatch - Mul vs Pow",
        input=Mul(Numeric(2.0), Numeric(3.0)),
        to_match=Pow(WildNode("base"), WildNode("exp")),
    ),
    Case(
        name="Type mismatch in nested - Add vs Mul",
        input=Add(Add(Numeric(1.0), Numeric(2.0)), Numeric(3.0)),
        to_match=Add(Mul(WildNode("a"), WildNode("b")), Numeric(3.0)),
    ),
    Case(
        name="Different numeric values",
        input=Add(Numeric(5.0), Numeric(1.0)),
        to_match=Add(Numeric(6.0), Numeric(1.0)),
    ),
    Case(
        name="Concrete numeric mismatch in nested",
        input=Mul(Numeric(2.0), Add(Numeric(3.0), Symbol("x"))),
        to_match=Mul(Numeric(2.0), Add(Numeric(4.0), WildNode("x"))),
    ),
]


@pytest.mark.parametrize("case", BIND_WILDNODES_CASES, ids=lambda c: c.name)
def test_bind_wildnodes(case: Case) -> None:
    result = BuiltIns._bind_wildnodes(case.input, case.to_match)
    assert isinstance(result, NotMatchingFormula)
