import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorUserMsg
from backend.internal.statements import Statement
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser

from backend.internal.tests.parser_invalid.util_parse_invalid import (
    AnyNonErrorStatement,
    wrap_stmt,
)


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


CASES_PARSER_INVALID_EXPR: list[Case] = [
    Case(
        name="Missing right operand after plus",
        input="2 + \n",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Missing right operand after minus",
        input="x -",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("x", "-"))],
    ),
    Case(
        name="Missing right operand after multiply",
        input="5 *",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("5", "*"))],
    ),
    Case(
        name="Missing right operand after divide",
        input="a /",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("a", "/"))],
    ),
    Case(
        name="Missing right operand after power",
        input="2 ^",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "^"))],
    ),
    Case(
        name="Missing right operand after equals",
        input="x =",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("x", "="))],
    ),
    Case(
        name="Two operators in a row - plus plus",
        input="2 + + 3",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Two operators in a row - multiply minus",
        input="x * - 5",
        expected=[AnyNonErrorStatement()],
    ),
    Case(
        name="Two operators in a row - divide plus",
        input="a / + b",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("a", "/"))],
    ),
    Case(
        name="Three operators in a row",
        input="2 + * / 3",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Operator at start except minus",
        input="+ 5",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("+"))],
    ),
    Case(
        name="Multiply at start",
        input="* x",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("*"))],
    ),
    Case(
        name="Power at start",
        input="^ 3",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("^"))],
    ),
    Case(
        name="Equals at start",
        input="= x",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("="))],
    ),
    Case(
        name="Unclosed parenthesis",
        input="(2 + 3",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Unclosed nested parenthesis - outer",
        input="(2 + (3 * 4)",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Unclosed nested parenthesis - inner",
        input="(2 + (3 * 4",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Unopened parenthesis",
        input="2 + 3)",
        expected=[wrap_stmt(ParserErrorUserMsg.extra_input_in_line(")"))],
    ),
    Case(
        name="Empty parentheses",
        input="()",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Empty nested parentheses",
        input="(())",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Only opening parenthesis",
        input="(",
        expected=[wrap_stmt(ParserErrorUserMsg.unexpected_eof())],
    ),
    Case(
        name="Only closing parenthesis",
        input=")",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Minus with empty parentheses",
        input="-()",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix(")"))],
    ),
    Case(
        name="Multiple unclosed parentheses",
        input="((2 + 3",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Operator before opening paren",
        input="2 + (3",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Double dot in number",
        input="3.14.15",
        expected=[wrap_stmt(ParserErrorUserMsg.illegal_str("."))],
    ),
    Case(
        name="Number starting with dot",
        input=".5",
        expected=[wrap_stmt(ParserErrorUserMsg.illegal_str("."))],
    ),
    Case(
        name="Only dot",
        input=".",
        expected=[wrap_stmt(ParserErrorUserMsg.illegal_str("."))],
    ),
    Case(
        name="Multiple dots",
        input="...",
        expected=[wrap_stmt(ParserErrorUserMsg.illegal_str("."))],
    ),
    Case(
        name="Two identifiers without operator",
        input="abc def",
        expected=[wrap_stmt(ParserErrorUserMsg.extra_input_in_line("d"))],
    ),
    Case(
        name="Minus without operand",
        input="-",
        expected=[wrap_stmt(ParserErrorUserMsg.unexpected_eof())],
    ),
    Case(
        name="Minus without right side in expression",
        input="2 + -",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Operator at end of parentheses",
        input="(2 +)",
        expected=[wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "+"))],
    ),
    Case(
        name="Operator at start of parentheses",
        input="(+ 2)",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("+"))],
    ),
    Case(
        name="Only operator in parentheses",
        input="(+)",
        expected=[wrap_stmt(ParserErrorUserMsg.invalid_prefix("+"))],
    ),
    Case(
        name="First line valid, second error",
        input="2 + 3\n5 *",
        expected=[
            AnyNonErrorStatement(),
            wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("5", "*")),
        ],
    ),
    Case(
        name="Middle line error",
        input="1 + 1\n2 *\n3 + 3",
        expected=[
            AnyNonErrorStatement(),
            wrap_stmt(ParserErrorUserMsg.missing_rhs_in_expr("2", "*")),
        ],
    ),
    Case(
        name="Mismatched parens depth",
        input="((1 + 2) + (3 * 4)",
        expected=[wrap_stmt(ParserErrorUserMsg.no_rparen())],
    ),
    Case(
        name="Extra closing parens",
        input="(1 + 2))",
        expected=[wrap_stmt(ParserErrorUserMsg.extra_input_in_line(")"))],
    ),
]


@pytest.mark.parametrize("case", CASES_PARSER_INVALID_EXPR, ids=lambda c: c.name)
def test_parser_invalid_expr(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert case.expected == program.get()
