import pytest
from dataclasses import dataclass

from backend.internal.expressions import Prefix, Infix, Identifier, Number
from backend.internal.lexing import Lexer
from backend.internal.statements import Statement, Subject
from backend.internal.tokens import Token, TokenType
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser


@dataclass
class Case:
    name: str
    input: str
    expected: list[Statement]


CASES_ALGEBRAIC = [
    Case(
        "Simple expr",
        "x = 3",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Identifier(Token(TokenType.IDENT, "x")),
                    Number(3.0),
                )
            ),
        ],
    ),
    Case(
        "Infix mul expr lhs",
        "2*x = 3",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Number(2.0),
                        Identifier(Token(TokenType.IDENT, "x")),
                    ),
                    Number(3.0),
                )
            ),
        ],
    ),
    Case(
        "Infix mul expr lhs x front",
        "x*2 = 3",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Identifier(Token(TokenType.IDENT, "x")),
                        Number(2.0),
                    ),
                    Number(3.0),
                )
            ),
        ],
    ),
    Case(
        "Infix mul expr rhs",
        "2 = 3*x",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Number(2.0),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Number(3.0),
                        Identifier(Token(TokenType.IDENT, "x")),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Infix mul expr rhs x front",
        "2 = x*3",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Number(2.0),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Identifier(Token(TokenType.IDENT, "x")),
                        Number(3.0),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Prefix lhs",
        "-2 = x",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Prefix(
                        Token(TokenType.MINUS, "-"),
                        Number(2.0),
                    ),
                    Identifier(Token(TokenType.IDENT, "x")),
                )
            ),
        ],
    ),
    Case(
        "Prefix rhs",
        "2 = -x",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Number(2.0),
                    Prefix(
                        Token(TokenType.MINUS, "-"),
                        Identifier(Token(TokenType.IDENT, "x")),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Infix mixed precedence with floats",
        "a = x*3 + y/2 - z^2.5 + 7.0",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Identifier(Token(TokenType.IDENT, "a")),
                    Infix(
                        Token(TokenType.PLUS, "+"),
                        Infix(
                            Token(TokenType.MINUS, "-"),
                            Infix(
                                Token(TokenType.PLUS, "+"),
                                Infix(
                                    Token(TokenType.ASTERISK, "*"),
                                    Identifier(Token(TokenType.IDENT, "x")),
                                    Number(3.0),
                                ),
                                Infix(
                                    Token(TokenType.SLASH, "/"),
                                    Identifier(Token(TokenType.IDENT, "y")),
                                    Number(2.0),
                                ),
                            ),
                            Infix(
                                Token(TokenType.CARET, "^"),
                                Identifier(Token(TokenType.IDENT, "z")),
                                Number(2.5),
                            ),
                        ),
                        Number(7.0),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Redundant grouped",
        "(x + y) = 2",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Infix(
                        Token(TokenType.PLUS, "+"),
                        Identifier(Token(TokenType.IDENT, "x")),
                        Identifier(Token(TokenType.IDENT, "y")),
                    ),
                    Number(2.0),
                )
            ),
        ],
    ),
    Case(
        "Basic grouped",
        "2*(x + y) = 3",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Number(2.0),
                        Infix(
                            Token(TokenType.PLUS, "+"),
                            Identifier(Token(TokenType.IDENT, "x")),
                            Identifier(Token(TokenType.IDENT, "y")),
                        ),
                    ),
                    Number(3.0),
                )
            ),
        ],
    ),
    Case(
        "Basic grouped rhs",
        "2 = 3*(x + 5)",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Number(2.0),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Number(3.0),
                        Infix(
                            Token(TokenType.PLUS, "+"),
                            Identifier(Token(TokenType.IDENT, "x")),
                            Number(5.0),
                        ),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Redundant parens",
        "(2) = x",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Number(2.0),
                    Identifier(Token(TokenType.IDENT, "x")),
                )
            ),
        ],
    ),
    Case(
        "Group with caret and mul",
        "(2 + x) ^ 3 = (y - 4) * 5",
        [
            Subject(
                Infix(
                    Token(TokenType.EQUALS, "="),
                    Infix(
                        Token(TokenType.CARET, "^"),
                        Infix(
                            Token(TokenType.PLUS, "+"),
                            Number(2.0),
                            Identifier(Token(TokenType.IDENT, "x")),
                        ),
                        Number(3.0),
                    ),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Infix(
                            Token(TokenType.MINUS, "-"),
                            Identifier(Token(TokenType.IDENT, "y")),
                            Number(4.0),
                        ),
                        Number(5.0),
                    ),
                )
            ),
        ],
    ),
    Case(
        "Nested grouping",
        "2^(3*(4 + y))",
        [
            Subject(
                Infix(
                    Token(TokenType.CARET, "^"),
                    Number(2.0),
                    Infix(
                        Token(TokenType.ASTERISK, "*"),
                        Number(3.0),
                        Infix(
                            Token(TokenType.PLUS, "+"),
                            Number(4.0),
                            Identifier(Token(TokenType.IDENT, "y")),
                        ),
                    ),
                )
            ),
        ],
    ),
]


@pytest.mark.parametrize("case", CASES_ALGEBRAIC, ids=[c.name for c in CASES_ALGEBRAIC])
def test_parser_algebraic(case: Case) -> None:
    lexer = Lexer(case.input)
    stream = TokenStream(lexer)
    parser = Parser(stream)
    program = parser.parse()
    assert program.get() == case.expected
