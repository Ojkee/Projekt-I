package lexer

import (
	"app/internal/token"
)

type InputType []rune

type Lexer struct {
	input   InputType
	pos     int  // Points to current
	readPos int  // Points to next character after current
	current rune // Current rune

	readContentIdx int
	content        []token.Token
}

func New(input string) *Lexer {
	lexer := Lexer{
		input:   []rune(input),
		pos:     0,
		readPos: 0,

		readContentIdx: 0,
		content:        make([]token.Token, 0),
	}
	lexer.tokenize()
	return &lexer
}

func (lexer *Lexer) Tokenize() []token.Token {
	return lexer.content
}

func (lexer *Lexer) tokenize() {
	lexer.readRune()

	tokens := make([]token.Token, 0)
	tok := lexer.readNextToken()
	for ; tok.Type != token.EOF; tok = lexer.readNextToken() {
		tokens = append(tokens, tok)
	}
	tokens = append(tokens, token.New(token.EOF, "EOF"))
	lexer.content = tokens
}

func (lexer *Lexer) readNextToken() token.Token {
	lexer.skipWhitespace()
	if lexer.pos >= len(lexer.input) {
		return token.New(token.EOF, "EOF")
	}

	var tok token.Token
	switch lexer.current {
	case '+':
		tok = token.New(token.PLUS, "+")
	case '-':
		tok = token.New(token.MINUS, "-")
	case '*':
		tok = token.New(token.ASTERISK, "*")
	case '/':
		tok = token.New(token.SLASH, "/")
	case '^':
		tok = token.New(token.CARET, "^")
	case '=':
		tok = token.New(token.EQUALS, "=")
	case '!':
		if lexer.peekRune() == '=' {
			tok = token.New(token.NOT_EQUALS, "!=")
			lexer.readRune()
		} else {
			tok = token.New(token.BANG, "!")
		}
	case '<':
		if lexer.peekRune() == '=' {
			tok = token.New(token.LE, "<=")
			lexer.readRune()
		} else {
			tok = token.New(token.LT, "<")
		}
	case '>':
		if lexer.peekRune() == '=' {
			tok = token.New(token.GE, ">=")
			lexer.readRune()
		} else {
			tok = token.New(token.GT, ">")
		}
	case ',':
		tok = token.New(token.COMMA, ",")
	case '(':
		tok = token.New(token.LPAREN, "(")
	case ')':
		tok = token.New(token.RPAREN, ")")
	case '\n':
		tok = token.New(token.NEW_LINE, "\\n")
	default:
		if isLetter(lexer.current) {
			literal := lexer.readPred(isLetter)
			tok = token.New(token.IDENT, literal)
			return tok
		} else if isNumber(lexer.current) {
			literal := lexer.readPred(numberPred())
			tok = token.New(token.NUMBER, literal)
			return tok
		} else {
			tok = token.New(token.ILLEGAL, string(lexer.current))
		}
	}

	lexer.readRune()
	return tok
}

func (lexer *Lexer) skipWhitespace() {
	for isWhitespace(lexer.current) {
		lexer.readRune()
	}
}

func isWhitespace(r rune) bool {
	return r == '\t' || r == '\r' || r == ' '
}

func isLetter(r rune) bool {
	return ('a' <= r && r <= 'z') || ('A' <= r && r <= 'Z') || r == '_'
}

func isNumber(r rune) bool {
	return ('0' <= r && r <= '9')
}

func numberPred() func(rune) bool {
	seenDot := false
	return func(r rune) bool {
		if isNumber(r) {
			return true
		}
		if (r == '.') && !seenDot {
			seenDot = true
			return true
		}
		return false
	}
}

func (lexer *Lexer) peekRune() rune {
	if lexer.readPos >= len(lexer.input) {
		return 0
	}
	return lexer.input[lexer.readPos]
}

func (lexer *Lexer) readPred(pred func(rune) bool) string {
	start := lexer.pos
	for pred(lexer.current) {
		lexer.readRune()
	}
	literal := lexer.input[start:lexer.pos]
	return string(literal)
}

func (lexer *Lexer) readRune() {
	if lexer.readPos >= len(lexer.input) {
		lexer.current = 0
	} else {
		lexer.current = lexer.input[lexer.readPos]
	}
	lexer.pos = lexer.readPos
	lexer.readPos += 1
}
