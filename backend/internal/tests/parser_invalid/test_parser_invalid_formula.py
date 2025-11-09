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


CASES_PARSER_INVALID_FORMULA: list[Case] = [
    Case(
        name="Bang alone",
        input="!",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with newline",
        input="!\n",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with only whitespace",
        input="!   ",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with number as name",
        input="!123",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with operator as name",
        input="!+",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with illegal char",
        input="!@func",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Bang with lparen",
        input="!(func)",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Bang with comma",
        input="!,",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Multiple trailing commas",
        input="!func x,,",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Comma at start of params",
        input="!func ,x",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Only comma as param",
        input="!func ,",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Consecutive commas",
        input="!func x,,y",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Illegal char in first param",
        input="!func @x",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal char in middle param",
        input="!func x, @y, z",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Illegal char in last param",
        input="!func x, y, #",
        expected=[wrap(ParserErrorUserMsg.illegal_str("#"))],
    ),
    Case(
        name="Multiple illegals in params",
        input="!func @, $, %",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Incomplete expression in param",
        input="!func 2 +",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Incomplete expression after comma",
        input="!func x, 3 *",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("3", "*"))],
    ),
    Case(
        name="Multiple incomplete expressions",
        input="!func 2+, 3*",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Operator without operand in param",
        input="!func +",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix("+"))],
    ),
    Case(
        name="Operator without operand after comma",
        input="!func x, *",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix("*"))],
    ),
    Case(
        name="Unclosed paren in param",
        input="!func (x + 2",
        expected=[wrap(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Unclosed paren in second param",
        input="!func x, (y + 3",
        expected=[wrap(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Empty parens in param",
        input="!func ()",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Empty parens after comma",
        input="!func x, ()",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Unopened paren in param",
        input="!func x + 2)",
        expected=[wrap(ParserErrorUserMsg.missing_comma_in_formula())],
    ),
    Case(
        name="Mismatched parens in params",
        input="!func (x + y), z)",
        expected=[wrap(ParserErrorUserMsg.missing_comma_in_formula())],
    ),
    Case(
        name="Consecutive operators in param",
        input="!func 2 + + 3",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Consecutive operators after comma",
        input="!func x, 2 * / 3",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("2", "*"))],
    ),
    Case(
        name="Missing operator between params",
        input="!func x y",
        expected=[wrap(ParserErrorUserMsg.missing_comma_in_formula())],
    ),
    Case(
        name="Only commas",
        input="!func ,,,",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Comma before name",
        input="!, func",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Double comma with spaces",
        input="!func x, , y",
        expected=[wrap(ParserErrorUserMsg.invalid_prefix(","))],
    ),
    Case(
        name="Invalid name and trailing comma",
        input="!123 x,",
        expected=[wrap(ParserErrorUserMsg.no_formula_name())],
    ),
    Case(
        name="Illegal in name and params",
        input="!@func #x",
        expected=[wrap(ParserErrorUserMsg.illegal_str("@"))],
    ),
    Case(
        name="Nested unclosed parens",
        input="!func ((x + y)",
        expected=[wrap(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Error in 5th parameter",
        input="!func a, b, c, d, e +",
        expected=[wrap(ParserErrorUserMsg.missing_rhs_in_expr("e", "+"))],
    ),
    Case(
        name="Valid expression then invalid formula",
        input="x + 2\n!",
        expected=[
            AnyNonErrorStatement(),
            wrap(ParserErrorUserMsg.no_formula_name()),
        ],
    ),
    Case(
        name="Multiple invalid formulas",
        input="!\n!123\n!func ,",
        expected=[
            wrap(ParserErrorUserMsg.no_formula_name()),
        ],
    ),
    Case(
        name="Mix of valid and invalid",
        input="x\n!func @\ny",
        expected=[
            AnyNonErrorStatement(),
            wrap(ParserErrorUserMsg.illegal_str("@")),
        ],
    ),
]


@pytest.mark.parametrize("case", CASES_PARSER_INVALID_FORMULA, ids=lambda c: c.name)
def test_parser_invalid_formula(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert case.expected == program.get()
