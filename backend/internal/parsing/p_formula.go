package parser

import (
	"app/internal/expression"
	"app/internal/statement"
	"app/internal/token"
)

func (parser *Parser) parseFormula() (statement.Statement, *ParseErr) {
	parser.advanceToken()
	ident := parser.current
	parser.advanceToken()
	params, err := parser.parseCommaSepParams()
	if err != nil {
		err.AddStack("parseFormula")
		return nil, err
	}
	return statement.NewFormula(ident, params), nil
}

func (parser *Parser) parseCommaSepParams() ([]expression.Expression, *ParseErr) {
	params := make([]expression.Expression, 0)
	for !newLineOrEOF(parser.current) {
		expr, err := parser.parseExpression(LOWEST)
		if err != nil {
			err.AddStack("parseCommaSepParams", parser.current)
			return nil, err
		}
		params = append(params, expr)
		parser.advanceToken()                   // For some reason expr stops at last exprs token
		if parser.current.Type == token.COMMA { // TODO-BACK: error handling
			parser.advanceToken()
		}
	}
	return params, nil
}
