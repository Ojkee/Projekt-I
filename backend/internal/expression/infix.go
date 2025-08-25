package expression

import (
	"bytes"

	"app/internal/token"
)

type Infix struct {
	operator token.Token
	lhs      Expression
	rhs      Expression
}

func NewInfix(op token.Token, lhs, rhs Expression) *Infix {
	return &Infix{
		operator: op,
		lhs:      lhs,
		rhs:      rhs,
	}
}

func (infix *Infix) DebugString() string {
	lhsString := infix.lhs.DebugString()
	rhsString := infix.rhs.DebugString()

	var buffer bytes.Buffer
	buffer.WriteString("INFIX(")
	buffer.WriteString(lhsString)
	buffer.WriteString(infix.operator.Literal)
	buffer.WriteString(rhsString)
	buffer.WriteString(")")
	return buffer.String()
}

func (infix *Infix) PrettyString() string {
	lhsString := infix.lhs.PrettyString()
	rhsString := infix.rhs.PrettyString()

	var buffer bytes.Buffer
	buffer.WriteString("(")
	buffer.WriteString(lhsString)
	buffer.WriteString(infix.operator.Literal)
	buffer.WriteString(rhsString)
	buffer.WriteString(")")
	return buffer.String()
}
