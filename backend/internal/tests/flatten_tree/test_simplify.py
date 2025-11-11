import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import Node, Mul, Pow, Add, Numeric, Symbol
from backend.internal.expression_tree import FlattenNode, FlattenMul, FlattenAdd, FlattenSymbol, FlattenNumeric, FlattenPow

@dataclass
class Case:
    name: str
    input: FlattenNode
    expected: FlattenNode


CASES_CONVERT_ADDITION = [
    Case(
        "Simple addition",
        FlattenAdd([FlattenNumeric(3), FlattenNumeric(2)]),
        FlattenNumeric(5),
    ),
    Case(
        "Addition with zero",
        FlattenAdd([FlattenSymbol("x"), FlattenSymbol("x")]),
        FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
    ),
]

EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_CONVERT_ADDITION)

@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    pass #assert case.input.simplify() == case.expected