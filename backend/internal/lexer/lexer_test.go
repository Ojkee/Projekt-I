package lexer_test

import (
	"reflect"
	"testing"

	lexer_api "app/internal/lexer"
	"app/internal/token"
)

func TestLexerInCategories(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []token.Token
	}{
		"Empty": {
			input: "",
			expected: []token.Token{
				token.New(token.EOF, "EOF"),
			},
		},
		"Empty whitespaces": {
			input: "    \r   \n       ",
			expected: []token.Token{
				token.New(token.NEW_LINE, "\\n"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Comperison operators": {
			input: "> < >= <=",
			expected: []token.Token{
				token.New(token.GT, ">"),
				token.New(token.LT, "<"),
				token.New(token.GE, ">="),
				token.New(token.LE, "<="),
				token.New(token.EOF, "EOF"),
			},
		},
		"Math operators": {
			input: "= + - / * ^ !=",
			expected: []token.Token{
				token.New(token.EQUALS, "="),
				token.New(token.PLUS, "+"),
				token.New(token.MINUS, "-"),
				token.New(token.SLASH, "/"),
				token.New(token.ASTERISK, "*"),
				token.New(token.CARET, "^"),
				token.New(token.NOT_EQUALS, "!="),
				token.New(token.EOF, "EOF"),
			},
		},
		"Parentheses and separators": {
			input: "( ) ,",
			expected: []token.Token{
				token.New(token.LPAREN, "("),
				token.New(token.RPAREN, ")"),
				token.New(token.COMMA, ","),
				token.New(token.EOF, "EOF"),
			},
		},
		"Numbers": {
			input: "5 2 22 103 1.4 100.1 0.0003",
			expected: []token.Token{
				token.New(token.NUMBER, "5"),
				token.New(token.NUMBER, "2"),
				token.New(token.NUMBER, "22"),
				token.New(token.NUMBER, "103"),
				token.New(token.NUMBER, "1.4"),
				token.New(token.NUMBER, "100.1"),
				token.New(token.NUMBER, "0.0003"),
				token.New(token.EOF, "EOF"),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			result := lexer.Tokenize()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("got: `%v`, expected: `%v`", result, tt.expected)
			}
		})
	}
}

func TestLexerExamplePrograms(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []token.Token
	}{
		"Equation spreaded": {
			input: "2 * 3 = 6 * x",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.ASTERISK, "*"),
				token.New(token.NUMBER, "3"),
				token.New(token.EQUALS, "="),
				token.New(token.NUMBER, "6"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Equation shrinked": {
			input: "2*3=6*x",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.ASTERISK, "*"),
				token.New(token.NUMBER, "3"),
				token.New(token.EQUALS, "="),
				token.New(token.NUMBER, "6"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Equation spreaded #2": {
			input: "2 - 3 = 6 * x + 9",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.MINUS, "-"),
				token.New(token.NUMBER, "3"),
				token.New(token.EQUALS, "="),
				token.New(token.NUMBER, "6"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "9"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Equation shrinked #2": {
			input: "2-3=6*x+9",
			expected: []token.Token{
				token.New(token.NUMBER, "2"),
				token.New(token.MINUS, "-"),
				token.New(token.NUMBER, "3"),
				token.New(token.EQUALS, "="),
				token.New(token.NUMBER, "6"),
				token.New(token.ASTERISK, "*"),
				token.New(token.IDENT, "x"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "9"),
				token.New(token.EOF, "EOF"),
			},
		},
		"Command no params": {
			input: "/+23",
			expected: []token.Token{
				token.New(token.SLASH, "/"),
				token.New(token.PLUS, "+"),
				token.New(token.NUMBER, "23"),
				token.New(token.EOF, "EOF"),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			result := lexer.Tokenize()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("\ngot: `%v`,\nexpected: `%v`", result, tt.expected)
			}
		})
	}
}

func TestLexerPreprocess(t *testing.T) {
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
				token.New(token.NUMBER, "y"),
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
				token.New(token.LPAREN, ")"),
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
			result := lexer.Tokenize()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("\ngot: `%v`,\nexpected: `%v`", result, tt.expected)
			}
		})
	}
}
