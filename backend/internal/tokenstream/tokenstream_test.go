package tokenstream_test

import (
	"reflect"
	"testing"

	fn "app/internal/functional"
	lexer_api "app/internal/lexer"
	"app/internal/token"
	"app/internal/tokenstream"
)

func TestTokenStreamPreprocess(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []token.Token
	}{
		"Multiply num ident": {
			input: "2x",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply ident-ident": {
			input: "yx",
			expected: []token.Token{
				token.New(token.IDENT, "y"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply num-parens": {
			input: "2(x + 3)",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.ASTERISK, "*"),
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply parens-num": {
			input: "(x + 3)2",
			expected: []token.Token{
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.ASTERISK, "*"),
				token.New(token.NUMBER, "2"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply ident-parens": {
			input: "y(x + 3)",
			expected: []token.Token{
				token.New(token.IDENT, "y"),
				token.New(token.ASTERISK, "*"),
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply parens-ident": {
			input: "(x + 3)y",
			expected: []token.Token{
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "y"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply paren-paren": {
			input: "(y * 4)(x + 3)",
			expected: []token.Token{
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "y"),
				token.New(token.ASTERISK, "*"),
				token.New(token.NUMBER, "4"),
				token.New(token.RPAREN, ")"),
				token.New(token.ASTERISK, "*"),
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Multiply complex": {
			input: "a(bcd * 4)ef((g + 3)hh)",
			expected: []token.Token{
				token.New(token.IDENT, "a"),
				token.New(token.ASTERISK, "*"),
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "b"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "c"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "d"),
				token.New(token.ASTERISK, "*"),
				token.New(token.NUMBER, "4"),
				token.New(token.RPAREN, ")"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "e"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "f"),
				token.New(token.ASTERISK, "*"),
				token.New(token.LPAREN, "("),
				token.New(token.LPAREN, "("),
				token.New(token.IDENT, "g"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "3"),
				token.New(token.RPAREN, ")"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "h"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "h"),
				token.New(token.RPAREN, ")"),
				token.New(token.EOF, "EOF"),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			result := tokenstream.New(lexer).Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\nDiff at: %d\ngot: `%v`,\nexpected: `%v`",
					fn.DiffIdx(result, tt.expected),
					result,
					tt.expected,
				)
			}
		})
	}
}

func TestTokenStreamPreprocessFormula(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []token.Token
	}{
		"Formula no args": {
			input: "!formula",
			expected: []token.Token{
				token.New(token.BANG, "!"),
				token.New(token.IDENT, "formula"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Formula args": {
			input: "!formula xy",
			expected: []token.Token{
				token.New(token.BANG, "!"),
				token.New(token.IDENT, "formula"),
				token.New(token.IDENT, "x"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "y"),
				token.New(token.EOF, "EOF"),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			result := tokenstream.New(lexer).Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\nDiff at: %d\ngot: `%v`,\nexpected: `%v`",
					fn.DiffIdx(result, tt.expected),
					result,
					tt.expected,
				)
			}
		})
	}
}
