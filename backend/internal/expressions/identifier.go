package expression

import (
	"bytes"

	"app/internal/token"
)

type Identifier struct {
	name token.Token
}

func NewIdentifier(name token.Token) *Identifier {
	return &Identifier{
		name: name,
	}
}

func (ident *Identifier) DebugString() string {
	var buffer bytes.Buffer
	buffer.WriteString("IDENT(")
	buffer.WriteString(ident.name.Literal)
	buffer.WriteString(")")
	return buffer.String()
}

func (ident *Identifier) PrettyString() string {
	return ident.name.Literal
}
