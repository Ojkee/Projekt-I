package expression

import (
	"bytes"
	"math"
	"strconv"
	"strings"
)

type Number struct {
	value float64
}

func NewNumber(value float64) *Number {
	return &Number{
		value: value,
	}
}

func (number *Number) numToString() string {
	if math.Trunc(number.value) == number.value {
		return strconv.Itoa(int(number.value))
	}

	maxPrec := 3
	valueStr := strconv.FormatFloat(float64(number.value), 'f', maxPrec, 64)
	valueStr = strings.TrimRightFunc(valueStr, func(r rune) bool { return r == '0' })
	return valueStr
}

func (number *Number) DebugString() string {
	var buffer bytes.Buffer
	buffer.WriteString("NUBER(")
	buffer.WriteString(number.numToString())
	buffer.WriteString(")")
	return buffer.String()
}

func (number *Number) PrettyString() string {
	return number.numToString()
}
