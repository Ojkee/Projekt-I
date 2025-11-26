import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import Node, Mul, Pow, Add, Numeric, Symbol
from backend.internal.expression_tree import FlattenNode, FlattenMul, FlattenAdd, FlattenSymbol, FlattenNumeric, FlattenPow

@dataclass
class Case:
    name: str
    input: FlattenNode
    expected: FlattenNode


CASES_ADDITION = [
    Case(
        "Simple addition",
        FlattenAdd([FlattenNumeric(3), FlattenNumeric(2)]),
        FlattenNumeric(5),
    ),
    Case(
        "Addition with zero",
        FlattenAdd([FlattenNumeric(5), FlattenNumeric(0)]),
        FlattenNumeric(5),
    ),
    Case(
        "Addition with negatives",
        FlattenAdd([FlattenNumeric(4), FlattenNumeric(-4)]),
        FlattenNumeric(0),
    ),
    Case(
        "Addition with multiple numerics",
        FlattenAdd([FlattenNumeric(1), FlattenNumeric(2), FlattenNumeric(3)]),
        FlattenNumeric(6),
    ),
    Case(
        "Addition with symbols",
        FlattenAdd([FlattenNumeric(12), FlattenSymbol("x"), FlattenNumeric(7)]),
        FlattenAdd([FlattenSymbol("x"), FlattenNumeric(19)]),
    ),
]

CASES_MULTIPLICATION = [
    Case(
        "Simple multiplication",
        FlattenMul([FlattenNumeric(4), FlattenNumeric(5)]),
        FlattenNumeric(20),
    ),
    Case(
        "Multiplication with one",
        FlattenMul([FlattenNumeric(9), FlattenNumeric(1)]),
        FlattenNumeric(9),
    ),
    Case(
        "Multiplication with zero",
        FlattenMul([FlattenNumeric(8), FlattenNumeric(0)]),
        FlattenNumeric(0),
    ),
    Case(
        "Multiplication with negatives",
        FlattenMul([FlattenNumeric(-3), FlattenNumeric(6)]),
        FlattenNumeric(-18),
    ),
    Case(
        "Multiplication with multiple numerics",
        FlattenMul([FlattenNumeric(2), FlattenNumeric(3), FlattenNumeric(4)]),
        FlattenNumeric(24),
    ),
    Case(
        "Multiplication with symbols",
        FlattenMul([FlattenNumeric(7), FlattenSymbol("y"), FlattenNumeric(3)]),
        FlattenMul([FlattenSymbol("y"), FlattenNumeric(21)]),
    ),
]

CASES_ADVANCED = [
    Case(
        "Addition and multiplication",
        FlattenAdd([FlattenMul([FlattenNumeric(2), FlattenNumeric(3)]), FlattenSymbol("x")]),
        FlattenAdd([FlattenSymbol("x"), FlattenNumeric(6)]),
    ),
    Case(
        "Multiplication and addition",
        FlattenMul([FlattenAdd([FlattenNumeric(1), FlattenNumeric(2)]), FlattenSymbol("z")]),
        FlattenMul([FlattenSymbol("z"), FlattenNumeric(3)]),
    ),
    Case(
        "Complex nested expression",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenAdd([FlattenNumeric(3), FlattenNumeric(4)])]),
            FlattenSymbol("w")
        ]),
        FlattenAdd([FlattenSymbol("w"),FlattenNumeric(14)]),
    ),
    Case(
        "Complex nested expression with multiple levels",
        FlattenAdd([
            FlattenMul([
                FlattenAdd([FlattenNumeric(1), FlattenNumeric(2)]),
                FlattenAdd([FlattenNumeric(3), FlattenNumeric(4)])
            ]),
            FlattenNumeric(5)
        ]),
        FlattenNumeric(26),
    ),
    Case(
        "Mixed operations with symbols and numerics",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("b")]),
            FlattenNumeric(4)
        ]),
        FlattenAdd([
            FlattenMul([FlattenSymbol("a"), FlattenNumeric(2.0)]),
            FlattenMul([FlattenSymbol("b"), FlattenNumeric(3.0)]),
            FlattenNumeric(4)
        ]),
    ),
]

CASES_POWER = [
    Case(
        "Simple power",
        FlattenPow(FlattenNumeric(2), FlattenNumeric(3)),
        FlattenNumeric(8),
    ),
    Case(
        "Power with one",
        FlattenPow(FlattenNumeric(5), FlattenNumeric(1)),
        FlattenNumeric(5),
    ),
    Case(
        "Power with zero",
        FlattenPow(FlattenNumeric(7), FlattenNumeric(0)),
        FlattenNumeric(1),
    ),
    Case(
        "Power with negative exponent",
        FlattenPow(FlattenNumeric(2), FlattenNumeric(-2)),
        FlattenNumeric(0.25),
    ),
    Case(
        "Power with multiplication base",
        FlattenPow(FlattenMul([FlattenNumeric(2), FlattenNumeric(3)]), FlattenNumeric(2)),
        FlattenNumeric(36),
    ),
    Case(
        "Power with addition base",
        FlattenPow(FlattenAdd([FlattenNumeric(1), FlattenNumeric(1)]), FlattenNumeric(3)),
        FlattenNumeric(8),
    ),
]

EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_ADDITION)
EXPRESSION_TREE_UT.extend(CASES_MULTIPLICATION)
EXPRESSION_TREE_UT.extend(CASES_ADVANCED)
EXPRESSION_TREE_UT.extend(CASES_POWER)

@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    folded = case.input.constant_fold()
    print(f"Test case '{case.name}': GOT: {folded} EXPECTED: {case.expected}")
    assert folded == case.expected