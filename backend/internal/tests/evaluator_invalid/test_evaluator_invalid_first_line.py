from typing import NamedTuple
import pytest

from backend.internal.evaluators import Evaluator
from backend.internal.evaluators.error_msgs import EvaluatorErrorUserMsg
from backend.internal.lexing import Lexer
from backend.internal.objects import Object
from backend.internal.parsing import Parser
from backend.internal.tests.evaluator_invalid.util_evalate_invalid import (
    AnyNonErrorObject,
    wrap_obj,
)
from backend.internal.tokenstreams import TokenStream


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Object]


CASES_EVALUATOR_INVALID_FIRST_LINE: list[Case] = [
    Case(
        name="Empty",
        input="",
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_input())],
    ),
    Case(
        name="Atom transform as first line",
        input="/2",
        expected=[wrap_obj("No input")],
    ),
    # Case(
    #     name="Atom transform with operator as first line",
    #     input="/+ x",
    #     expected="First line must be equation or expression",
    # ),
    # Case(
    #     name="Formula as first line",
    #     input="!func x",
    #     expected="First line must be equation or expression",
    # ),
    # Case(
    #     name="Only slash",
    #     input="/",
    #     expected="First line must be equation or expression",
    # ),
    # Case(
    #     name="Only bang",
    #     input="!",
    #     expected="First line must be equation or expression",
    # ),
    # Case(
    #     name="Illegal char at start",
    #     input="@ + 2",
    #     expected_error="Illegal character",
    # ),
]


@pytest.mark.parametrize(
    "case", CASES_EVALUATOR_INVALID_FIRST_LINE, ids=lambda c: c.name
)
def test_cases_evaluator_invalid(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    assert case.expected == subjects
