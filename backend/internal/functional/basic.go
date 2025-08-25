package functional

func Map[T, V any](ts []T, f func(T) V) []V {
	value := make([]V, len(ts))
	for i, t := range ts {
		value[i] = f(t)
	}
	return value
}
