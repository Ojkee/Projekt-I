import pytest
from dataclasses import dataclass

from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.tokenstreams.tokenstream import TokenStream
from backend.internal.evaluators import Evaluator


@dataclass
class Case:
    name: str
    input: str
    expected: str


CASES_EVAL_SUBJECT = [
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
]

CASES_EVAL_ATOM_TRANSFORM = [
    Case(
        "Plus",
        "/+2",
        "None",
    ),
    Case(
        "Minus",
        "/-2",
        "None",
    ),
    Case(
        "Divide",
        "/2",
        "None",
    ),
    Case(
        "Multiply",
        "/*2",
        "None",
    ),
]

CASES_EVAL_SUBJECT_ATOM = [
    Case(
        "Addition",
        "a + b\n/+2",
        "((a+b)+2.0)",
    ),
    Case(
        "Subtraction",
        "a + b\n/-2",
        "((a+b)+(2.0*-1))",
    ),
    Case(
        "Multiplication",
        "a + b\n/*2",
        "((a+b)*2.0)",
    ),
    Case(
        "Division",
        "a + b\n/2",
        "((a+b)*(2.0^-1))",
    ),
]

EVALUATOR_UT: list[Case] = []
EVALUATOR_UT.extend(CASES_EVAL_SUBJECT)
EVALUATOR_UT.extend(CASES_EVAL_ATOM_TRANSFORM)
EVALUATOR_UT.extend(CASES_EVAL_SUBJECT_ATOM)


@pytest.mark.parametrize("case", EVALUATOR_UT, ids=lambda c: c.name)
def test_expression_tree(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjectObject = evaluator.eval(program)

    assert repr(subjectObject) == case.expected
