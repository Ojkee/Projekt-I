import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import Node, Add, Numeric
from backend.internal.builtins import BuiltIns


@dataclass
class Case:
    name: str
    input: Node
    param: Node
    expected: Node


CASES_FIND_MATCH = [
    Case(
        "Find Numeric Leaf",
        Add(Numeric(3.0), Numeric(4.0)),
        Numeric(3.0),
        Numeric(3.0),
    ),
]

FIND_MATCH_UT: list[Case] = []
FIND_MATCH_UT.extend(CASES_FIND_MATCH)


# TODO: implement mechanism that checks if expected output is reference to original node subtree.
@pytest.mark.parametrize("case", FIND_MATCH_UT, ids=lambda c: c.name)
def test_find_match_wildnodes(case: Case) -> None:
    pass
