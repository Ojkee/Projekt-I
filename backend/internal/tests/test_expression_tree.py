import pytest
from dataclasses import dataclass

from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.expression_tree import convert_to_expression_tree
from backend.internal.statements import Subject
from backend.internal.tokenstreams.tokenstream import TokenStream


@dataclass
class Case:
    name: str
    input: str
    expected: str


CASES_CONVERT_AST_EXPRESSION = [
    Case(
        "Simple addition",
        "a + b",
        "(a+b)",
    ),
    Case(
        "Addition and subtraction",
        "a + b - c",
        "((a+b)+(c*-1))",
    ),
    Case(
        "Addition, subtraction and multiplication",
        "a + b - c * d",
        "((a+b)+((c*d)*-1))",
    ),
    Case(
        "Multiplication and addition",
        "a * b + c",
        "((a*b)+c)",
    ),
    Case(
        "Multiplication, addition and subtraction",
        "a * b + c - d",
        "(((a*b)+c)+(d*-1))",
    ),
    Case(
        "Multiple operations",
        "a + b * c - d / e",
        "((a+(b*c))+((d*(e^-1))*-1))",
    ),
    Case(
        "Parentheses",
        "(a + b) * (c - d)",
        "((a+b)*(c+(d*-1)))",
    ),
    Case(
        "Exponentiation",
        "a ^ 2 + b",
        "((a^2.0)+b)",
    ),
    Case(
        "Complex expression",
        "a ^ 2 + b * (c - d) / e - f",
        "(((a^2.0)+((b*(c+(d*-1)))*(e^-1)))+(f*-1))",
    ),
    Case(
        "Unary minus",
        "-a + b",
        "((a*-1)+b)",
    ),
    Case(
        "Unary minus with parentheses",
        "-(a + b) * c",
        "(((a+b)*-1)*c)",
    ),
    Case(
        "Multiple unary minuses",
        "-a - b",
        "((a*-1)+(b*-1))",
    ),
]

CASES_SIMPLIFY_EXPRESSION_TREE = [
    Case(
        "Addition with zero",
        "a + 0",
        "a",
    ),
    Case(
        "Addition with zero (reversed)",
        "0 + a",
        "a",
    ),
    Case(
        "Subtraction with zero",
        "a - 0",
        "a",
    ),
    Case(
        "Multiplication with zero (left)",
        "0 * a",
        "0",
    ),
    Case(
        "Multiplication with zero (right)",
        "a * 0",
        "0",
    ),
    Case(
        "Multiplication with one (left)",
        "1 * a",
        "a",
    ),
    Case(
        "Multiplication with one (right)",
        "a * 1",
        "a",
    ),
    Case(
        "Complex expression simplification",
        "a * 1 + 0 - (b * 0 + c)",
        "(a+(c*-1))",
    ),
    Case(
        "Exponentiation with zero",
        "a ^ 0",
        "1",
    ),
    Case(
        "Exponentiation with one",
        "a ^ 1",
        "a",
    ),
    Case(
        "Complex exponentiation simplification",
        "a ^ 1 + b * 0 - (c ^ 0 + d * 1)",
        "(a+((1+d)*-1))",
    ),
    Case(
        "Nested simplifications",
        "(a + 0) * (b - 0) + (c * 1 - c * 0)",
        "((a*b)+c)",
    ),
    Case(
        "Multiple simplifications",
        "((a + 0) * 1 + 0) - ((b * 0 + c) * 1 - (d ^ 0))",
        "(a+((c+-1)*-1))",
    ),
    Case(
        "All simplifications",
        "((a + 0) * 1 + 0) - ((b * 0 + c) * 1 - (d ^ 1)) + (e * 0) + (f ^ 0) - (g * 1)",
        "(((a+((c+(d*-1))*-1))+1)+(g*-1))",
    ),
    Case(
        "Simplification resulting in zero",
        "a * 0 + b * 0 - (c * 0 + d * 0)",
        "0",
    ),
]

EXPRESSION_TREE_UT: list[Case] = []
EXPRESSION_TREE_UT.extend(CASES_CONVERT_AST_EXPRESSION)
EXPRESSION_TREE_UT.extend(CASES_SIMPLIFY_EXPRESSION_TREE)


@pytest.mark.parametrize("case", EXPRESSION_TREE_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()

    [stmnt] = program.get()
    assert isinstance(stmnt, Subject)
    node = convert_to_expression_tree(stmnt.expr)
    assert node
    tree = node.reduce()
    assert repr(tree) == case.expected
