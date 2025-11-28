import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import FlattenNode, FlattenMul, FlattenAdd, FlattenSymbol, FlattenNumeric, FlattenPow
from backend.internal.expression_tree.add_node import simplify


@dataclass
class Case:
    name: str
    input: FlattenNode
    expected: FlattenNode

CASES_COMBINE_LIKE_TERMS = [
    Case(
        "Combine like terms with symbols",
        FlattenAdd([FlattenSymbol("x"), FlattenSymbol("x"), FlattenSymbol("x")]),
        FlattenMul([FlattenNumeric(3), FlattenSymbol("x")]),
    ),
    Case(
        "Combine like terms with numeric coefficients",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("y")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("y")]),
            FlattenSymbol("y"),
        ]),
        FlattenMul([FlattenNumeric(6), FlattenSymbol("y")]),
    ),
    Case(
        "Combine like terms with negatives",
        FlattenAdd([
            FlattenMul([FlattenNumeric(5), FlattenSymbol("z")]),
            FlattenMul([FlattenNumeric(-2), FlattenSymbol("z")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("z")]),
        ]),
        FlattenMul([FlattenNumeric(6), FlattenSymbol("z")]),
    ),
    Case(
        "Combine multiple different terms",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("b")]),
            FlattenMul([FlattenNumeric(4), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("b")]),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(6), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(2), FlattenSymbol("b")]),
        ]),
    ),
    Case(
        "Combine like terms with numeric and symbols",
        FlattenAdd([
            FlattenNumeric(1),
            FlattenSymbol("x"),
            FlattenNumeric(2),
            FlattenSymbol("x"),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenNumeric(3),
        ]),
    ),
    Case(
        "Complex nested expression",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenNumeric(3),
            FlattenMul([FlattenNumeric(4), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("x")]),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(5), FlattenSymbol("x")]),
            FlattenNumeric(3),
        ]),
    ),
    Case(
        "Factor common term",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(5), FlattenSymbol("x")]),
    ),
    Case(
        "Factor common term with negatives",
        FlattenAdd([
            FlattenMul([FlattenNumeric(4), FlattenSymbol("y")]),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("y")]),
        ]),
        FlattenMul([FlattenNumeric(3), FlattenSymbol("y")]),
    ),
    Case(
        "Factor common term with multiple terms",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("z")]),
            FlattenMul([FlattenNumeric(5), FlattenSymbol("z")]),
            FlattenMul([FlattenNumeric(-3), FlattenSymbol("z")]),
        ]),
        FlattenMul([FlattenNumeric(4), FlattenSymbol("z")]),
    ),
    Case(
        "Factor common simple numeric + symbol",
        FlattenAdd([
            FlattenMul([FlattenNumeric(5), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(10), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(15), FlattenSymbol("x")]),
    ),

    Case(
        "Factor common symbol with power x^2",
        FlattenAdd([
            FlattenMul([FlattenNumeric(3), FlattenSymbol("x^2")]),
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x^2")]),
        ]),
        FlattenMul([FlattenNumeric(5), FlattenSymbol("x^2")]),
    ),

    Case(
        "Factor common multi-letter symbol",
        FlattenAdd([
            FlattenMul([FlattenNumeric(4), FlattenSymbol("velocity")]),
            FlattenMul([FlattenNumeric(6), FlattenSymbol("velocity")]),
        ]),
        FlattenMul([FlattenNumeric(10), FlattenSymbol("velocity")]),
    ),

    Case(
        "Factor common negative coefficient",
        FlattenAdd([
            FlattenMul([FlattenNumeric(-5), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(-10), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(-15), FlattenSymbol("x")]),
    ),

    Case(
        "Factor common with zero term",
        FlattenAdd([
            FlattenMul([FlattenNumeric(4), FlattenSymbol("x")]),
            FlattenNumeric(0),
            FlattenMul([FlattenNumeric(1), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(5), FlattenSymbol("x")]),
    ),

    Case(
        "Factor common nested add inside mul",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x"), FlattenAdd([FlattenNumeric(1), FlattenNumeric(2)])]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("x"), FlattenAdd([FlattenNumeric(1), FlattenNumeric(2)])]),
        ]),
        FlattenMul([
            FlattenNumeric(15),
            FlattenSymbol("x"),
        ]),
    ),

    Case(
        "Factor common symbol with different order (x vs x*1)",
        FlattenAdd([
            FlattenSymbol("x"),
            FlattenMul([FlattenNumeric(1), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
    ),

    Case(
        "Factor common on 3 different variables where only two match",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(5), FlattenSymbol("b")]),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(5), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(5), FlattenSymbol("b")]),
        ])
    ),

    Case(
        "Factor common symbol y in mixed numeric/symbolic expression",
        FlattenAdd([
            FlattenSymbol("y"),
            FlattenMul([FlattenNumeric(5), FlattenSymbol("y")])
        ]),
        FlattenMul([
            FlattenNumeric(6),
            FlattenSymbol("y")
        ]),
    ),

    Case(
        "No common factor (should stay same)",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("y")]),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("y")]),
        ]),
    ),
]


