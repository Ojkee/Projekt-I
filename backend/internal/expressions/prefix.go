package expression

import (
	"bytes"

	"app/internal/token"
)

type Prefix struct {
	operator token.Token
	expr     Expression
}

func NewPrefix(op token.Token, expr Expression) *Prefix {
	return &Prefix{
		operator: op,
		expr:     expr,
	}
}

func (prefix *Prefix) DebugString() string {
	exprString := prefix.expr.DebugString()

	var buffer bytes.Buffer
	buffer.WriteString("PREFIX(")
	buffer.WriteString(prefix.operator.Literal)
	buffer.WriteString(exprString)
	buffer.WriteString(")")
	return buffer.String()
}

func (prefix *Prefix) PrettyString() string {
	return prefix.operator.Literal + prefix.expr.PrettyString()
}
