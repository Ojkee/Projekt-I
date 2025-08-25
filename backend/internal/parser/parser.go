package parser

import (
	"fmt"
	"strconv"

	"app/internal/ast"
	"app/internal/expression"
	lexer_api "app/internal/lexer"
	"app/internal/statement"
	"app/internal/token"
)

const (
	_ int = iota
	LOWEST
	EQUALS
	PLUSMINUS
	MULDIV
	PREFIX
	POWER
	FUNCTION
)

var precedences = map[token.TokenType]int{
	token.EQUALS:   EQUALS,
	token.LT:       EQUALS,
	token.GT:       EQUALS,
	token.PLUS:     PLUSMINUS,
	token.MINUS:    PLUSMINUS,
	token.ASTERISK: MULDIV,
	token.SLASH:    MULDIV,
	token.CARET:    POWER,
}

type (
	prefixExprFn          = func() expression.Expression
	infixExprFn           = func(expression.Expression) expression.Expression
	prefixAtomTransformFn = func() statement.Statement
)

type Parser struct {
	lexer   *lexer_api.Lexer
	current token.Token
	peek    token.Token

	prefixExprFns          map[token.TokenType]prefixExprFn
	infixExprFns           map[token.TokenType]infixExprFn
	prefixAtomTransformFns map[token.TokenType]prefixAtomTransformFn
}

func New(lexer *lexer_api.Lexer) *Parser {
	newParser := Parser{
		lexer:                  lexer,
		prefixExprFns:          make(map[token.TokenType]prefixExprFn),
		infixExprFns:           make(map[token.TokenType]infixExprFn),
		prefixAtomTransformFns: make(map[token.TokenType]prefixAtomTransformFn),
	}
	// Setting current and peek
	newParser.advanceToken()
	newParser.advanceToken()

	// Prefixes Expressions
	newParser.prefixExprFns[token.IDENT] = newParser.parseIdentifier
	newParser.prefixExprFns[token.NUMBER] = newParser.parseNumber
	newParser.prefixExprFns[token.MINUS] = newParser.parsePrefixExpression
	newParser.prefixExprFns[token.LPAREN] = newParser.parseGroupedExpression

	// Infixes Expressions
	newParser.infixExprFns[token.EQUALS] = newParser.parseInfixExpression
	newParser.infixExprFns[token.LT] = newParser.parseInfixExpression
	newParser.infixExprFns[token.GT] = newParser.parseInfixExpression
	newParser.infixExprFns[token.PLUS] = newParser.parseInfixExpression
	newParser.infixExprFns[token.MINUS] = newParser.parseInfixExpression
	newParser.infixExprFns[token.ASTERISK] = newParser.parseInfixExpression
	newParser.infixExprFns[token.SLASH] = newParser.parseInfixExpression
	newParser.infixExprFns[token.CARET] = newParser.parseInfixExpression

	// Prefix Atom Transform
	newParser.prefixAtomTransformFns[token.NUMBER] = newParser.prefixAtomDiv
	newParser.prefixAtomTransformFns[token.IDENT] = newParser.prefixAtomDiv
	newParser.prefixAtomTransformFns[token.PLUS] = newParser.prefixAtom
	newParser.prefixAtomTransformFns[token.MINUS] = newParser.prefixAtom
	newParser.prefixAtomTransformFns[token.ASTERISK] = newParser.prefixAtom
	newParser.prefixAtomTransformFns[token.CARET] = newParser.prefixAtom
	return &newParser
}

func (parser *Parser) Parse() *ast.Program {
	program := ast.NewProgram()
	for parser.current.Type != token.EOF {
		stmt := parser.parseStatement()
		if stmt != nil {
			program.AppendStatement(stmt)
		}
		parser.advanceToken()
	}
	return program
}

func (parser *Parser) advanceToken() {
	parser.current = parser.peek
	parser.peek = parser.lexer.ReadToken()
}

func (parser *Parser) parseStatement() statement.Statement {
	switch parser.current.Type {
	case token.ILLEGAL:
		return parser.parseIllegal()
	case token.SLASH:
		return parser.parseCommand()
	default:
		return parser.parseSubject()
	}
}

func (parser *Parser) skipOverNewLine() {
	for !newLineOrEOF(parser.current) {
		parser.advanceToken()
	}
	if parser.current.Type == token.NEW_LINE {
		parser.advanceToken()
	}
}

