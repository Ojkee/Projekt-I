package statement

import "app/internal/expression"

type Subject struct {
	expr expression.Expression
}

func NewSubject(expr expression.Expression) *Subject {
	return &Subject{
		expr: expr,
	}
}

func (subject *Subject) ToString() string {
	return subject.expr.PrettyString()
}
