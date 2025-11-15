from dataclasses import asdict, dataclass
from typing import TypeAlias
from backend.internal.lexing import Lexer
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


FrontFormula: TypeAlias = dict[str, str]
FrontFormulas: TypeAlias = dict[str, list[FrontFormula]]


def get_implemented_formulas_json() -> FrontFormulas:
    @dataclass(frozen=True)
    class FormData:
        pass

    def formula_dict() -> FrontFormula:
        return asdict(FormData())

    result: FrontFormulas = {}
    for category_name, category in FORMULA_MAP.items():
        pass
    return result
