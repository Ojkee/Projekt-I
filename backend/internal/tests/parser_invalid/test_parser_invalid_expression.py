import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorMsg
from backend.internal.statements import Statement
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser

from backend.internal.tests.parser_invalid.util_parse_invalid import AnyNonError, wrap


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


CASES_PARSER_INVALID_EXPR: list[Case] = []


@pytest.mark.parametrize("case", CASES_PARSER_INVALID_EXPR, ids=lambda c: c.name)
def test_parser_invalid_expr(case: Case) -> None:
    # if case.name == "Illegal after atom operator":
    #     import pdb
    #
    #     pdb.set_trace()

    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert case.expected == program.get()
