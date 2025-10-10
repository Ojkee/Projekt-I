package expression

type Expression interface {
	DebugString() string
	PrettyString() string
}
