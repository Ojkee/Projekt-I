from typing import Optional
from backend.internal.math_builtins.builtins_error import (
    BuiltinsError,
    NotMatchingFormula,
    NotMatchingParam,
)
from backend.internal.math_builtins.formula_node import WildNode
from backend.internal.expression_tree import Node, Mul, Pow, Add, Numeric, Symbol
from backend.internal.math_builtins.formulas import FORMULA_MAP


class BuiltIns:
    @staticmethod
    def is_present(name: str) -> bool:
        return name in FORMULA_MAP

    @staticmethod
    def get(name: str, root: Node, param: Optional[Node]) -> Node | BuiltinsError:
        if not param:
            raise NotImplementedError("Auto search param not implemented yet")

        entry = FORMULA_MAP.get(name)
        assert entry, f"{name}, not present in builtins, use `BuiltIns.is_present`"

        to_replace = BuiltIns._find_match(root, param)
        if not to_replace:
            return NotMatchingParam(f"no match for {param}")

        match BuiltIns._bind_wildnodes(to_replace, entry.to_match):
            case NotMatchingFormula() as err:
                return err
            case cache:
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
    def _bind_wildnodes(
        node: Node, to_match: Node
    ) -> dict[str, Node] | NotMatchingFormula:
        """
        Recursively binds each WildNode in `to_match` to the corresponding node in `node`.
        Fills cache with {tag: Node} pair.
        """
        cache: dict[str, Node] = {}

        def aux(node_, to_match_) -> Optional[NotMatchingFormula]:
            match node_, to_match_:
                case Pow() as lhs, Pow() as rhs:
                    if err := aux(lhs.base, rhs.base):
                        return err
                    if err := aux(lhs.exponent, rhs.exponent):
                        return err

                case (Add() as lhs, Add() as rhs) | (Mul() as lhs, Mul() as rhs):
                    if err := aux(lhs.left, rhs.left):
                        return err
                    if err := aux(lhs.right, rhs.right):
                        return err

                case lhs, WildNode(tag=tag) if not tag in cache:
                    cache[tag] = lhs

                case Numeric(value=lvalue), Numeric(value=rvalue) if lvalue != rvalue:
                    return NotMatchingFormula(
                        f"Cannot use this formula because {lvalue} and {rvalue} aren't the same"
                    )

                case lhs, WildNode(tag=tag) if tag in cache and lhs != cache[tag]:
                    return NotMatchingFormula(
                        f"Cannot use this formula because {lhs} and {cache[tag]} aren't the same"
                    )

                case (Pow() | Add() | Mul()) as lhs, rhs if id(lhs) != id(
                    rhs
                ) and not isinstance(rhs, WildNode):
                    return NotMatchingFormula(
                        f"Cannot use this formula because {lhs} and {rhs} aren't the same"
                    )

            return None

        if err := aux(node, to_match):
            return err
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
