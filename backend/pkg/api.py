import json
from typing import NamedTuple
from backend.internal.lexing import Lexer
from backend.internal.math_builtins.formulas import FORMULA_MAP
from backend.internal.tokenstreams import TokenStream
from backend.internal.parsing import Parser
from backend.internal.evaluators import Evaluator


def run_code(input: str) -> list[str]:
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
        [("display_name", str), ("box_name", str), ("latex_str", str)],
    )
    formulas = (
        Formula_tuple(entry.display_name, box_name, entry.latex_str)
        for box_name, entry in FORMULA_MAP.items()
    )
    formulas_dict = (formula._asdict() for formula in formulas)
    json_bytes = json.dumps(formulas_dict).encode("utf-8")
    return json_bytes
