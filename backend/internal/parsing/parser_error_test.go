package parser_test

import (
	"reflect"
	"testing"

	lexer_api "app/internal/lexer"
	parser_api "app/internal/parser"
	"app/internal/statement"
	"app/internal/tokenstream"
)

func TestParserErrorsSingleLineAtomic(t *testing.T) {
	tests := map[string]struct {
		input    string
		expected []statement.Statement
	}{
		"Missing number after plus": {
			input:    "/+",
			expected: []statement.Statement{},
		},
		"Missing number after minus": {
			input:    "/-",
			expected: []statement.Statement{},
		},
		"Missing number after asterisk": {
			input:    "/*",
			expected: []statement.Statement{},
		},
		"Missing number after slash": {
			input:    "/",
			expected: []statement.Statement{},
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
