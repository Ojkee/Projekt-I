import pytest
from typing import NamedTuple

from backend.internal.lexing import Lexer
from backend.internal.parsing.error_msgs import ParserErrorMsg
from backend.internal.statements import Statement, LineError
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser

from backend.internal.tests.parser_invalid.util_parse_invalid import AnyNonError, wrap


class Case(NamedTuple):
    name: str
    input: str
    expected: list[Statement]


CASES_PARSER_INVALID_EXPR: list[Case] = [
    # Case(
    #     name="Missing right operand after plus",
    #     input="2 +",
    #     expected=[wrap("LMAO")],
    # ),
    # Case(
    #     name="Missing right operand after minus",
    #     input="x -",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after multiply",
    #     input="5 *",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after divide",
    #     input="a /",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after power",
    #     input="2 ^",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after equals",
    #     input="x =",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after less than",
    #     input="5 <",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing right operand after greater than",
    #     input="y >",
    #     expected=[LineError(None)],
    # ),
    # # === Konsekutywne operatory ===
    # Case(
    #     name="Two operators in a row - plus plus",
    #     input="2 + + 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Two operators in a row - multiply minus",
    #     input="x * - 5",
    #     expected=[AnyNonError()],  # To może być OK: x * (-5)
    # ),
    # Case(
    #     name="Two operators in a row - divide plus",
    #     input="a / + b",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Three operators in a row",
    #     input="2 + * / 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Operator at start except minus",
    #     input="+ 5",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Multiply at start",
    #     input="* x",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Divide at start",
    #     input="/ 2",
    #     expected=[LineError(None)],  # To nie jest atom transform bez komendy
    # ),
    # Case(
    #     name="Power at start",
    #     input="^ 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Equals at start",
    #     input="= x",
    #     expected=[LineError(None)],
    # ),
    # # === Problemy z nawiasami ===
    # Case(
    #     name="Unclosed parenthesis",
    #     input="(2 + 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Unclosed nested parenthesis - outer",
    #     input="(2 + (3 * 4)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Unclosed nested parenthesis - inner",
    #     input="(2 + (3 * 4",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Unopened parenthesis",
    #     input="2 + 3)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Empty parentheses",
    #     input="()",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Empty nested parentheses",
    #     input="(())",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Only opening parenthesis",
    #     input="(",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Only closing parenthesis",
    #     input=")",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Multiple unclosed parentheses",
    #     input="((2 + 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Operator before opening paren",
    #     input="2 + (3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing operator between paren and number",
    #     input="(2) 3",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Missing operator between number and paren",
    #     input="2 (3)",
    #     expected=[LineError(None)],
    # ),
    # # === Puste wyrażenia ===
    # Case(
    #     name="Empty line",
    #     input="",
    #     expected=[],
    # ),
    # Case(
    #     name="Only whitespace",
    #     input="   ",
    #     expected=[],
    # ),
    # Case(
    #     name="Empty after operator in multiline",
    #     input="2 + 3\n\n5 * 2",
    #     expected=[AnyNonError(), AnyNonError()],
    # ),
    # # === Problemy z liczbami ===
    # Case(
    #     name="Double dot in number",
    #     input="3.14.15",
    #     expected=[LineError(None)],  # Lexer da: 3.14, ILLEGAL(.), 15
    # ),
    # Case(
    #     name="Number ending with dot",
    #     input="42.",
    #     expected=[AnyNonError()],  # Lexer da: NUMBER(42), ILLEGAL(.)
    # ),
    # Case(
    #     name="Number starting with dot",
    #     input=".5",
    #     expected=[LineError(None)],  # ILLEGAL(.), NUMBER(5)
    # ),
    # Case(
    #     name="Only dot",
    #     input=".",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Multiple dots",
    #     input="...",
    #     expected=[LineError(None)],
    # ),
    # # === Problemy z identyfikatorami ===
    # Case(
    #     name="Two identifiers without operator",
    #     input="abc def",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Identifier and number without operator",
    #     input="x 5",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Number and identifier without operator",
    #     input="5 x",
    #     expected=[LineError(None)],
    # ),
    # # === Prefix operator problems ===
    # Case(
    #     name="Minus without operand",
    #     input="-",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Double minus at start",
    #     input="--5",
    #     expected=[AnyNonError()],  # To jest OK: -(-5)
    # ),
    # Case(
    #     name="Minus with empty parentheses",
    #     input="-()",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Minus without right side in expression",
    #     input="2 + -",
    #     expected=[LineError(None)],
    # ),
    # # === Mieszane przypadki ===
    # Case(
    #     name="Operator at end of parentheses",
    #     input="(2 +)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Operator at start of parentheses",
    #     input="(+ 2)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Only operator in parentheses",
    #     input="(+)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Multiple operators at end",
    #     input="2 + 3 * + -",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Expression with only operators",
    #     input="+ - * /",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Comparison without right side",
    #     input="x < ",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Multiple comparisons",
    #     input="x < y < z",
    #     expected=[AnyNonError()],  # To może być OK semantycznie, syntaktycznie valid
    # ),
    # # === Multiline z errorami ===
    # Case(
    #     name="First line error, second valid",
    #     input="2 +\n3 * 4",
    #     expected=[LineError(None), AnyNonError()],
    # ),
    # Case(
    #     name="First line valid, second error",
    #     input="2 + 3\n5 *",
    #     expected=[AnyNonError(), LineError(None)],
    # ),
    # Case(
    #     name="Both lines error",
    #     input="2 +\n* 5",
    #     expected=[LineError(None), LineError(None)],
    # ),
    # Case(
    #     name="Middle line error",
    #     input="1 + 1\n2 *\n3 + 3",
    #     expected=[AnyNonError(), LineError(None), AnyNonError()],
    # ),
    # Case(
    #     name="All lines error",
    #     input="+\n*\n/",
    #     expected=[LineError(None), LineError(None), LineError(None)],
    # ),
    # # === Graniczné przypadki ===
    # Case(
    #     name="Very long operator chain ending with operator",
    #     input="1 + 2 - 3 * 4 / 5 ^",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Deeply nested unclosed parens",
    #     input="(((((1 + 2",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Mismatched parens depth",
    #     input="((1 + 2) + (3 * 4)",
    #     expected=[LineError(None)],
    # ),
    # Case(
    #     name="Extra closing parens",
    #     input="(1 + 2))",
    #     expected=[LineError(None)],
    # ),
]


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
