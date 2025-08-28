package parser_test

import (
	"fmt"
	"reflect"
	"strings"
	"testing"

	"app/internal/expression"
	fn "app/internal/functional"
	lexer_api "app/internal/lexer"
	parser_api "app/internal/parser"
	"app/internal/statement"
	"app/internal/token"
	"app/internal/tokenstream"
)

func stmtsToString(stmts []statement.Statement) string {
	stmtToString := func(stmt statement.Statement) string {
		switch s := stmt.(type) {
		case *statement.LineError:
			return fmt.Sprintf("- %s\n%s", s.ToString(), s.StackString())
		}
		return "- " + stmt.ToString()
	}
	strs := fn.Map(stmts, stmtToString)
	return strings.Join(strs, "\n")
}

func TestParserAlgebraic(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{
		"Simple epxr": {
			input: "x = 3",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewIdentifier(token.New(token.IDENT, "x")),
						expression.NewNumber(3.),
					),
				),
			},
		},
		"Infix mul epxr lhs": {
			input: "2*x = 3",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewInfix(
							token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewNumber(3.),
					),
				),
			},
		},
		"Infix mul epxr lhs x front": {
			input: "x*2 = 3",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewInfix(
							token.New(token.ASTERISK, "*"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewNumber(2.),
						),
						expression.NewNumber(3.),
					),
				),
			},
		},
		"Infix mul epxr rhs": {
			input: "2 = 3*x",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewNumber(2.),
						expression.NewInfix(
							token.New(token.ASTERISK, "*"),
							expression.NewNumber(3.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
					),
				),
			},
		},
		"Infix mul epxr rhs x front": {
			input: "2 = x*3",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewNumber(2.),
						expression.NewInfix(
							token.New(token.ASTERISK, "*"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewNumber(3.),
						),
					),
				),
			},
		},
		"Prefix lhs": {
			input: "-2 = x",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewPrefix(
							token.New(token.MINUS, "-"),
							expression.NewNumber(2.),
						),
						expression.NewIdentifier(token.New(token.IDENT, "x")),
					),
				),
			},
		},
		"Prefix rhs": {
			input: "2 = -x",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewNumber(2.),
						expression.NewPrefix(
							token.New(token.MINUS, "-"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
					),
				),
			},
		},
		"Infix mixed precedence with floats": {
			input: "a = x*3 + y/2 - z^2.5 + 7.0",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewIdentifier(token.New(token.IDENT, "a")),
						expression.NewInfix(
							token.New(token.PLUS, "+"),
							expression.NewInfix(
								token.New(token.MINUS, "-"),
								expression.NewInfix(
									token.New(token.PLUS, "+"),
									expression.NewInfix(
										token.New(token.ASTERISK, "*"),
										expression.NewIdentifier(token.New(token.IDENT, "x")),
										expression.NewNumber(3.0),
									),
									expression.NewInfix(
										token.New(token.SLASH, "/"),
										expression.NewIdentifier(token.New(token.IDENT, "y")),
										expression.NewNumber(2.0),
									),
								),
								expression.NewInfix(
									token.New(token.CARET, "^"),
									expression.NewIdentifier(token.New(token.IDENT, "z")),
									expression.NewNumber(2.5),
								),
							),
							expression.NewNumber(7.0),
						),
					),
				),
			},
		},
		"Redundant grouped": {
			input: "(x + y) = 2",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.PLUS, "+"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewIdentifier(token.New(token.IDENT, "y")),
						),
						expression.NewNumber(2.),
					),
				),
			},
		},
		"Basic grouped": {
			input: "2*(x + y) = 3",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewInfix(token.New(token.PLUS, "+"),
								expression.NewIdentifier(token.New(token.IDENT, "x")),
								expression.NewIdentifier(token.New(token.IDENT, "y")),
							),
						),
						expression.NewNumber(3.),
					),
				),
			},
		},
		"Basic grouped rhs": {
			input: "2 = 3*(x + 5)",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewNumber(2.),
						expression.NewInfix(
							token.New(token.ASTERISK, "*"),
							expression.NewNumber(3.),
							expression.NewInfix(
								token.New(token.PLUS, "+"),
								expression.NewIdentifier(token.New(token.IDENT, "x")),
								expression.NewNumber(5.),
							),
						),
					),
				),
			},
		},
		"Redundant Parens": {
			input: "(2) = x",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(
						token.New(token.EQUALS, "="),
						expression.NewNumber(2.),
						expression.NewIdentifier(token.New(token.IDENT, "x")),
					),
				),
			},
		},
		"Group with caret and mul": {
			input: "(2 + x) ^ 3 = (y - 4) * 5",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewInfix(token.New(token.PLUS, "+"),
								expression.NewNumber(2.),
								expression.NewIdentifier(token.New(token.IDENT, "x")),
							),
							expression.NewNumber(3.),
						),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewInfix(token.New(token.MINUS, "-"),
								expression.NewIdentifier(token.New(token.IDENT, "y")),
								expression.NewNumber(4.),
							),
							expression.NewNumber(5.),
						),
					),
				),
			},
		},
		"Nested grouping": {
			input: "2^(3*(4 + y))",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.CARET, "^"),
						expression.NewNumber(2.),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(3.),
							expression.NewInfix(token.New(token.PLUS, "+"),
								expression.NewNumber(4.),
								expression.NewIdentifier(token.New(token.IDENT, "y")),
							),
						),
					),
				),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			stream := tokenstream.New(lexer)
			parser := parser_api.New(stream)
			result := *parser.Parse().Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\ngot: \n\t`%s`, \nexpected: \n\t`%s`",
					stmtsToString(result),
					stmtsToString(tt.expected),
				)
			}
		})
	}
}

