package token

type TokenType string

const (
	PLUS     = "+"
	MINUS    = "-"
	ASTERISK = "*"
	SLASH    = "/"
	CARET    = "^"

	EQUALS     = "="
	NOT_EQUALS = "!="
	LT         = "<"
	LE         = "<="
	GT         = ">"
	GE         = ">="

	BANG = "!"

	COMMA  = ","
	LPAREN = "("
	RPAREN = ")"

	IDENT  = "IDENT"
	NUMBER = "NUMBER"

	NEW_LINE = "NEW_LINE"
	EOF      = "EOF"
	ILLEGAL  = "ILLEGAL"
)

type Token struct {
	Type    TokenType
	Literal string
}

func New(tokenType TokenType, literal string) Token {
	return Token{
		Type:    tokenType,
		Literal: literal,
	}
}

func (tok *Token) IsSymbol() bool {
	return tok.Type == IDENT && len(tok.Literal) == 1
}
