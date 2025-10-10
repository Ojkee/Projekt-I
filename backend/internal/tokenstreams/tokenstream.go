package tokenstream

import (
	lexer_api "app/internal/lexer"
	"app/internal/token"
)

type TokenStream struct {
	readIdx int
	tokens  []token.Token

	mulMap map[token.TokenType]map[token.TokenType]struct{}
}

func New(lexer *lexer_api.Lexer) *TokenStream {
	stream := TokenStream{
		readIdx: 0,
		tokens:  lexer.Tokenize(),
		mulMap:  make(map[token.TokenType]map[token.TokenType]struct{}),
	}

	stream.mulMap[token.IDENT] = typeSet(token.NUMBER, token.LPAREN)
	stream.mulMap[token.NUMBER] = typeSet(token.IDENT, token.LPAREN)
	stream.mulMap[token.RPAREN] = typeSet(token.IDENT, token.NUMBER, token.LPAREN)

	stream.preprocess()
	return &stream
}

func (tokenStream *TokenStream) Get() []token.Token {
	return tokenStream.tokens
}

func (tokenStream *TokenStream) Next() token.Token {
	tok := tokenStream.tokens[tokenStream.readIdx]
	if tok.Type != token.EOF {
		tokenStream.readIdx++
	}
	return tok
}

func (tokenStream *TokenStream) preprocess() {
	value := make([]token.Token, 0)

	for i := 0; i < len(tokenStream.tokens)-1; i++ {
		current := tokenStream.tokens[i]
		next := tokenStream.tokens[i+1]
		if current.Type == token.BANG {
			i++
			value = append(value, current)
			value = append(value, next)
			continue
		}
		if current.Type == token.IDENT && len(current.Literal) > 1 {
			idents := mulSplit(current.Literal)
			value = append(value, idents...)
		} else {
			value = append(value, current)
		}
		if tokenStream.mulBetween(current.Type, next.Type) {
			value = append(value, token.New(token.ASTERISK, "*"))
		}
	}
	last := tokenStream.tokens[len(tokenStream.tokens)-1]
	value = append(value, last)
	tokenStream.tokens = value
}

func (tokenStream *TokenStream) mulBetween(lhs, rhs token.TokenType) bool {
	if possible, ok := tokenStream.mulMap[lhs]; ok {
		_, containts := possible[rhs]
		return containts
	}
	return false
}

func typeSet(types ...token.TokenType) map[token.TokenType]struct{} {
	value := make(map[token.TokenType]struct{}, 0)
	for _, tokType := range types {
		value[tokType] = struct{}{}
	}
	return value
}

func mulSplit(ident string) []token.Token {
	value := make([]token.Token, 0)

	syms := []rune(ident)
	for i, sym := range syms {
		tok := token.New(token.IDENT, string(sym))
		value = append(value, tok)
		if i < len(syms)-1 {
			value = append(value, token.New(token.ASTERISK, "*"))
		}
	}
	return value
}
