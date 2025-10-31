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
]


@pytest.mark.parametrize("case", BIND_WILDNODES_CASES, ids=lambda c: c.name)
def test_bind_wildnodes(case: Case) -> None:
    result = BuiltIns._bind_wildnodes(case.input, case.to_match)
    assert isinstance(result, NotMatchingFormula)
