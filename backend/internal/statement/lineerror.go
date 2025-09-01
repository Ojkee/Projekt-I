package statement

import (
	"bytes"
	"fmt"
	"strings"

	"app/internal/functional"
)

type LineError struct {
	msg   string
	stack []string
}

func NewLineError(msg string, stack []string) *LineError {
	return &LineError{
		msg:   msg,
		stack: stack,
	}
}

func (lineError *LineError) ToString() string {
	var buffer bytes.Buffer
	buffer.WriteString("error: `")
	buffer.WriteString(lineError.msg)
	buffer.WriteString("`")
	return buffer.String()
}

func (lineError *LineError) StackString() string {
	fillToRight := func(line string) string {
		return fmt.Sprintf("|%40s   |", line)
	}
	framesToRight := functional.Map(lineError.stack, fillToRight)
	return strings.Join(framesToRight, "\n")
}