CASES_SIMPLE = [
    Case(
        "Simple addition",
        FlattenAdd([FlattenNumeric(3), FlattenNumeric(2)]),
        FlattenNumeric(5),
    ),
    Case(
        "Addition with symbols",
        FlattenAdd([FlattenSymbol("x"), FlattenSymbol("x")]),
        FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
    ),
    Case(
        "Addition with numeric and symbol",
        FlattenAdd([FlattenNumeric(1), FlattenSymbol("x"), FlattenNumeric(2)]),
        FlattenAdd([FlattenSymbol("x"), FlattenNumeric(3)]),
    ),
    Case(
        "Nested addition",
        FlattenAdd([
            FlattenNumeric(1),
            FlattenNumeric(2), FlattenSymbol("y")
        ]),
        FlattenAdd([FlattenSymbol("y"), FlattenNumeric(3)]),
    ),
    Case(
        "Combine multiple symbols",
        FlattenAdd([FlattenSymbol("x"), FlattenMul([FlattenNumeric(3), FlattenSymbol("x")])]),
        FlattenMul([FlattenNumeric(4), FlattenSymbol("x")]),
    ),
]

CASES_DISTRIBUTE_MUL = [
    Case(
        "Distribute multiplication over addition",
        FlattenMul([
            FlattenNumeric(2),
            FlattenAdd([
                FlattenNumeric(3),
                FlattenNumeric(4)
            ])
        ]),
        FlattenNumeric(14)
    ),
    Case(
        "Distribute multiplication over addition with symbols",
        FlattenMul([
            FlattenSymbol("x"),
            FlattenAdd([
                FlattenSymbol("y"),
                FlattenSymbol("z")
            ])
        ]),
        FlattenAdd([
            FlattenMul([FlattenSymbol("x"), FlattenSymbol("y")]),
            FlattenMul([FlattenSymbol("x"), FlattenSymbol("z")]),
        ]),
    ),
]

CASES_COMBINE_POWERS = [
    Case(
        "Combine powers with same base",
        FlattenMul([
            FlattenPow(FlattenSymbol("x"), FlattenNumeric(2)),
            FlattenPow(FlattenSymbol("x"), FlattenNumeric(3)),
        ]),
        FlattenPow(FlattenSymbol("x"), FlattenNumeric(5)),
    ),
    Case(
        "Combine powers with different bases (should stay same)",
        FlattenMul([
            FlattenPow(FlattenSymbol("x"), FlattenNumeric(2)),
            FlattenPow(FlattenSymbol("y"), FlattenNumeric(3)),
        ]),
        FlattenMul([
            FlattenPow(FlattenSymbol("x"), FlattenNumeric(2)),
            FlattenPow(FlattenSymbol("y"), FlattenNumeric(3)),
        ]),
    ),
    Case(
        "Combine multiple powers with same base",
        FlattenMul([
            FlattenPow(FlattenSymbol("z"), FlattenNumeric(1)),
            FlattenPow(FlattenSymbol("z"), FlattenNumeric(2)),
            FlattenPow(FlattenSymbol("z"), FlattenNumeric(3)),
        ]),
        FlattenPow(FlattenSymbol("z"), FlattenNumeric(6)),
    ),
]


CASES_ADVANCED = [
    Case(
        "Multiple like terms",
        FlattenAdd([
            FlattenMul([FlattenNumeric(2), FlattenSymbol("x")]),
            FlattenSymbol("x"),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("x")]),
        ]),
        FlattenMul([FlattenNumeric(6), FlattenSymbol("x")]),
    ),
    Case(
        "Addition with negatives",
        FlattenAdd([
            FlattenSymbol("a"),
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("b")]),
            FlattenMul([FlattenNumeric(-2), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(3), FlattenSymbol("b")]),
        ]),
        FlattenAdd([
            FlattenMul([FlattenNumeric(-1), FlattenSymbol("a")]),
            FlattenMul([FlattenNumeric(2), FlattenSymbol("b")]),
        ]),
    ),

]



EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_COMBINE_LIKE_TERMS)
EXPRESSION_TREE_UT.extend(CASES_DISTRIBUTE_MUL)
EXPRESSION_TREE_UT.extend(CASES_COMBINE_POWERS)
EXPRESSION_TREE_UT.extend(CASES_SIMPLE)
EXPRESSION_TREE_UT.extend(CASES_ADVANCED)


@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    result = simplify(case.input)
    assert result == case.expected, f"GOT: {result}, EXPECTED: {case.expected}"
