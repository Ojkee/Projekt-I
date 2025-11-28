import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import Node, Mul, Pow, Add, Numeric, Symbol
from backend.internal.expression_tree import FlattenNode, FlattenMul, FlattenAdd, FlattenSymbol, FlattenNumeric, FlattenPow

@dataclass
class Case:
    name: str
    input: FlattenNode
    expected: str


CASES_ADDITION = [
    Case(
        "Simple addition",
        FlattenAdd([FlattenNumeric(3), FlattenNumeric(2)]),
        "3 + 2",
    ),
    Case(
        "Addition with multiple terms",
        FlattenAdd([FlattenSymbol("x"), FlattenSymbol("x"), FlattenSymbol("x")]),
        "x + x + x",
    ),

]

CASES_MULTIPLICATION = [
    Case(
        "Simple multiplication",
        FlattenMul([FlattenNumeric(4), FlattenNumeric(5)]),
        "4 * 5",
    ),
    Case(
        "Multiplication with multiple terms",
        FlattenMul([FlattenSymbol("y"), FlattenSymbol("y"), FlattenSymbol("y")]),
        "y * y * y",
    ),
]

CASES_SUBTRACTION = [
    Case(
        "Simple subtraction",
        FlattenAdd([FlattenSymbol("a"), FlattenMul([FlattenNumeric(-1), FlattenSymbol("b")])]),
        "a - b",
    ),
    Case(
        "Subtraction with multiple terms",
        FlattenAdd([
            FlattenSymbol("a"),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("b")]),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("c")]),
        ]),
        "a - b - c",
    ),
]

CASES_POWER = [
    Case(
        "Simple power",
        FlattenPow(FlattenSymbol("x"), FlattenNumeric(2)),
        "x ^ 2",
    ),
    Case(
        "Power with addition base",
        FlattenPow(FlattenAdd([FlattenSymbol("x"), FlattenNumeric(1)]), FlattenNumeric(3)),
        "(x + 1) ^ 3",
    ),
    Case(
        "Power with multiplication base",
        FlattenPow(FlattenMul([FlattenSymbol("x"), FlattenNumeric(2)]), FlattenNumeric(4)),
        "(x * 2) ^ 4",
    ),
    Case(
        "Power with subtraction base",
        FlattenPow(
            FlattenAdd([
                FlattenSymbol("x"),
                FlattenMul([FlattenNumeric(-1), FlattenSymbol("y")])
            ]),
            FlattenNumeric(5)
        ),
        "(x - y) ^ 5",
    ),
]

CASES_COMPLEX = [
    Case(
        "Complex expression",
        FlattenAdd([
            FlattenPow(FlattenSymbol("x"), FlattenNumeric(2)),
            FlattenMul([
                FlattenSymbol("y"),
                FlattenAdd([
                    FlattenSymbol("z"),
                    FlattenNumeric(3)
                ])
            ]),
            FlattenMul([
                FlattenNumeric(-1),
                FlattenSymbol("w")
            ])
        ]),
        "x ^ 2 + y * (z + 3) - w",
    ),
    Case(
        "Nested operations",
        FlattenMul([
            FlattenAdd([
                FlattenSymbol("a"),
                FlattenNumeric(2)
            ]),
            FlattenPow(
                FlattenAdd([
                    FlattenSymbol("b"),
                    FlattenMul([
                        FlattenNumeric(-1),
                        FlattenSymbol("c")
                    ])
                ]),
                FlattenNumeric(3)
            )
        ]),
        "(a + 2) * (b - c) ^ 3",
    ),
    Case(
        "Mixed operations",
        FlattenAdd([
            FlattenMul([
                FlattenSymbol("m"),
                FlattenPow(FlattenSymbol("n"), FlattenNumeric(2))
            ]),
            FlattenMul([
                FlattenNumeric(-1),
                FlattenAdd([
                    FlattenSymbol("p"),
                    FlattenNumeric(4)
                ])
            ])
        ]),
        "m * n ^ 2 - (p + 4)",
    ),
    Case(
        "Subtraction with negative term",
        FlattenAdd([
            FlattenSymbol("a"),
            FlattenMul([FlattenNumeric(-1), FlattenNumeric(-1)])
        ]),
        "a - (-1)",
    ),
    Case(
        "Subtraction with negative term",
        FlattenAdd([
            FlattenSymbol("a"),
            FlattenMul([FlattenNumeric(-1), FlattenMul([FlattenNumeric(-1), FlattenAdd([FlattenSymbol("b"), FlattenNumeric(2)])])])
        ]),
        "a - (b + 2)",
    ),
    Case(
        "Custom complex expression (x+2+2+2/2)*24/11",
        FlattenMul([
            FlattenAdd([
                FlattenSymbol("x"),
                FlattenNumeric(2),
                FlattenNumeric(2),
                FlattenMul([FlattenNumeric(2), FlattenPow(FlattenNumeric(2), FlattenNumeric(-1))])  # 2/2
            ]),
            FlattenMul([
                FlattenNumeric(24),
                FlattenPow(FlattenNumeric(11), FlattenNumeric(-1))  # /11
            ])
        ]),
        "(x + 2 + 2 + 2 * 2 ^ -1) * 24 * 11 ^ -1",
    ),
]

EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_ADDITION)
EXPRESSION_TREE_UT.extend(CASES_MULTIPLICATION)
EXPRESSION_TREE_UT.extend(CASES_SUBTRACTION)
EXPRESSION_TREE_UT.extend(CASES_POWER)
EXPRESSION_TREE_UT.extend(CASES_COMPLEX)

@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    assert str(case.input) == case.expected