func (parser *Parser) parseIllegal() *statement.LineError {
	msg := fmt.Sprintf("Illegal character: %s", parser.current.Literal)
	invalid := statement.NewLineError(msg)
	parser.skipOverNewLine()
	return invalid
}

func (parser *Parser) parseCommand() statement.Statement {
	parser.advanceToken()
	var stmt statement.Statement
	switch parser.current.Type {
	case token.NEW_LINE, token.EOF:
		stmt = statement.NewLineError("Empty line")
	case token.IDENT:
		if parser.current.IsSymbol() {
			stmt = parser.parseAtomTransform()
		} else {
			stmt = parser.parseFormula()
		}
	default:
		stmt = parser.parseAtomTransform()
	}

	parser.skipOverNewLine()
	return stmt
}

func (parser *Parser) parseAtomTransform() statement.Statement {
	prefix := parser.prefixAtomTransformFns[parser.current.Type]
	if prefix == nil {
		return statement.NewLineError("Error near: `" + parser.current.Literal + "`")
	}
	return prefix()
}

func (parser *Parser) prefixAtom() statement.Statement {
	op := parser.current
	parser.advanceToken()
	expr := parser.parseExpression(LOWEST)
	return statement.NewAtomTransform(op, expr)
}

func (parser *Parser) prefixAtomDiv() statement.Statement {
	op := token.New(token.SLASH, "/")
	expr := parser.parseExpression(LOWEST)
	return statement.NewAtomTransform(op, expr)
}

func (parser *Parser) parseFormula() statement.Statement {
	ident := parser.current
	parser.advanceToken()
	params := parser.parseCommaSepParams()
	return statement.NewFormula(ident, params)
}

func (parser *Parser) parseCommaSepParams() []expression.Expression {
	params := make([]expression.Expression, 0)
	for !newLineOrEOF(parser.current) {
		expr := parser.parseExpression(LOWEST)
		params = append(params, expr)
		parser.advanceToken() // For some reason expr stops at last exprs token
		if parser.current.Type == token.COMMA {
			parser.advanceToken()
		}
	}
	return params
}

func (parser *Parser) parseSubject() *statement.Subject {
	expr := parser.parseExpression(LOWEST)
	if newLineOrEOF(parser.peek) {
		parser.advanceToken()
	}
	return statement.NewSubject(expr)
}

func (parser *Parser) parseExpression(precedence int) expression.Expression {
	prefix := parser.prefixExprFns[parser.current.Type]
	if prefix == nil {
		msg := "Error near: `" + parser.current.Literal + "`"
		parser.skipOverNewLine()
		return expression.NewExprError(msg)
	}
	lhs := prefix()

	for !newLineOrEOF(parser.peek) && precedence < parser.peekPrecedence() {
		infix := parser.infixExprFns[parser.peek.Type]
		if infix == nil {
			return lhs
		}
		parser.advanceToken()
		lhs = infix(lhs)
	}

	return lhs
}

func (parser *Parser) parsePrefixExpression() expression.Expression {
	operator := parser.current
	parser.advanceToken()
	rhs := parser.parseExpression(PREFIX)
	return expression.NewPrefix(operator, rhs)
}

func (parser *Parser) parseInfixExpression(lhs expression.Expression) expression.Expression {
	operator := parser.current
	precedence := parser.currentPrecedence()
	parser.advanceToken()
	rhs := parser.parseExpression(precedence)
	return expression.NewInfix(operator, lhs, rhs)
}

func (parser *Parser) parseGroupedExpression() expression.Expression {
	parser.advanceToken()
	expr := parser.parseExpression(LOWEST)
	if parser.peek.Type != token.RPAREN {
		return nil
	}
	parser.advanceToken()
	return expr
}

func (parser *Parser) parseIdentifier() expression.Expression {
	return expression.NewIdentifier(parser.current)
}

func (parser *Parser) parseNumber() expression.Expression {
	num, err := strconv.ParseFloat(parser.current.Literal, 64)
	if err != nil {
		panic(err)
	}
	return expression.NewNumber(num)
}

func (parser *Parser) peekPrecedence() int {
	return getPrecedence(parser.peek.Type)
}

func (parser *Parser) currentPrecedence() int {
	return getPrecedence(parser.current.Type)
}

func getPrecedence(tokenType token.TokenType) int {
	if prec, ok := precedences[tokenType]; ok {
		return prec
	}
	return LOWEST
}

func newLineOrEOF(t token.Token) bool {
	return t.Type == token.NEW_LINE || t.Type == token.EOF
}
