from typing import Callable
from backend.internal.tokens import Token, TokenType

NULL_CODE: str = "\0"


class Lexer:
    def __init__(self, input: str) -> None:
        self._input = input

        self._pos: int = 0
        self._read_pos: int = 0
        self._current: str = ""

        self._read_content_idx: int = 0
        self._content: list[Token] = []

        self._tokenize()

    def tokenize(self) -> list[Token]:
        return self._content

    def _tokenize(self) -> None:
        self._content.clear()
        self._read_unicode()

        token = self._read_next_token()
        while token.ttype is not TokenType.EOF:
            self._content.append(token)
            token = self._read_next_token()
        self._content.append(Token(TokenType.EOF, "EOF"))

    def _read_unicode(self) -> None:
        self._current = (
            NULL_CODE
            if self._read_pos >= len(self._input)
            else self._input[self._read_pos]
        )
        self._pos = self._read_pos
        self._read_pos += 1

    def _read_next_token(self) -> Token:
        self._skip_whitespace()
        if self._pos >= len(self._input):
            return Token(TokenType.EOF, "EOF")

        token = Token(TokenType.EOF, "EOF")
        match self._current:
            case "+":
                token = Token(TokenType.PLUS, "+")
            case "-":
                token = Token(TokenType.MINUS, "-")
            case "*":
                token = Token(TokenType.ASTERISK, "*")
            case "/":
                token = Token(TokenType.SLASH, "/")
            case "^":
                token = Token(TokenType.CARET, "^")
            case "=":
                token = Token(TokenType.EQUALS, "=")
            case ",":
                token = Token(TokenType.COMMA, ",")
            case "(":
                token = Token(TokenType.LPAREN, "(")
            case ")":
                token = Token(TokenType.RPAREN, ")")
            case "\n":
                token = Token(TokenType.NEW_LINE, "\\n")
            case "!":
                if self._peek_unicode() == "=":
                    token = Token(TokenType.NOT_EQUALS, "!=")
                    self._read_unicode()
                else:
                    token = Token(TokenType.BANG, "!")
            case "<":
                if self._peek_unicode() == "=":
                    token = Token(TokenType.LE, "<=")
                    self._read_unicode()
                else:
                    token = Token(TokenType.LT, "<")
            case ">":
                if self._peek_unicode() == "=":
                    token = Token(TokenType.GE, ">=")
                    self._read_unicode()
                else:
                    token = Token(TokenType.GT, ">")
            case _:
                if is_letter(self._current):
                    literal = self._read_pred(is_letter)
                    return Token(TokenType.IDENT, literal)
                elif is_number(self._current):
                    literal = self._read_pred(number_pred())
                    return Token(TokenType.NUMBER, literal)
                else:
                    token = Token(TokenType.ILLEGAL, self._current)

        self._read_unicode()
        return token

    def _skip_whitespace(self) -> None:
        while is_whitespace(self._current):
            self._read_unicode()

    def _peek_unicode(self) -> str:
        if self._read_pos >= len(self._input):
            return NULL_CODE
        return self._input[self._read_pos]

    def _read_pred(self, pred: Callable[[str], bool]) -> str:
        start = self._pos
        while pred(self._current):
            self._read_unicode()
        return self._input[start : self._pos]


def is_whitespace(code: str) -> bool:
    whitespaces: set[str] = {" ", "\r", "\t"}
    return code in whitespaces


def is_letter(code: str) -> bool:
    c = code.lower()
    return "a" <= c and c <= "z" or code == "_"


def is_number(code: str) -> bool:
    return "0" <= code and code <= "9"


def number_pred() -> Callable[[str], bool]:
    seen_dot = False

    def inner(code: str) -> bool:
        nonlocal seen_dot
        if is_number(code):
            return True
        elif (code == ".") and not seen_dot:
            seen_dot = True
            return True
        return False

    return inner
