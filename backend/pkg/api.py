import json
from typing import NamedTuple
from backend.internal.lexing import Lexer
from backend.internal.math_builtins.formula_entry import FormulaEntry
from backend.internal.math_builtins.formula_handler import FORMULA_MAP
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser
from backend.internal.evaluators import Evaluator


def compile_math_input(input: str) -> list[str]:
    """
    Runs the input code through the full pipeline: lexing, parsing, and evaluating.
    Returns the string representations of the resulting SubjectObjects or error messages.

    Args:
        input (str): The input code to be processed.
    Returns:
        list[str]: A list of string representations of the resulting SubjectObjects or error messages.
    """

    lexer = Lexer(input)
    token_stream = TokenStream(lexer)
    parser = Parser(token_stream)
    program = parser.parse()
    evaluator = Evaluator()
    result = evaluator.eval(program)

    return [str(obj) for obj in result]


def get_implemented_formulas_json() -> bytes:
    Formula_tuple = NamedTuple(
        "Formula_tuple",
        [
            ("display_name", str),
            ("box_name", str),
            ("latex_str", str),
        ],
    )
    Category_tuple = NamedTuple(
        "Category_tuple",
        [
            ("name", str),
            ("formulas", list[Formula_tuple]),
        ],
    )

    def to_formula_tuple(fk: str, fv: FormulaEntry):
        return Formula_tuple(fv.display_name, fk, fv.latex_str)

    categories = []
    for cat_name, forms in FORMULA_MAP.items():
        form_tuples = [to_formula_tuple(*form) for form in forms.items()]
        cat = Category_tuple(cat_name, form_tuples)
        categories.append(cat)

    json_bytes = json.dumps(categories).encode("utf-8")
    return json_bytes
