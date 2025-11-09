from typing import NamedTuple
import pytest

from backend.internal.evaluators import Evaluator
from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.tokenstreams import TokenStream


class Case(NamedTuple):
    name: str
    input: str
    expected: list[str]


CASES_FIRST_LINE: list[Case] = [
    Case(
        name="Empty",
        input="",
        expected=["No input"],
    ),
    Case(
        name="Empty New Line",
        input="\n",
        expected=["First line must be equation or expression"],
    ),
]

CASES_EVALUATOR_INVALID: list[Case] = []
CASES_EVALUATOR_INVALID.extend(CASES_FIRST_LINE)


@pytest.mark.parametrize("case", CASES_EVALUATOR_INVALID, ids=lambda c: c.name)
def test_cases_evaluator_invalid(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    assert [str(subject) for subject in subjects] == case.expected
