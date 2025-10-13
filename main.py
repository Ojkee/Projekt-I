from backend.internal.evaluator.evaluator import Evaluator
from backend.internal.lexing import Lexer
from backend.internal.parsing import Parser
from backend.internal.tokenstreams import TokenStream
from backend.internal.statements import Subject

print("-------------------------")
print("Type 'exit' to quit")
while True:
    try:
        inp = input(">>> ").strip()
        if inp.lower() == "exit":
            break
        if not inp:
            continue

        lexer = Lexer(inp)
        stream = TokenStream(lexer)

        parser = Parser(stream)
        program = parser.parse()

        stmts = program.get()

        evaluator = Evaluator(program)

        tree = evaluator.eval_program()

        print("Tree:", tree)

    except Exception as e:
        print("Error:", e)
