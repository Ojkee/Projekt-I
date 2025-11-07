import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorMsg
from backend.internal.parsing.parseerror import ParseErr
from backend.internal.statements import Statement, LineError
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser


class AnyNonError(Statement):
    def __str__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: Statement) -> bool:
        if isinstance(other, LineError):
            return False
        return True


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


def wrap(msg: str) -> LineError:
    return LineError(ParseErr(msg))


CASES_PARSER_INVALID_TOKENS: list[Case] = [
    Case(
        name="Illegal at start of line",
        input="@",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal in middle of expression",
        input="2 + @ * 3",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal after operator",
        input="x + $ - 5",
        expected=[wrap(ParserErrorMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal before operator",
        input="x # + 5",
        expected=[wrap(ParserErrorMsg.illegal_str("#"))],
    ),
    Case(
        name="Illegal inside parentheses",
        input="(2 + &)",
        expected=[wrap(ParserErrorMsg.illegal_str("&"))],
    ),
    Case(
        name="Illegal after opening paren",
        input="(@ + 2)",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal before closing paren",
        input="(2 + 3 $)",
        expected=[wrap(ParserErrorMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal at end of expression",
        input="2 + 3 @",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Multiple illegals in line",
        input="x @ y # z",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal in formula parameters",
        input="!func x, #, y",
        expected=[wrap(ParserErrorMsg.illegal_str("#"))],
    ),
    Case(
        name="Illegal in atom transform",
        input="/+ x & 2",
        expected=[wrap(ParserErrorMsg.illegal_str("&"))],
    ),
    Case(
        name="Illegal after atom operator",
        input="/$ x",
        expected=[wrap(ParserErrorMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal in nested parentheses",
        input="(2 + (3 @ 4))",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal between identifiers",
        input="abc $ def",
        expected=[wrap(ParserErrorMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal in number",
        input="3.14$59",
        expected=[wrap(ParserErrorMsg.illegal_str("$"))],
    ),
    Case(
        name="Illegal after comma",
        input="!func a, @, b",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal as prefix operator",
        input="@ 5",
        expected=[wrap(ParserErrorMsg.illegal_str("@"))],
    ),
    # Case(
    #     name="Illegal with valid multiline",
    #     input="x + 2\ny @ z",
    #     expected=[
    #         AnyNonError(),
    #         wrap(ParserErrorMsg.illegal_str("@")),
    #     ],
    # ),
    # Case(
    #     name="Multiple statements with illegal in second",
    #     input="1 + 1\n@ + 2\n3 + 3",
    #     expected=[AnyNonError(), LineError(None), AnyNonError()],
    # ),
]

CASES_PARSER_INVALID: list[Case] = []
CASES_PARSER_INVALID.extend(CASES_PARSER_INVALID_TOKENS)


@pytest.mark.parametrize("case", CASES_PARSER_INVALID, ids=lambda c: c.name)
def test_parser_invalid(case: Case) -> None:
    # if case.name == "Illegal after atom operator":
    #     import pdb
    #
    #     pdb.set_trace()

    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    program_strs = [str(stmt) for stmt in program.get()]
    expected_strs = [str(stmt) for stmt in case.expected]
    assert program_strs == expected_strs
