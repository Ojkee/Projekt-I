from typing import NamedTuple
import pytest

from backend.internal.lexing import Lexer
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser
from backend.internal.evaluators import Evaluator


class Case(NamedTuple):
    name: str
    input: str
    expected: list[str]


CASES_EVALUATOR_FORMULA: list[Case] = []


# TODO
@pytest.mark.parametrize("case", CASES_EVALUATOR_FORMULA, ids=lambda c: c.name)
def test_evaluator_formula(case: Case) -> None:

    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    assert [repr(subject) for subject in subjects] == case.expected
