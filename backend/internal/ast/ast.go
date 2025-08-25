package ast

import "app/internal/statement"

type Program struct {
	statements []statement.Statement
}

func NewProgram() *Program {
	return &Program{
		statements: make([]statement.Statement, 0),
	}
}

func (program *Program) AppendStatement(stmt statement.Statement) {
	program.statements = append(program.statements, stmt)
}

func (program *Program) Get() *[]statement.Statement {
	return &program.statements
}
