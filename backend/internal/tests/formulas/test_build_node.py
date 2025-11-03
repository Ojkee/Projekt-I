import pytest
from typing import NamedTuple

from backend.internal.expression_tree import Node, Add, Numeric, Mul, Pow, Symbol
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.math_builtins.lookups import BuiltIns


class Case(NamedTuple):
    name: str
    input: Node
    cache: dict[str, Node]
    expected: Node


CASES_BUILD_NODE: list[Case] = [
    Case(
        name="Single node",
        input=WildNode("x"),
        cache={"x": Numeric(5.0)},
        expected=Numeric(5.0),
    ),
    Case(
        name="Single Add node",
        input=Add(Numeric(1.0), WildNode("x")),
        cache={"x": Numeric(2.0)},
        expected=Add(Numeric(1.0), Numeric(2.0)),
    ),
    Case(
        name="Dual Add node",
        input=Add(WildNode("x"), WildNode("x")),
        cache={"x": Numeric(2.0)},
        expected=Add(Numeric(2.0), Numeric(2.0)),
    ),
    Case(
        name="Nested multi nodes",
        input=Pow(
            Add(WildNode("x"), WildNode("z")),
            Mul(WildNode("x"), WildNode("y")),
        ),
        cache={"x": Numeric(2.0), "y": Symbol("a"), "z": Numeric(3.0)},
        expected=Pow(
            Add(Numeric(2.0), Numeric(3.0)),
            Mul(Numeric(2.0), Symbol("a")),
        ),
    ),
    Case(
        name="No wildcards - passthrough",
        input=Add(Numeric(1.0), Numeric(2.0)),
        cache={},
        expected=Add(Numeric(1.0), Numeric(2.0)),
    ),
    Case(
        name="Nested wildcard replacement",
        input=Mul(WildNode("expr"), Numeric(2.0)),
        cache={"expr": Add(Symbol("x"), Numeric(1.0))},
        expected=Mul(Add(Symbol("x"), Numeric(1.0)), Numeric(2.0)),
    ),
    Case(
        name="Deep nesting with multiple wildcards",
        input=Add(Mul(WildNode("a"), Pow(WildNode("b"), Numeric(2.0))), WildNode("c")),
        cache={"a": Numeric(3.0), "b": Symbol("x"), "c": Numeric(1.0)},
        expected=Add(Mul(Numeric(3.0), Pow(Symbol("x"), Numeric(2.0))), Numeric(1.0)),
    ),
    Case(
        name="Wildcard to complex expression",
        input=Mul(WildNode("term"), WildNode("term")),
        cache={"term": Pow(Symbol("x"), Numeric(2.0))},
        expected=Mul(Pow(Symbol("x"), Numeric(2.0)), Pow(Symbol("x"), Numeric(2.0))),
    ),
    Case(
        name="All wildcards replaced",
        input=Pow(WildNode("base"), WildNode("exp")),
        cache={"base": Symbol("x"), "exp": Numeric(3.0)},
        expected=Pow(Symbol("x"), Numeric(3.0)),
    ),
    Case(
        name="Mix of concrete and wildcard nodes",
        input=Add(Mul(Numeric(2.0), WildNode("x")), Mul(Numeric(3.0), WildNode("y"))),
        cache={"x": Symbol("a"), "y": Symbol("b")},
        expected=Add(Mul(Numeric(2.0), Symbol("a")), Mul(Numeric(3.0), Symbol("b"))),
    ),
    Case(
        name="Wildcard replaced with nested expression",
        input=Add(WildNode("lhs"), Numeric(5.0)),
        cache={"lhs": Mul(Add(Numeric(1.0), Numeric(2.0)), Numeric(3.0))},
        expected=Add(Mul(Add(Numeric(1.0), Numeric(2.0)), Numeric(3.0)), Numeric(5.0)),
    ),
    Case(
        name="Same wildcard used three times",
        input=Add(WildNode("n"), Add(WildNode("n"), WildNode("n"))),
        cache={"n": Numeric(7.0)},
        expected=Add(Numeric(7.0), Add(Numeric(7.0), Numeric(7.0))),
    ),
    Case(
        name="Power with both wildcards",
        input=Pow(Mul(WildNode("coef"), WildNode("var")), WildNode("exp")),
        cache={"coef": Numeric(2.0), "var": Symbol("x"), "exp": Numeric(3.0)},
        expected=Pow(Mul(Numeric(2.0), Symbol("x")), Numeric(3.0)),
    ),
    Case(
        name="Complex nested with reused wildcards",
        input=Mul(Add(WildNode("a"), WildNode("b")), Add(WildNode("b"), WildNode("a"))),
        cache={"a": Numeric(1.0), "b": Numeric(2.0)},
        expected=Mul(Add(Numeric(1.0), Numeric(2.0)), Add(Numeric(2.0), Numeric(1.0))),
    ),
    Case(
        name="Single Symbol replacement",
        input=WildNode("var"),
        cache={"var": Symbol("x")},
        expected=Symbol("x"),
    ),
    Case(
        name="Wildcard to entire subtree",
        input=WildNode("whole"),
        cache={"whole": Add(Mul(Numeric(2.0), Symbol("x")), Numeric(1.0))},
        expected=Add(Mul(Numeric(2.0), Symbol("x")), Numeric(1.0)),
    ),
    Case(
        name="Multiple very nested trees with deeply nested cache structures",
        input=Add(
            Mul(
                Pow(Add(WildNode("a"), WildNode("b")), WildNode("c")),
                Add(WildNode("d"), Pow(WildNode("a"), WildNode("e"))),
            ),
            Pow(
                Mul(
                    Add(WildNode("b"), WildNode("c")), Pow(WildNode("d"), WildNode("e"))
                ),
                Add(Mul(WildNode("a"), WildNode("e")), WildNode("f")),
            ),
        ),
        cache={
            "a": Mul(Pow(Symbol("x"), Numeric(2.0)), Add(Symbol("y"), Numeric(1.0))),
            "b": Add(Mul(Numeric(3.0), Symbol("z")), Pow(Symbol("w"), Numeric(2.0))),
            "c": Pow(Add(Symbol("a"), Mul(Numeric(2.0), Symbol("b"))), Numeric(3.0)),
            "d": Mul(
                Add(Pow(Symbol("p"), Numeric(2.0)), Numeric(1.0)),
                Add(Symbol("q"), Numeric(5.0)),
            ),
            "e": Add(Mul(Symbol("r"), Pow(Symbol("s"), Numeric(2.0))), Numeric(7.0)),
            "f": Pow(
                Mul(Add(Symbol("t"), Numeric(2.0)), Symbol("u")),
                Add(Numeric(1.0), Symbol("v")),
            ),
        },
        expected=Add(
            Mul(
                Pow(
                    Add(
                        Mul(
                            Pow(Symbol("x"), Numeric(2.0)),
                            Add(Symbol("y"), Numeric(1.0)),
                        ),
                        Add(
                            Mul(Numeric(3.0), Symbol("z")),
                            Pow(Symbol("w"), Numeric(2.0)),
                        ),
                    ),
                    Pow(Add(Symbol("a"), Mul(Numeric(2.0), Symbol("b"))), Numeric(3.0)),
                ),
                Add(
                    Mul(
                        Add(Pow(Symbol("p"), Numeric(2.0)), Numeric(1.0)),
                        Add(Symbol("q"), Numeric(5.0)),
                    ),
                    Pow(
                        Mul(
                            Pow(Symbol("x"), Numeric(2.0)),
                            Add(Symbol("y"), Numeric(1.0)),
                        ),
                        Add(
                            Mul(Symbol("r"), Pow(Symbol("s"), Numeric(2.0))),
                            Numeric(7.0),
                        ),
                    ),
                ),
            ),
            Pow(
                Mul(
                    Add(
                        Add(
                            Mul(Numeric(3.0), Symbol("z")),
                            Pow(Symbol("w"), Numeric(2.0)),
                        ),
                        Pow(
                            Add(Symbol("a"), Mul(Numeric(2.0), Symbol("b"))),
                            Numeric(3.0),
                        ),
                    ),
                    Pow(
                        Mul(
                            Add(Pow(Symbol("p"), Numeric(2.0)), Numeric(1.0)),
                            Add(Symbol("q"), Numeric(5.0)),
                        ),
                        Add(
                            Mul(Symbol("r"), Pow(Symbol("s"), Numeric(2.0))),
                            Numeric(7.0),
                        ),
                    ),
                ),
                Add(
                    Mul(
                        Mul(
                            Pow(Symbol("x"), Numeric(2.0)),
                            Add(Symbol("y"), Numeric(1.0)),
                        ),
                        Add(
                            Mul(Symbol("r"), Pow(Symbol("s"), Numeric(2.0))),
                            Numeric(7.0),
                        ),
                    ),
                    Pow(
                        Mul(Add(Symbol("t"), Numeric(2.0)), Symbol("u")),
                        Add(Numeric(1.0), Symbol("v")),
                    ),
                ),
            ),
        ),
    ),
]


@pytest.mark.parametrize("case", CASES_BUILD_NODE, ids=lambda c: c.name)
def test_build_node(case: Case) -> None:
    result = BuiltIns._build_node(case.input, case.cache)
    assert result == case.expected
