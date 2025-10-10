package parser

import (
	"app/internal/statement"
	"app/internal/token"
)

func (parser *Parser) parseAtomTransform() (statement.Statement, *ParseErr) {
	prefix := parser.prefixAtomTransformFns[parser.current.Type]
	if prefix == nil {
		err := NewParseErr("Error near: `" + parser.current.Literal + "`")
		err.AddStack("parseAtomTransform", parser.current)
		return nil, err
	}
	expr, err := prefix()
	if err != nil {
		err.AddStack("parseAtomTransform")
		return nil, err
	}
	return expr, nil
}

func (parser *Parser) prefixAtom() (statement.Statement, *ParseErr) {
	op := parser.current
	parser.advanceToken()
	expr, err := parser.parseExpression(LOWEST)
	if err != nil {
		err.AddStack("prefixAtom", parser.current)
		return nil, err
	}
	return statement.NewAtomTransform(op, expr), nil
}

func (parser *Parser) prefixAtomDiv() (statement.Statement, *ParseErr) {
	op := token.New(token.SLASH, "/")
	expr, err := parser.parseExpression(LOWEST)
	if err != nil {
		err.AddStack("prefixAtomDiv", parser.current)
	}
	return statement.NewAtomTransform(op, expr), nil
}
