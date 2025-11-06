from enum import Enum
from typing import NamedTuple


class TokenType(Enum):
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    CARET = "^"

    EQUALS = "="
    NOT_EQUALS = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="

    BANG = "!"

    COMMA = ","
    LPAREN = "("
    RPAREN = ")"

    IDENT = "IDENT"
    NUMBER = "NUMBER"

    NEW_LINE = "NEW_LINE"
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"


class Token(NamedTuple):
    ttype: TokenType
    literal: str

    def __repr__(self):
        return f"Token({self.ttype}, {self.literal})"

    def __eq__(self, value) -> bool:
        return (
            isinstance(value, Token)
            and self.ttype == value.ttype
            and self.literal == value.literal
        )

    def is_symbol(self) -> bool:
        return self.ttype == TokenType.IDENT and len(self.literal) == 1
