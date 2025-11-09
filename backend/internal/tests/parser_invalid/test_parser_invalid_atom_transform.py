import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorUserMsg
from backend.internal.statements import Statement
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser

from backend.internal.tests.parser_invalid.util_parse_invalid import AnyNonError, wrap


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


CASES_PARSER_INVALID_ATOM_TRANSFORM: list[Case] = [
    Case(
        name="Slash alone",
        input="/",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("/"))],
    ),
    Case(
        name="Slash with only newline",
        input="/\n",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("/"))],
    ),
    Case(
        name="Plus operator without expression",
        input="/+",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("+"))],
    ),
    Case(
        name="Minus operator without expression",
        input="/-",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("-"))],
    ),
    Case(
        name="Multiply operator without expression",
        input="/*",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("*"))],
    ),
    Case(
        name="Power operator without expression",
        input="/^",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("^"))],
    ),
    Case(
        name="Plus operator with newline",
        input="/+\n",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("+"))],
    ),
    Case(
        name="Invalid operator - equals",
        input="/= x",
        expected=[wrap(ParserErrorUserMsg.invalid_atom_prefix("="))],
    ),
    Case(
        name="Invalid operator - greater than",
        input="/> 3",
        expected=[wrap(ParserErrorUserMsg.invalid_atom_prefix(">"))],
    ),
    Case(
        name="Invalid operator - rparen",
        input="/) x",
        expected=[wrap(ParserErrorUserMsg.invalid_atom_prefix(")"))],
    ),
    Case(
        name="Invalid operator - comma",
        input="/, x",
        expected=[wrap(ParserErrorUserMsg.invalid_atom_prefix(","))],
    ),
    Case(
        name="Invalid operator - bang",
        input="/! x",
        expected=[wrap(ParserErrorUserMsg.invalid_atom_prefix("!"))],
    ),
    Case(
        name="Illegal after slash",
        input="/@ x",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal as operator",
        input="/$ 5",
        expected=[wrap(ParserErrorUserMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal in expression",
        input="/+ x @ y",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Division with incomplete expression",
        input="/2 +",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Unclosed parenthesis in division",
        input="/(2 + 3",
        expected=[wrap(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Unclosed parenthesis in plus atom",
        input="/+ (x * y",
        expected=[wrap(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Empty parentheses in atom",
        input="/+ ()",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("+"))],
    ),
    Case(
        name="Consecutive invalid operators",
        input="/+ + x",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("+"))],
    ),
    Case(
        name="Only whitespace after slash",
        input="/   ",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("/"))],
    ),
    Case(
        name="Only whitespace after operator",
        input="/+   ",
        expected=[wrap(ParserErrorUserMsg.expected_expression_after("+"))],
    ),
    Case(
        name="Empty atom in middle",
        input="/+ 1\n/\n/- 2",
        expected=[
            AnyNonError(),
            wrap(ParserErrorUserMsg.expected_expression_after("/")),
        ],
    ),
]


@pytest.mark.parametrize(
    "case", CASES_PARSER_INVALID_ATOM_TRANSFORM, ids=lambda c: c.name
)
def test_parser_invalid_atom_transform(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert case.expected == program.get()
