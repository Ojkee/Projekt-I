from typing import NamedTuple
import pytest

from backend.internal.evaluators import Evaluator
from backend.internal.evaluators.error_msgs import EvaluatorErrorUserMsg
from backend.internal.lexing import Lexer
from backend.internal.objects import Object
from backend.internal.parsing import Parser
from backend.internal.parsing.error_msgs import ParserErrorUserMsg
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
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_expr())],
    ),
    Case(
        name="Atom transform with operator as first line",
        input="/+ x",
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_expr())],
    ),
    Case(
        name="Formula as first line",
        input="!func x",
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_expr())],
    ),
    Case(
        name="Only slash",
        input="/",
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_expr())],
    ),
    Case(
        name="Only bang",
        input="!",
        expected=[wrap_obj(EvaluatorErrorUserMsg.no_expr())],
    ),
    Case(
        name="Illegal char at start",
        input="@ + 2",
        expected=[wrap_obj(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Direct division by zero",
        input="5 / 0",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Division by zero in equation",
        input="x = 10 / 0",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Division by zero result",
        input="x = 5 / (2 - 2)",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Nested division by zero",
        input="(5 + 3) / (10 - 5 * 2)",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Zero to negative power",
        input="0 ^ -1",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Zero to negative power complex",
        input="(5 - 5) ^ -2",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Negative base fractional exponent",
        input="(-4) ^ 0.5",
        expected=[wrap_obj(EvaluatorErrorUserMsg.negative_root())],
    ),
    Case(
        name="Complex fractional power",
        input="(-2) ^ (1/3)",
        expected=[wrap_obj(EvaluatorErrorUserMsg.negative_root())],
    ),
    Case(
        name="Invalid operation result",
        input="0 / 0",
        expected=[wrap_obj(EvaluatorErrorUserMsg.zero_division())],
    ),
    Case(
        name="Divide by zero in atom transform",
        input="x = 2\n/0",
        expected=[
            AnyNonErrorObject(),
            wrap_obj(EvaluatorErrorUserMsg.zero_division()),
        ],
    ),
    # Case(
    #     name="Divide equation by zero",
    #     input="x = y + 5\n/0",
    #     expected_error="division by zero",
    # ),
    # Case(
    #     name="Divide by zero expression",
    #     input="x = 10\n/(5 - 5)",
    #     expected_error="division by zero",
    # ),
    # Case(
    #     name="Power to invalid exponent in transform",
    #     input="x = 0\n/^ -1",
    #     expected_error="zero",
    # ),
    # Case(
    #     name="Non-existent formula",
    #     input="x = 5\n!nonexistent x",
    #     expected_error="No formula",
    # ),
    # Case(
    #     name="Empty formula name with params",
    #     input="x = 1\n! x",
    #     expected_error="No formula",  # To może być parser error
    # ),
    # Case(
    #     name="Too many parameters",
    #     input="x = 5\n!solve x, y, z",  # Jeśli solve przyjmuje max 2
    #     expected_error="parameters",
    # ),
    # Case(
    #     name="Formula with division by zero in param",
    #     input="x = 5\n!solve 10/0",
    #     expected_error="division by zero",
    # ),
    # Case(
    #     name="Formula with invalid math in param",
    #     input="x = 2\n!expand 0^-1",
    #     expected_error="zero",
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
