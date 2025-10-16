# Main Objectives
- [ ] [Lexer](#lexer)
- [x] [Token Stream](#token-stream)
- [ ] [Parser](#parser)
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
- [ ] Test invalid:
    - [ ] Invalid characters

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
- [ ] Test invalid:
    - [ ] Invalid characters
    - [ ] Missing characters

## Evaluator
- [x] Translate Prefix/Infix into Math Nodes (Add, Mul, Pow...)
- [ ] Evaluate:
    - [ ] Subjects
        - [x] Equation
        - [x] Expression
        - [ ] ???
    - [x] Atom transformations
    - [ ] Formulas
- [ ] Test:
    - [x] Translation
    - [x] Evaluation:
        - [ ] Subjects
            - [x] Equation
            - [x] Expression
            - [ ] ???
    - [x] Atom transformations
    - [ ] Formulas
- [ ] Test invalid:
    - [x] Empty input
    - [ ] ???


## Extras
- [x] Replace all 'ToString's with string builders
- [x] Better __repl__ implementation of statments and expressions (more readable)
- [ ] In case of complexity of multiple params in Formulas, It might be necessary to limit Formulas to 1 parameter at most
