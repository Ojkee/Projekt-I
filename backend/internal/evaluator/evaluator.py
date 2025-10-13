from backend.internal.evaluator.objects import Object, SubjectObject, TransformObject

from backend.internal.ast import Program, ASTNode
from backend.internal.statements import Subject, AtomTransform, Formula, LineError
from backend.internal.expressions import Expression, Infix, Prefix, Number, Identifier
from backend.internal.tokens import TokenType, Token

from backend.internal.expressionTree import Node, convert_to_expression_tree

class Evaluator:
    def eval(self, node: ASTNode) -> Object:
        match node:
            # Statements
            case Program():
                return self._eval_program(node)
            case Subject():
                return self.eval(node.expression())
            case AtomTransform():
                return self._evaluate_atom_transform(node)
            case Formula():
                raise NotImplementedError("Formula evaluation not implemented yet.")
            case LineError():
                raise NotImplementedError("LineError evaluation not implemented yet.")
            
            # Expressions
            case Infix():
                if node.operator == Token(TokenType.EQUALS, '='):
                    return SubjectObject(
                        self._convert_expression(node.left()),
                        self._convert_expression(node.right())
                    )
                return SubjectObject(self._convert_expression(node), None)
            case Prefix():
                return SubjectObject(self._convert_expression(node), None)
            case Number():
                return SubjectObject(self._convert_expression(node), None)
            case Identifier():
                return SubjectObject(self._convert_expression(node), None)
            case _:
                raise ValueError(f"Unknown AST node type: {type(node)}")

    def _convert_expression(self, expr: Expression) -> Node:
        tree = convert_to_expression_tree(expr)
        return tree.reduce()

    def _evaluate_atom_transform(self, transform: AtomTransform) -> Object:
        operator = transform.operator().literal
        expr = self.eval(transform.expression())

        return TransformObject(operator, expr)

    def _eval_program(self, program: Program) -> Object:
        subject_object = None
        for stmt in program.get():
            object = self.eval(stmt)
            match object:
                case SubjectObject():
                    subject_object = object
                case TransformObject():
                    if subject_object is not None:
                        subject_object.transform(object.operator, object.transform)
                case _:
                    raise ValueError(f"Unknown object type: {type(object)}")

        return subject_object


