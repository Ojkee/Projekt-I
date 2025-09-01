package parser

import "app/internal/statement"

func (parser *Parser) parseSubject() (*statement.Subject, *ParseErr) {
	expr, err := parser.parseExpression(LOWEST)
	if err != nil {
		err.AddStack("parseSubject")
		return nil, err
	}
	if newLineOrEOF(parser.peek) {
		parser.advanceToken()
	}
	return statement.NewSubject(expr), nil
}
