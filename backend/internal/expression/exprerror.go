package expression

import "bytes"

type ExprError struct {
	msg string
}

func NewExprError(msg string) *ExprError {
	return &ExprError{
		msg: msg,
	}
}

func (exprError *ExprError) DebugString() string {
	var buffer bytes.Buffer
	buffer.WriteString("ERROR: `")
	buffer.WriteString(exprError.msg)
	buffer.WriteString("`")
	return buffer.String()
}

func (exprError *ExprError) PrettyString() string {
	return exprError.msg
}
