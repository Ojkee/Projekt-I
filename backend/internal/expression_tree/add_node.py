from __future__ import annotations
from .node import Node, FlattenNode
from backend.internal.expression_tree.numeric_node import FlattenNumeric, Numeric
from backend.internal.expression_tree.mul_node import FlattenMul
from backend.internal.expression_tree.symbol_node import FlattenSymbol
from backend.internal.expression_tree.pow_node import FlattenPow


class Add(Node):
    __match_args__ = ("left", "right")

    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            isinstance(other, Add)
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self):
        return "(" + repr(self.left) + "+" + repr(self.right) + ")"

    def __str__(self) -> str:
        return self.flatten().__str__()

    def flatten(self) -> FlattenAdd:
        children: list[FlattenNode] = []

        def _flat_node(n: Node) -> None:
            if isinstance(n, Add):
                flat = n.flatten()
                children.extend(flat.children)
            else:
                children.append(n.flatten())

        _flat_node(self.left)
        _flat_node(self.right)

        return FlattenAdd(children)

    def reduce(self) -> Node:
        left = self.left.reduce()
        right = self.right.reduce()

        match left, right:
            # 0 + x or x + 0 => x
            case (Numeric(0), other) | (other, Numeric(0)):
                return other

            case Numeric(a), Numeric(b):
                return Numeric(a + b)

        return Add(left, right)


class FlattenAdd(FlattenNode):
    PRECEDENCE = 1

    def __init__(self, chidren: list[FlattenNode]) -> None:
        self.children = chidren

    def constant_fold(self):
        numeric_sum = 0.0
        new_children = []

        for child in self.children:
            folded = child.constant_fold()

            if isinstance(folded, FlattenNumeric):
                numeric_sum += folded.value
            else:
                new_children.append(folded)

        if numeric_sum != 0 or not new_children:
            new_children.insert(0, FlattenNumeric(numeric_sum))

        if len(new_children) == 1:
            return new_children[0]

        return FlattenAdd(new_children)

    def __str__(self) -> str:
        parts = []
        for c in self.children:
            if isinstance(c, FlattenNumeric) and c.value < 0:
                parts.append(f"- {abs(c.value)}")
            elif isinstance(c, FlattenMul) and c.children[0] == FlattenNumeric(-1):
                parts.append(f"- {c}")
            elif c.precedence() < self.PRECEDENCE:
                parts.append(f"({c})")
            else:
                parts.append(f"+ {c}")

        result = " ".join(parts).strip()
        if result.startswith("+ "):
            result = result[2:]

        return result

    def unflatten(self) -> Add:
        if not self.children:
            raise ValueError("Cannot unflatten a Add node with no children.")

        result: Node = self.children[0].unflatten()
        for child in self.children[1:]:
            child_unflattened = child.unflatten()
            result = Add(result, child_unflattened)

        return result

    def __eq__(self, other):
        return isinstance(other, FlattenAdd) and self.children == other.children

    def precedence(self):
        return self.PRECEDENCE

    def canonical_sort(self):
        def extract_symbol_and_power(term):
            if isinstance(term, FlattenNumeric):
                return ("~", 0)

            if isinstance(term, FlattenSymbol):
                return (term.name, 1)

            if isinstance(term, FlattenPow) and isinstance(term.base, FlattenSymbol) and isinstance(term.exponent, FlattenNumeric):
                return (term.base.name, term.exponent.value)

            if isinstance(term, FlattenMul):
                max_symbol = "~"
                max_power = 0
                for c in term.children:
                    if isinstance(c, FlattenSymbol):
                        if c.name < max_symbol:
                            max_symbol = c.name
                            max_power = 1
                    elif isinstance(c, FlattenPow) and isinstance(c.base, FlattenSymbol) and isinstance(c.exponent, FlattenNumeric):
                        if c.base.name < max_symbol:
                            max_symbol = c.base.name
                            max_power = c.exponent.value
                        elif c.base.name == max_symbol:
                            max_power = max(max_power, c.exponent.value)
                return (max_symbol, max_power)

            return ("~", 0)

        def key(term):
            symbol, power = extract_symbol_and_power(term)
            return (symbol,-power)

        self.children.sort(key=key)


# RULES

