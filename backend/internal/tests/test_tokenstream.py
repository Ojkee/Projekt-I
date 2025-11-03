import pytest
from dataclasses import dataclass

from backend.internal.tokens import Token, TokenType
from backend.internal.lexing import Lexer
from backend.internal.tokenstreams import TokenStream


@dataclass
class Case:
    name: str
    input: str
    expected: list[Token]


CASES_PREPROCESS = [
    Case(
        "Multiply num ident",
        "2x",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply ident-ident",
        "yx",
        [
            Token(TokenType.IDENT, "y"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply num-parens",
        "2(x + 3)",
        [
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply parens-num",
        "(x + 3)2",
        [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply ident-parens",
        "y(x + 3)",
        [
            Token(TokenType.IDENT, "y"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply parens-ident",
        "(x + 3)y",
        [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply paren-paren",
        "(y * 4)(x + 3)",
        [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.NUMBER, "4"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        "Multiply complex",
        "a(bcd * 4)ef((g + 3)hh)",
        [
            Token(TokenType.IDENT, "a"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "b"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "c"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "d"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.NUMBER, "4"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "e"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "f"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "g"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.NUMBER, "3"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "h"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "h"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
]

CASES_TOKEN_FORMULA = [
    Case(
        name="Simple formula",
        input="!formula",
        expected=[
            Token(TokenType.BANG, "!"),
            Token(TokenType.IDENT, "formula"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
    Case(
        name="Simple formula",
        input="!formula x, y, 2x",
        expected=[
            Token(TokenType.BANG, "!"),
            Token(TokenType.IDENT, "formula"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.NUMBER, "2"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.EOF, "EOF"),
        ],
    ),
]

TOKEN_UT: list[Case] = []
TOKEN_UT.extend(CASES_PREPROCESS)
TOKEN_UT.extend(CASES_TOKEN_FORMULA)


@pytest.mark.parametrize("case", TOKEN_UT, ids=[c.name for c in TOKEN_UT])
def test_lexer(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    assert stream.preprocess() == case.expected
