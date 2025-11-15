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


CASES_EVALUATOR_FORMULA_POWERS: list[Case] = [
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
        name="Product of powers rule in equation lhs",
        input="a^3*a^4=x\n!product_of_powers a^3*a^4\n",
        expected=[
            "EQUATION(((a^3.0)*(a^4.0)) = x)",
            "EQUATION((a^(3.0+4.0)) = x)",
        ],
    ),
    Case(
        name="Product of powers rule in equation rhs",
        input="x=a^3*a^4\n!product_of_powers a^3*a^4\n",
        expected=[
            "EQUATION(x = ((a^3.0)*(a^4.0)))",
            "EQUATION(x = (a^(3.0+4.0)))",
        ],
    ),
    Case(
        name="Product of powers rule in equation rhs",
        input="a^3*a^4 = a^3*a^4\n!product_of_powers a^3*a^4\n",
        expected=[
            "EQUATION(((a^3.0)*(a^4.0)) = ((a^3.0)*(a^4.0)))",
            "EQUATION((a^(3.0+4.0)) = (a^(3.0+4.0)))",
        ],
    ),
]

CASES_EVALUATOR_FORMULA_POWERS_FRACTIONS: list[Case] = [
    Case(
        name="Quotient of Powers rule in expression",
        input="a^5/a^3\n!quotient_of_powers a^5/a^3\n",
        expected=[
            "EXPR(((a^5.0)*((a^3.0)^-1)))",
            "EXPR((a^(5.0+(3.0*-1.0))))",
        ],
    ),
    Case(
        name="Power of a quotient in expression",
        input="(a/b)^(3x)\n!power_of_a_quotient (a/b)^(3x)",
        expected=[
            "EXPR(((a*(b^-1))^(3.0*x)))",
            "EXPR(((a^(3.0*x))*((b^(3.0*x))^-1.0)))",
        ],
    ),
    Case(
        name="Quotient of Powers rule in expression reversed",
        input="a^(4-x)\n!quotient_of_powers a^(4-x)\n",
        expected=[
            "EXPR((a^(4.0+(x*-1))))",
            "EXPR(((a^4.0)*((a^x)^-1.0)))",
        ],
    ),
    Case(
        name="Power of a quotient in expression reversed",
        input="(a^9)/(b^9)\n!power_of_a_quotient (a^9)/(b^9)",
        expected=[
            "EXPR(((a^9.0)*((b^9.0)^-1)))",
            "EXPR(((a*(b^-1.0))^9.0))",
        ],
    ),
]

CASES_EVALUATOR_FORMULA_BINOMIAL_IDENTITIES: list[Case] = [
    # Case(
    #     name="Square of a difference in expression",
    #     input="(2a + 3b)^2\n!square_of_a_difference (2a + 3b)^2",
    #     expected=[
    #         "EXPR((((2.0*a)+(3.0*b))^2.0))",
    #         "EXPR(((((2.0*a)^2.0)+(((2.0*(2.0*a))*(3.0*b))*-1.0))+((3.0*b)^2.0)))",
    #     ],
    # ),
    # Case(
    #     name="Square of a Difference in expression",
    #     input="(2a)^2 - 2*(2a)*(3b) + (3b)^2\n!square_of_a_difference (2a)^2 - 2*(2a)*(3b) + (3b)^2",
    #     expected=[
    #         "EXPR(((((2.0*a)^2.0)+(((2.0*(2.0*a))*(3.0*b))*-1))+((3.0*b)^2.0)))",
    #         "EXPR((((2.0*a)+(3.0*b))^2.0))",
    #     ],
    # ),
]

CASES_EVALUATOR_FORMULA: list[Case] = []
CASES_EVALUATOR_FORMULA.extend(CASES_EVALUATOR_FORMULA_POWERS)
CASES_EVALUATOR_FORMULA.extend(CASES_EVALUATOR_FORMULA_POWERS_FRACTIONS)
CASES_EVALUATOR_FORMULA.extend(CASES_EVALUATOR_FORMULA_BINOMIAL_IDENTITIES)


@pytest.mark.parametrize("case", CASES_EVALUATOR_FORMULA, ids=lambda c: c.name)
def test_evaluator_formula(case: Case) -> None:
    # if case.name == "Power of a quotient in expression reversed":
    #     import pdb
    #
    #     pdb.set_trace()
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    evaluator = Evaluator()
    subjects = evaluator.eval(program)

    print(repr(subjects))
    assert [repr(subject) for subject in subjects] == case.expected
