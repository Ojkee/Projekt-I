from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.tokenstreams import TokenStream
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
    subject = parser.parse()
    evaluator = Evaluator()
    result = evaluator.eval(subject)

    return [str(obj) for obj in result] if result else []