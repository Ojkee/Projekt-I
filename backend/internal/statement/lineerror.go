package statement

import "bytes"

type LineError struct {
	msg string
}

func NewLineError(msg string) *LineError {
	return &LineError{
		msg: msg,
	}
}

func (lineError *LineError) ToString() string {
	var buffer bytes.Buffer
	buffer.WriteString("error: `")
	buffer.WriteString(lineError.msg)
	buffer.WriteString("`")
	return buffer.String()
}
