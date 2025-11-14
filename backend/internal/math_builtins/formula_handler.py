from collections.abc import Mapping
from typing import Callable, TypeAlias
from backend.internal.math_builtins.formula_entry import FormulaEntry

FormulaCategory: TypeAlias = Mapping[str, FormulaEntry]


class FormulaHandler:
    def __init__(self) -> None:
        self._formulas: dict[str, Mapping[str, FormulaEntry]] = {}

    def formula_category(self, category_name: str):
        def register(category: FormulaCategory | Callable[[], FormulaCategory]):
            self._formulas[category_name] = (
                category() if callable(category) else category
            )
            return category

        return register

    def __getitem__(self, formula_name: str) -> FormulaEntry:
        for category in self._formulas.values():
            if formula_name in category:
                return category[formula_name]
        raise KeyError(f"No formula {formula_name}")

    def __contains__(self, formula_name: str) -> bool:
        return any(formula_name in category for category in self._formulas.values())


FORMULA_MAP = FormulaHandler()

# Trigger auto-discovery of formula modules (registration happens on import).
import backend.internal.math_builtins.formulas as _  # noqa: F401, E402