# ---------- Rule: Sort children ----------
def rule_canonical_form(node: FlattenNode) -> FlattenNode | None:
    if isinstance(node, FlattenAdd) or isinstance(node, FlattenMul):
        if hasattr(node, "canonical_sort"):
            return node.canonical_sort()
    return None


# ---------- Rule: Constant Fold ----------
def rule_constant_fold(node: FlattenNode) -> FlattenNode | None:
    if hasattr(node, "constant_fold"):
        return node.constant_fold()
    return None


# ---------- Rule: Combine Like Terms ----------
def rule_combine_like_terms(node: FlattenNode) -> FlattenNode| None:
    if not isinstance(node, FlattenAdd):
        return None

    terms: list[tuple[FlattenNode, float]] = []
    numeric_sum = 0.0

    for child in node.children:
        if isinstance(child, FlattenNumeric):
            numeric_sum += child.value
            continue

        if isinstance(child, FlattenSymbol):
            base = child
            coeff = 1.0
        elif isinstance(child, FlattenMul):
            coeff = 1.0
            base_factors = []
            for f in child.children:
                if isinstance(f, FlattenNumeric):
                    coeff *= f.value
                else:
                    base_factors.append(f)
            if len(base_factors) == 1:
                base = base_factors[0]
            else:
                base = FlattenMul(base_factors)
        else:
            base = child
            coeff = 1.0

        for i, (existing_base, existing_coeff) in enumerate(terms):
            if existing_base == base:
                terms[i] = (existing_base, existing_coeff + coeff)
                break
        else:
            terms.append((base, coeff))

    new_children = []

    if numeric_sum != 0:
        new_children.append(FlattenNumeric(numeric_sum))

    for base, coeff in terms:
        if coeff == 1:
            new_children.append(base)
        else:
            new_children.append(FlattenMul([FlattenNumeric(coeff), base]))

    if len(new_children) == 1:
        return new_children[0]

    return FlattenAdd(new_children)



# ---------- Rule: Distribute Mul----------
def rule_distribute_mul(node: FlattenNode) -> FlattenNode | None:
    if not isinstance(node, FlattenMul):
        return None
    
    for i, child in enumerate(node.children):
        if isinstance(child, FlattenAdd):
            other_factors = node.children[:i] + node.children[i+1:]
            distributed_terms = []
            for term in child.children:
                distributed_terms.append(FlattenMul([term] + other_factors))
            return FlattenAdd(distributed_terms)

    return None

# ---------- Rule: Combine powers in multiplication ----------
def rule_combine_powers(node: "FlattenNode") -> "FlattenNode" | None:
    if not isinstance(node, FlattenMul):
        return None

    powers: dict[str, float] = {}
    new_factors: list[FlattenNode] = []

    for child in node.children:
        if isinstance(child, FlattenPow) and isinstance(child.base, FlattenSymbol) and isinstance(child.exponent, FlattenNumeric):
            key = child.base.name
            powers[key] = powers.get(key, 0) + child.exponent.value
        elif isinstance(child, FlattenSymbol):
            key = child.name
            powers[key] = powers.get(key, 0) + 1
        else:
            new_factors.append(child)

    for sym_name, exp in powers.items():
        if exp == 1:
            new_factors.append(FlattenSymbol(sym_name))
        else:
            new_factors.append(FlattenPow(FlattenSymbol(sym_name), FlattenNumeric(exp)))

    if len(new_factors) == 1:
        return new_factors[0]

    return FlattenMul(new_factors)


RULES = [
    rule_combine_like_terms,
    rule_distribute_mul,
    rule_canonical_form,
    rule_combine_powers,
    rule_constant_fold,
]

def simplify(node: FlattenNode) -> FlattenNode:
    prev_str = ""
    current = node
    while str(current) != prev_str: #TODO: constant_fold czasami nie dziala po aplikacji wszystkich reguł
        prev_str = str(current)
        current = _apply_rules_recursively(current)
    return current


def _apply_rules_recursively(node: FlattenNode) -> FlattenNode:
    if isinstance(node, FlattenAdd) or isinstance(node, FlattenMul):
        node.children = [_apply_rules_recursively(c) for c in node.children]
    elif isinstance(node, FlattenPow):
        node.base = _apply_rules_recursively(node.base)
        node.exponent = _apply_rules_recursively(node.exponent)

    for rule in RULES:
        new_node = rule(node)
        if new_node is not None:
            node = new_node
    return node