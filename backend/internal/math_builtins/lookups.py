from typing import Optional
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Node, Mul, Pow, Add
from backend.internal.math_builtins.formulas import FORMULA_MAP


class BuiltIns:
    @staticmethod
    def is_present(name: str) -> bool:
        return name in FORMULA_MAP

    @staticmethod
    def get(name: str, root: Node, param: Optional[Node]) -> Optional[Node]:
        if not param:
            raise NotImplementedError("Auto search param not implemented yet")

        entry = FORMULA_MAP.get(name)
        assert entry, f"{name}, not present in builtins, use `BuiltIns.is_present`"

        to_replace = BuiltIns._find_match(root, param)
        if not to_replace:
            return None

        cache = BuiltIns._bind_wildnodes(to_replace, entry.to_match)
        return BuiltIns._build_node(entry.replacement, cache)

    @staticmethod
    def _find_match(node: Node, param: Node) -> Optional[Node]:
        """
        Finds an exact subtree match of `param` within `node`.

        Returns:
            Node | None: the original node reference if found, or None otherwise.
        """
        if node == param:
            return node

        def dfs(lhs: Node, rhs: Node) -> Optional[Node]:
            node = BuiltIns._find_match(lhs, param)
            return node if node else BuiltIns._find_match(rhs, param)

        match node:
            case Add(left=a, right=b) | Mul(left=a, right=b) | Pow(base=a, exponent=b):
                return dfs(a, b)

        return None

    @staticmethod
    def _bind_wildnodes(node: Node, to_match: Node) -> dict[str, Node]:
        """
        Recursively binds each WildNode in `to_match` to the corresponding node in `node`.
        Fills cache with {tag: Node} pair.

        Asserts that `node` matches structurally with `to_match`.
        """
        cache: dict[str, Node] = {}

        def aux(node_, to_match_):
            match node_, to_match_:
                case Pow() as lhs, Pow() as rhs:
                    aux(lhs.base, rhs.base)
                    aux(lhs.exponent, rhs.exponent)

                case (Add() as lhs, Add() as rhs) | (Mul() as lhs, Mul() as rhs):
                    aux(lhs.left, rhs.left)
                    aux(lhs.right, rhs.right)

                case lhs, WildNode(tag=tag):
                    cache[tag] = lhs

        aux(node, to_match)
        return cache

    @staticmethod
    def _build_node(node: Node, cache: dict[str, Node]) -> Node:
        """
        Build a new node tree by replacing WildNodes using the provided cache.

        Each WildNode in the original tree is substituted with the corresponding node
        from the cache, preserving references to the original nodes from the user's input expression.

        Returns:
            Node: The reconstructed node tree with all WildNodes replaced.
        """
        if isinstance(node, WildNode):
            return cache[node.tag]

        match node:
            case Add(left=left, right=right):
                return Add(
                    BuiltIns._build_node(left, cache),
                    BuiltIns._build_node(right, cache),
                )
            case Mul(left=left, right=right):
                return Mul(
                    BuiltIns._build_node(left, cache),
                    BuiltIns._build_node(right, cache),
                )
            case Pow(base=base, exponent=exponent):
                return Pow(
                    BuiltIns._build_node(base, cache),
                    BuiltIns._build_node(exponent, cache),
                )

        return node
