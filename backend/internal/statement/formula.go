package statement

import (
	"bytes"
	"strings"

	"app/internal/expression"
	fn "app/internal/functional"
	"app/internal/token"
)

type Formula struct {
	name   token.Token
	params []expression.Expression
}

func NewFormula(name token.Token, params []expression.Expression) *Formula {
	return &Formula{
		name:   name,
		params: params,
	}
}

func (formula *Formula) ToString() string {
	exprStrings := fn.Map(formula.params, exprToString)
	exprJoins := strings.Join(exprStrings, ", ")

	var buffer bytes.Buffer
	buffer.WriteString(formula.name.Literal)
	buffer.WriteString(" ")
	buffer.WriteString(exprJoins)
	return buffer.String()
}

func exprToString(expr expression.Expression) string {
	return expr.PrettyString()
}
