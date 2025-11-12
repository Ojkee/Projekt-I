import pytest
from dataclasses import dataclass

from backend.internal.expression_tree import Node, Mul, Pow, Add, Numeric, Symbol
from backend.internal.expression_tree import (
    FlattenNode,
    FlattenMul,
    FlattenAdd,
    FlattenSymbol,
    FlattenNumeric,
    FlattenPow,
)


@dataclass
class Case:
    name: str
    input: Node
    expected: FlattenNode


CASES_CONVERT_ADDITION = [
    Case(
        "Simple addition",
        Add(Symbol("a"), Symbol("b")),
        FlattenAdd([FlattenSymbol("a"), FlattenSymbol("b")]),
    ),
    Case(
        "Nested addition",
        Add(Add(Symbol("a"), Symbol("b")), Symbol("c")),
        FlattenAdd([FlattenSymbol("a"), FlattenSymbol("b"), FlattenSymbol("c")]),
    ),
    Case(
        "Multiple nested additions",
        Add(Add(Symbol("a"), Add(Symbol("b"), Symbol("c"))), Symbol("d")),
        FlattenAdd(
            [
                FlattenSymbol("a"),
                FlattenSymbol("b"),
                FlattenSymbol("c"),
                FlattenSymbol("d"),
            ]
        ),
    ),
]

CASES_CONVERT_MULTIPLICATION = [
    Case(
        "Simple multiplication",
        Mul(Symbol("x"), Symbol("y")),
        FlattenMul([FlattenSymbol("x"), FlattenSymbol("y")]),
    ),
    Case(
        "Nested multiplication",
        Mul(Mul(Symbol("x"), Symbol("y")), Symbol("z")),
        FlattenMul([FlattenSymbol("x"), FlattenSymbol("y"), FlattenSymbol("z")]),
    ),
    Case(
        "Multiple nested multiplications",
        Mul(Mul(Symbol("x"), Mul(Symbol("y"), Symbol("z"))), Symbol("w")),
        FlattenMul(
            [
                FlattenSymbol("x"),
                FlattenSymbol("y"),
                FlattenSymbol("z"),
                FlattenSymbol("w"),
            ]
        ),
    ),
]

CASES_CONVERT_ADVANCED = [
    Case(
        "Addition and multiplication",
        Add(Mul(Symbol("a"), Symbol("b")), Symbol("c")),
        FlattenAdd(
            [FlattenMul([FlattenSymbol("a"), FlattenSymbol("b")]), FlattenSymbol("c")]
        ),
    ),
    Case(
        "Multiplication and addition",
        Mul(Add(Symbol("x"), Symbol("y")), Symbol("z")),
        FlattenMul(
            [FlattenAdd([FlattenSymbol("x"), FlattenSymbol("y")]), FlattenSymbol("z")]
        ),
    ),
    Case(
        "Complex nested expression",
        Add(Mul(Symbol("a"), Add(Symbol("b"), Symbol("c"))), Symbol("d")),
        FlattenAdd(
            [
                FlattenMul(
                    [
                        FlattenSymbol("a"),
                        FlattenAdd([FlattenSymbol("b"), FlattenSymbol("c")]),
                    ]
                ),
                FlattenSymbol("d"),
            ]
        ),
    ),
    Case(
        "Complex nested expression with multiple levels",
        Add(
            Symbol("x"),
            Add(
                Mul(Symbol("y"), Symbol("z")),
                Add(Symbol("w"), Mul(Symbol("u"), Symbol("v"))),
            ),
        ),
        FlattenAdd(
            [
                FlattenSymbol("x"),
                FlattenMul([FlattenSymbol("y"), FlattenSymbol("z")]),
                FlattenSymbol("w"),
                FlattenMul([FlattenSymbol("u"), FlattenSymbol("v")]),
            ]
        ),
    ),
]


EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_CONVERT_ADDITION)
EXPRESSION_TREE_UT.extend(CASES_CONVERT_MULTIPLICATION)
EXPRESSION_TREE_UT.extend(CASES_CONVERT_ADVANCED)


@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    node_flat = case.input.flatten()
    print(str(node_flat), "==", str(case.expected))
    assert node_flat == case.expected

