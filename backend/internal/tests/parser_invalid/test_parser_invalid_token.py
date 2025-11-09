import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorUserMsg
from backend.internal.statements import Statement
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser

from backend.internal.tests.parser_invalid.util_parse_invalid import (
    AnyNonErrorStatement,
    wrap,
)


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


CASES_PARSER_INVALID_TOKENS: list[Case] = [
    Case(
        name="Illegal at start of line",
        input="@",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal in middle of expression",
        input="2 + @ * 3",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal after operator",
        input="x + $ - 5",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal before operator",
        input="x # + 5",
        expected=[wrap(ParserErrorUserMsg.illegal_str("#"))],
    ),
    Case(
        name="Illegal inside parentheses",
        input="(2 + &)",
        expected=[wrap(ParserErrorUserMsg.illegal_str("&"))],
    ),
    Case(
        name="Illegal after opening paren",
        input="(@ + 2)",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal before closing paren",
        input="(2 + 3 $)",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal at end of expression",
        input="2 + 3 @",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Multiple illegals in line",
        input="x @ y # z",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal in formula parameters",
        input="!func x, #, y",
        expected=[wrap(ParserErrorUserMsg.illegal_str("#"))],
    ),
    Case(
        name="Illegal in atom transform",
        input="/+ x & 2",
        expected=[wrap(ParserErrorUserMsg.illegal_str("&"))],
    ),
    Case(
        name="Illegal after atom operator",
        input="/$ x",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal in nested parentheses",
        input="(2 + (3 @ 4))",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal between identifiers",
        input="abc $ def",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal in number",
        input="3.14$59",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal after comma",
        input="!func a, @, b",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal as prefix operator",
        input="@ 5",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal with valid multiline",
        input="x + 2\ny @ z",
        expected=[
            AnyNonErrorStatement(),
            wrap(ParserErrorUserMsg.illegal_str("@")),
        ],
    ),
    Case(
        name="Multiple statements with illegal in second",
        input="1 + 1\n@ + 2\n3 + 3",
        expected=[
            AnyNonErrorStatement(),
            wrap(ParserErrorUserMsg.illegal_str("@")),
        ],
    ),
]


@pytest.mark.parametrize("case", CASES_PARSER_INVALID_TOKENS, ids=lambda c: c.name)
def test_parser_invalid_tokens(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert case.expected == program.get()
