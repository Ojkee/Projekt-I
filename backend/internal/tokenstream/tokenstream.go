package tokenstream

import (
	lexer_api "app/internal/lexer"
	"app/internal/token"
)

type TokenStream struct {
	readIdx int
	tokens  []token.Token
}

func New(lexer *lexer_api.Lexer) *TokenStream {
	stream := TokenStream{
		readIdx: 0,
		tokens:  lexer.Tokenize(),
	}
	stream.preprocess()
	return &stream
}

func (tokenStream *TokenStream) Next() token.Token {
	tok := tokenStream.tokens[tokenStream.readIdx]
	if tok.Type != token.EOF {
		tokenStream.readIdx++
	}
	return tok
}

func (tokenStream *TokenStream) preprocess() {
	preprocessed := make([]token.Token, 0)
	for _, tok := range tokenStream.tokens { // TODO-BACK: insert preprocess mechanism here
		preprocessed = append(preprocessed, tok)
	}
	tokenStream.tokens = preprocessed
}
