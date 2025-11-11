# Main Objectives
- [x] [Lexer](#lexer)
- [x] [Token Stream](#token-stream)
- [x] [Parser](#parser)
- [ ] [Evaluator](#evaluator)
- [ ] [Extras](#extras)

## Lexer
- [x] Tokenize
    - [x] Operators
    - [x] Numbers
    - [x] Identifiers
    - [x] Parentheses
    - [x] New lines
- [x] Test:
    - [x] Operators
    - [x] Numbers
    - [x] Identifiers
    - [x] Parentheses
    - [x] New lines

## Token Stream
- [x] Preprocess:
    - [x] Multiplying identifiers
    - [x] Multiplying grouped

## Parser
- [x] Parse:
    - [x] Numbers
    - [x] Identifiers
    - [x] Prefix
    - [x] Infix
    - [x] Grouped expressions
    - [x] Atom transformations
    - [x] Formulas
- [x] Test:
    - [x] Numbers
    - [x] Identifiers
    - [x] Prefix
    - [x] Infix
    - [x] Grouped expressions
    - [x] Atom transformations
    - [x] Formulas
- [x] Test invalid:
    - [x] Invalid characters
    - [x] Missing characters

## Evaluator
- [x] Translate Prefix/Infix into Math Nodes (Add, Mul, Pow...)
- [x] Evaluate:
    - [x] Subjects
        - [x] Equation
        - [x] Expression
    - [x] Atom transformations
    - [x] Formulas
- [x] Test:
    - [x] Translation
    - [x] Evaluation:
        - [x] Subjects
            - [x] Equation
            - [x] Expression
    - [x] Atom transformations
    - [x] Formulas
- [ ] Test invalid:
    - [x] Empty input
    - [ ] First line errors
    - [ ] Errors deep lines
    - [ ] Invalid Atom Transformations
    - [ ] Invalid Formula Transformations


## Extras
- [x] Replace all 'ToString's with string builders
- [x] Better `__repl__` implementation of statements and expressions (more readable)
- [ ] In case of complexity of multiple parameters in Formulas, It might be necessary to limit Formulas to 1 parameter at most
- [ ] Use `Decimal` as Numeric value for better precision
