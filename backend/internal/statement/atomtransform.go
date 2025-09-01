package statement

import (
	"bytes"

	"app/internal/expression"
	"app/internal/token"
)

type AtomTransform struct {
	operator token.Token
	expr     expression.Expression
}

func NewAtomTransform(op token.Token, expr expression.Expression) *AtomTransform {
	return &AtomTransform{
		operator: op,
		expr:     expr,
	}
}

func (atom *AtomTransform) ToString() string {
	var buffer bytes.Buffer
	buffer.WriteString(atom.operator.Literal)
	buffer.WriteString(atom.expr.PrettyString())
	return buffer.String()
}
