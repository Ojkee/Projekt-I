package parser

import (
	"app/internal/expression"
	"app/internal/token"
)

func (parser *Parser) parseExpression(precedence int) (expression.Expression, *ParseErr) {
	prefix := parser.prefixExprFns[parser.current.Type]
	if prefix == nil {
		err := NewParseErr("Error near: `" + parser.current.Literal + "`")
		err.AddStack("parseExpression nil prefix", parser.current)
		return nil, err
	}
	var err *ParseErr
	lhs, err := prefix()
	if err != nil {
		err.AddStack("parseExpression", parser.current)
		return nil, err
	}

	for !newLineOrEOF(parser.peek) && precedence < parser.peekPrecedence() {
		infix := parser.infixExprFns[parser.peek.Type]
		if infix == nil {
			return lhs, nil
		}
		parser.advanceToken()
		lhs, err = infix(lhs)
		if err != nil {
			err.AddStack("parseExpression")
			return nil, err
		}
	}

	return lhs, nil
}

func (parser *Parser) parsePrefixExpression() (expression.Expression, *ParseErr) {
	operator := parser.current
	parser.advanceToken()
	rhs, err := parser.parseExpression(PREFIX)
	if err != nil {
		err.AddStack("parsePrefixExpression", []any{parser.current})
		return nil, err
	}
	return expression.NewPrefix(operator, rhs), nil
}

func (parser *Parser) parseInfixExpression(
	lhs expression.Expression,
) (expression.Expression, *ParseErr) {
	operator := parser.current
	precedence := parser.currentPrecedence()
	parser.advanceToken()
	rhs, err := parser.parseExpression(precedence)
	if err != nil {
		err.AddStack("parseInfixExpression ", []any{parser.current})
		return nil, err
	}
	return expression.NewInfix(operator, lhs, rhs), nil
}

func (parser *Parser) parseGroupedExpression() (expression.Expression, *ParseErr) {
	parser.advanceToken()
	expr, err := parser.parseExpression(LOWEST)
	if err != nil {
		err.AddStack("parseGroupedExpression", []any{parser.current})
		return nil, err
	}
	if parser.peek.Type != token.RPAREN {
		err := NewParseErr("Parentheses should close, write: `)`")
		err.AddStack("parseGroupedExpression", parser.current)
		return nil, err
	}
	parser.advanceToken()
	return expr, nil
}
