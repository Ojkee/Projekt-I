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


CASES_EVALUATOR_FORMULA: list[Case] = [
    Case(
        name="Product of powers rule",
        input="a^3*a^4\n!product_of_powers a^3*a^4\n",
        expected=[
            "EXPR(((a^3.0)*(a^4.0)))",
            "EXPR((a^(3.0+4.0)))",
        ],
    ),
    Case(
        name="Product of powers rule reversed",
        input="a^(4 + x)\n!product_of_powers a^(4 + x)\n",
        expected=[
            "EXPR((a^(4.0+x)))",
            "EXPR(((a^4.0)*(a^x)))",
        ],
    ),
    Case(
        name="Product of powers rule nested",
        input="a^(3y)*a^4\n!product_of_powers a^(3y)*a^4\n",
        expected=[
            "EXPR(((a^(3.0*y))*(a^4.0)))",
            "EXPR((a^((3.0*y)+4.0)))",
        ],
    ),
    Case(
        name="Product of powers rule in equation",
        input="a^3*a^4=x\n!product_of_powers a^3*a^4\n",
        expected=[
            "EQUATION(((a^3.0)*(a^4.0)) = x)",
            "EQUATION((a^(3.0+4.0)) = x)",
        ],
    ),
]


@pytest.mark.parametrize("case", CASES_EVALUATOR_FORMULA, ids=lambda c: c.name)
def test_evaluator_formula(case: Case) -> None:

    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    assert [repr(subject) for subject in subjects] == case.expected
