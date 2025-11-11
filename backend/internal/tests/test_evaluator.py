import pytest
from dataclasses import dataclass

from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.tokenstreams import TokenStream
from backend.internal.evaluators import Evaluator


@dataclass
class Case:
    name: str
    input: str
    expected: list[str]


CASES_EVAL_SUBJECT = [
    Case(
        "Simple addition",
        "a + b",
        ["EXPR((a+b))"],
    ),
    Case(
        "Addition and subtraction",
        "a + b - c",
        ["EXPR(((a+b)+(c*-1)))"],
    ),
    Case(
        "Addition, subtraction and multiplication",
        "a + b - c * d",
        ["EXPR(((a+b)+((c*d)*-1)))"],
    ),
    Case(
        "Multiplication and addition",
        "a * b + c",
        ["EXPR(((a*b)+c))"],
    ),
]

CASES_EVAL_ATOM_TRANSFORM = [
    Case(
        "Plus",
        "/+2",
        ["ERROR: First line must be equation or expression"],
    ),
    Case(
        "Minus",
        "/-2",
        ["ERROR: First line must be equation or expression"],
    ),
    Case(
        "Divide",
        "/2",
        ["ERROR: First line must be equation or expression"],
    ),
    Case(
        "Multiply",
        "/*2",
        ["ERROR: First line must be equation or expression"],
    ),
]

CASES_EVAL_SUBJECT_ATOM = [
    Case(
        "Addition",
        "a + b\n/+2",
        ["EXPR((a+b))", "EXPR(((a+b)+2.0))"],
    ),
    Case(
        "Subtraction",
        "a + b\n/-2",
        ["EXPR((a+b))", "EXPR(((a+b)+(-1*2.0)))"],
    ),
    Case(
        "Multiplication",
        "a + b\n/*2",
        ["EXPR((a+b))", "EXPR(((a+b)*2.0))"],
    ),
    Case(
        "Division",
        "a + b\n/2",
        ["EXPR((a+b))", "EXPR(((a+b)*(2.0^-1)))"],
    ),
    Case(
        "Addition equation",
        "2x = 2\n/+2\n",
        [
            "EQUATION((2.0*x) = 2.0)",
            "EQUATION(((2.0*x)+2.0) = (2.0+2.0))",
        ],
    ),
]


EVALUATOR_UT: list[Case] = []
EVALUATOR_UT.extend(CASES_EVAL_SUBJECT)
EVALUATOR_UT.extend(CASES_EVAL_ATOM_TRANSFORM)
EVALUATOR_UT.extend(CASES_EVAL_SUBJECT_ATOM)


@pytest.mark.parametrize("case", EVALUATOR_UT, ids=lambda c: c.name)
def test_evaluator(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    assert [repr(subject) for subject in subjects] == case.expected