func TestParserCommand(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{
		"Atom plus": {
			input: "/+2",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.PLUS, "+"),
					expression.NewNumber(2.),
				),
			},
		},
		"Atom minus": {
			input: "/-2",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.MINUS, "-"),
					expression.NewNumber(2.),
				),
			},
		},
		"Atom div": {
			input: "/2",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.SLASH, "/"),
					expression.NewNumber(2.),
				),
			},
		},
		"Atom mul": {
			input: "/*2",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.ASTERISK, "*"),
					expression.NewNumber(2.),
				),
			},
		},
		"Atom power": {
			input: "/^2",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.CARET, "^"),
					expression.NewNumber(2.),
				),
			},
		},
		"Atom complex": {
			input: "/+(3*(x+y))",
			expected: []statement.Statement{
				statement.NewAtomTransform(
					token.New(token.PLUS, "+"),
					expression.NewInfix(token.New(token.ASTERISK, "*"),
						expression.NewNumber(3.),
						expression.NewInfix(token.New(token.PLUS, "+"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewIdentifier(token.New(token.IDENT, "y")),
						),
					),
				),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			stream := tokenstream.New(lexer)
			parser := parser_api.New(stream)
			result := *parser.Parse().Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\ngot: \n\t`%s`, \nexpected: \n\t`%s`",
					stmtsToString(result),
					stmtsToString(tt.expected),
				)
			}
		})
	}
}

func TestParserFormula(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{
		"Formula no args": {
			input: "!formula",
			expected: []statement.Statement{
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{},
				),
			},
		},
		"Formula single arg num": {
			input: "!formula 2",
			expected: []statement.Statement{
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewNumber(2.),
					},
				),
			},
		},
		"Formula single arg ident": {
			input: "!formula x",
			expected: []statement.Statement{
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewIdentifier(token.New(token.IDENT, "x")),
					},
				),
			},
		},
		"Formula multi arg": {
			input: "!formula 2, 1, x, a",
			expected: []statement.Statement{
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewNumber(2.),
						expression.NewNumber(1.),
						expression.NewIdentifier(token.New(token.IDENT, "x")),
						expression.NewIdentifier(token.New(token.IDENT, "a")),
					},
				),
			},
		},
		"Formula multi arg complex expression": {
			input: "!formula 2+x, i*(y - 8)",
			expected: []statement.Statement{
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewInfix(token.New(token.PLUS, "+"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewIdentifier(token.New(token.IDENT, "i")),
							expression.NewInfix(token.New(token.MINUS, "-"),
								expression.NewIdentifier(token.New(token.IDENT, "y")),
								expression.NewNumber(8.),
							),
						),
					},
				),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			stream := tokenstream.New(lexer)
			parser := parser_api.New(stream)
			result := *parser.Parse().Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\ngot: \n\t`%s`, \nexpected: \n\t`%s`",
					stmtsToString(result),
					stmtsToString(tt.expected),
				)
			}
		})
	}
}

