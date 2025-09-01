package expression_test

import (
	"testing"

	"app/internal/expression"
)

func TestNumberString(t *testing.T) {
	tests := map[string]struct {
		input    float64
		expected string
	}{
		"Int": {
			input:    1.,
			expected: "1",
		},
		"Long float": {
			input:    0.293147928374,
			expected: "0.293",
		},
		"Long float round": {
			input:    0.293847928374,
			expected: "0.294",
		},
		"Short float": {
			input:    2.342,
			expected: "2.342",
		},
		"Long float leading numbers": {
			input:    23984793284.29413472,
			expected: "23984793284.294",
		},
		"Long float leading numbers round": {
			input:    23984793284.29483472,
			expected: "23984793284.295",
		},
		"Short float leading numbers": {
			input:    23984793284.294,
			expected: "23984793284.294",
		},
		"Remove 1 zero": {
			input:    3.9200000,
			expected: "3.92",
		},
		"Remove 2 zeros": {
			input:    3.900000,
			expected: "3.9",
		},
		"Remove all zeros and dot": {
			input:    3.00000,
			expected: "3",
		},
		"Shouldn't remove": {
			input:    4.002,
			expected: "4.002",
		},
		"Should remove only last": {
			input:    4.0200000,
			expected: "4.02",
		},
	}

	for name, test := range tests {
		tt := test
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			result := expression.NewNumber(tt.input).PrettyString()
			if result != tt.expected {
				t.Errorf("got: `%v`, expected: `%v`", result, tt.expected)
			}
		})
	}
}
