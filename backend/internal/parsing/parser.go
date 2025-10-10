package parser

import (
	"fmt"
	"strconv"

	"app/internal/ast"
	"app/internal/expression"
	"app/internal/statement"
	"app/internal/token"
	"app/internal/tokenstream"
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
	prefixExprFn          = func() (expression.Expression, *ParseErr)
	infixExprFn           = func(expression.Expression) (expression.Expression, *ParseErr)
	prefixAtomTransformFn = func() (statement.Statement, *ParseErr)
)

type Parser struct {
	tokenStream *tokenstream.TokenStream
	current     token.Token
	peek        token.Token

	prefixExprFns          map[token.TokenType]prefixExprFn
	infixExprFns           map[token.TokenType]infixExprFn
	prefixAtomTransformFns map[token.TokenType]prefixAtomTransformFn
}

func New(tokenStream *tokenstream.TokenStream) *Parser {
	newParser := Parser{
		tokenStream:            tokenStream,
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
		stmt, err := parser.parseStatement()
		if err != nil {
			errStmt := statement.NewLineError(err.Error(), err.Stack())
			program.AppendStatement(errStmt)
		} else {
			program.AppendStatement(stmt)
		}
		if parser.current.Type == token.NEW_LINE {
			parser.advanceToken()
		}
	}
	return program
}

func (parser *Parser) advanceToken() {
	parser.current = parser.peek
	parser.peek = parser.tokenStream.Next()
}

func (parser *Parser) parseStatement() (statement.Statement, *ParseErr) {
	switch parser.current.Type {
	case token.ILLEGAL:
		return nil, parser.parseIllegal()
	case token.SLASH:
		return parser.parseCommand()
	case token.BANG:
		return parser.parseFormula()
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

func (parser *Parser) parseIllegal() *ParseErr {
	msg := fmt.Sprintf("Illegal character: %s", parser.current.Literal)
	err := NewParseErr(msg)
	err.AddStack("parseIllegal")
	return err
}

func (parser *Parser) parseCommand() (statement.Statement, *ParseErr) {
	parser.advanceToken()
	var err *ParseErr
	var stmt statement.Statement
	switch parser.current.Type {
	case token.NEW_LINE, token.EOF:
		err = NewParseErr("Empty line")
	default:
		stmt, err = parser.parseAtomTransform()
	}

	if err != nil {
		err.AddStack("parseCommand")
	}
	parser.advanceToken()
	return stmt, err
}

func (parser *Parser) parseIdentifier() (expression.Expression, *ParseErr) {
	return expression.NewIdentifier(parser.current), nil
}

func (parser *Parser) parseNumber() (expression.Expression, *ParseErr) {
	num, err := strconv.ParseFloat(parser.current.Literal, 64)
	if err != nil {
		msg := fmt.Sprintf("Parsing number error for: %s", parser.current.Literal)
		perr := NewParseErr(msg)
		perr.AddStack("parseNumber", parser.current)
		return nil, perr
	}
	return expression.NewNumber(num), nil
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