func TestParserAlgebraicMultiline(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{
		"Empty": {
			input:    "",
			expected: []statement.Statement{},
		},
		"+ AtomTransform": {
			input: "2*x = 3^5\n/2",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewAtomTransform(token.New(token.SLASH, "/"),
					expression.NewNumber(2.),
				),
			},
		},
		"+ 2 AtomTransform": {
			input: "2*x = 3^5\n/*1\n/+6",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewAtomTransform(token.New(token.ASTERISK, "*"),
					expression.NewNumber(1.),
				),
				statement.NewAtomTransform(token.New(token.PLUS, "+"),
					expression.NewNumber(6.),
				),
			},
		},
		"+ 3 AtomTransform": {
			input: "2*x = 3^5\n/*1\n/+6\n/2",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewAtomTransform(token.New(token.ASTERISK, "*"),
					expression.NewNumber(1.),
				),
				statement.NewAtomTransform(token.New(token.PLUS, "+"),
					expression.NewNumber(6.),
				),
				statement.NewAtomTransform(token.New(token.SLASH, "/"),
					expression.NewNumber(2.),
				),
			},
		},
		"+ 3 Complex AtomTransform": {
			input: "2*x = 3^5\n  /*(x + 1)  \n  /+(6-y)^5.3  \n  /2*z  ",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewAtomTransform(token.New(token.ASTERISK, "*"),
					expression.NewInfix(token.New(token.PLUS, "+"),
						expression.NewIdentifier(token.New(token.IDENT, "x")),
						expression.NewNumber(1.),
					),
				),
				statement.NewAtomTransform(token.New(token.PLUS, "+"),
					expression.NewInfix(token.New(token.CARET, "^"),
						expression.NewInfix(token.New(token.MINUS, "-"),
							expression.NewNumber(6.),
							expression.NewIdentifier(token.New(token.IDENT, "y")),
						),
						expression.NewNumber(5.3),
					),
				),
				statement.NewAtomTransform(token.New(token.SLASH, "/"),
					expression.NewInfix(token.New(token.ASTERISK, "*"),
						expression.NewNumber(2.),
						expression.NewIdentifier(token.New(token.IDENT, "z")),
					),
				),
			},
		},
		"+ Formula no args": {
			input: "2*x = 3^5\n!formula",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{},
				),
			},
		},
		"+ Formula with args": {
			input: "2*x = 3^5\n!formula (x * 2)\n",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewNumber(2.),
						),
					},
				),
			},
		},
		"+ 3 Formula with and without args": {
			input: "2*x = 3^5\n!formula (x * 2)\n!formula\n!formula x^(3 + y), x + y",
			expected: []statement.Statement{
				statement.NewSubject(
					expression.NewInfix(token.New(token.EQUALS, "="),
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewNumber(2.),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
						),
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewNumber(3.),
							expression.NewNumber(5.),
						),
					),
				),
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewInfix(token.New(token.ASTERISK, "*"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewNumber(2.),
						),
					},
				),
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{},
				),
				statement.NewFormula(token.New(token.IDENT, "formula"),
					[]expression.Expression{
						expression.NewInfix(token.New(token.CARET, "^"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewInfix(token.New(token.PLUS, "+"),
								expression.NewNumber(3.),
								expression.NewIdentifier(token.New(token.IDENT, "y")),
							),
						),
						expression.NewInfix(token.New(token.PLUS, "+"),
							expression.NewIdentifier(token.New(token.IDENT, "x")),
							expression.NewIdentifier(token.New(token.IDENT, "y")),
						),
					},
				),
			},
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			stream := tokenstream.New(lexer)
			parser := parser_api.New(stream)
			result := *parser.Parse().Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\ngot:\n%s \nexpected: \n%s",
					stmtsToString(result),
					stmtsToString(tt.expected),
				)
			}
		})
	}
}

func TestParserErrors(t *testing.T) { // TODO-BACK implement better err handling in parser
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			lexer := lexer_api.New(tt.input)
			stream := tokenstream.New(lexer)
			parser := parser_api.New(stream)
			result := *parser.Parse().Get()
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf(
					"\ngot:\n%s \nexpected: \n%s",
					stmtsToString(result),
					stmtsToString(tt.expected),
				)
			}
		})
	}
}
