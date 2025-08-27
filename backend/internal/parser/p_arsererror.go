package parser

import (
	"fmt"
	"strings"

	fn "app/internal/functional"
)

type stackFrame struct {
	name string
	args []any
}

func (sf *stackFrame) toString() string {
	argStrs := fn.Map(sf.args, func(arg any) string {
		return fmt.Sprintf("%v", arg)
	})
	argStr := strings.Join(argStrs, ", ")
	return fmt.Sprintf("%s(%s)", sf.name, argStr)
}

type ParseErr struct {
	msg   string
	stack []stackFrame
}

func NewParseErr(msg string) *ParseErr {
	return &ParseErr{
		msg:   msg,
		stack: make([]stackFrame, 0),
	}
}

func (parseErr *ParseErr) Error() string {
	return parseErr.msg
}

func (parseErr *ParseErr) AddStack(frame string, args ...any) {
	parseErr.stack = append(parseErr.stack, stackFrame{name: frame, args: args})
}

func (parseErr *ParseErr) Stack() []string {
	toStr := func(frame stackFrame) string {
		return frame.toString()
	}
	return fn.Map(parseErr.stack, toStr)
}
