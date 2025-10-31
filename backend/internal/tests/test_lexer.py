import pytest
from dataclasses import dataclass

from backend.internal.tokens import Token, TokenType
from backend.internal.lexing import Lexer


@dataclass
class Case:
    name: str
    input: str
    expected: list[Token]


CASES_CATEGORIES = [
    Case("Empty", "", [Token(TokenType.EOF, "EOF")]),
    Case(
        "Empty whitespaces",
        "    \r   \n       ",
        [
            Token(TokenType.NEW_LINE, "\\n"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Comparison operators",
        "> < >= <=",
        [
            Token(TokenType.GT, ">"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GE, ">="),
            Token(TokenType.LE, "<="),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Math operators",
        "= + - / * ^ !=",
        [
            Token(TokenType.EQUALS, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.CARET, "^"),
            Token(TokenType.NOT_EQUALS, "!="),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Parentheses and separators",
        "( ) ,",
        [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Numbers",
        "5 2 22 103 1.4 100.1 0.0003",
        [
            Token(TokenType.NUMBER, "5"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.NUMBER, "22"),
            Token(TokenType.NUMBER, "103"),
            Token(TokenType.NUMBER, "1.4"),
            Token(TokenType.NUMBER, "100.1"),
            Token(TokenType.NUMBER, "0.0003"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
]


CASES_EXAMPLE_PROGRAMS = [
    Case(
        "Equation spreaded",
        "2 * 3 = 6 * x",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EQUALS, "="),
            Token(TokenType.NUMBER, "6"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Equation shrinked",
        "2*3=6*x",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EQUALS, "="),
            Token(TokenType.NUMBER, "6"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Equation spreaded #2",
        "2 - 3 = 6 * x + 9",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EQUALS, "="),
            Token(TokenType.NUMBER, "6"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "9"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Equation shrinked #2",
        "2-3=6*x+9",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.EQUALS, "="),
            Token(TokenType.NUMBER, "6"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "9"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Command no params",
        "/+23",
        [
            Token(TokenType.SLASH, "/"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "23"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
]

LEXER_UT: list[Case] = []
LEXER_UT.extend(CASES_CATEGORIES)
LEXER_UT.extend(CASES_EXAMPLE_PROGRAMS)


@pytest.mark.parametrize("case", LEXER_UT, ids=lambda c: c.name)
def test_lexer(case: Case) -> None:
    lexer = Lexer(case.input)
    assert lexer.tokenize() == case.expected
