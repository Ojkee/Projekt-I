package functional

import "reflect"

func Map[T, V any](ts []T, f func(T) V) []V {
	value := make([]V, len(ts))
	for i, t := range ts {
		value[i] = f(t)
	}
	return value
}

func DiffIdx[T any](lhs, rhs []T) int {
	if len(lhs) < len(rhs) {
		return len(lhs)
	} else if len(rhs) < len(lhs) {
		return len(rhs)
	}
	for i := range lhs {
		if !reflect.DeepEqual(lhs[i], rhs[i]) {
			return i
		}
	}
	return -1
}
