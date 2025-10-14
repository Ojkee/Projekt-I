import copy
from backend.internal.objects import (
    SubjectObject,
    ExpressionObject,
    EquationObject,
    TransformObject,
    AtomTransformObject,
    ErrorObject,
)

from backend.internal.ast import Program
from backend.internal.statements import (
    Statement,
    Subject,
    AtomTransform,
    Formula,
    LineError,
)
from backend.internal.expressions import Expression, Infix, Prefix, Number, Identifier
from backend.internal.tokens import TokenType

from backend.internal.expression_tree import Node, convert_to_expression_tree


class Evaluator:
    def eval(self, program: Program) -> list[SubjectObject]:
        match program.get():
            case [Subject() as subject, *stmts]:
                return self._eval_statements(subject, stmts)
            case stmts if not stmts:
                return [ErrorObject("No input")]
            case _:
                return [ErrorObject("First line must be equation or expression")]

    def _eval_statements(
        self, subject: Subject, stmts: list[Statement]
    ) -> list[SubjectObject]:
        subject_object = self._eval_expression(subject.expression())
        assert isinstance(subject_object, SubjectObject)

        subjects: list[SubjectObject] = [copy.deepcopy(subject_object)]

        for stmt in stmts:
            match self._eval_statement(stmt):
                case SubjectObject() as sub:
                    subject_object = sub
                case AtomTransformObject() as atom:
                    subject_object.transform(atom)
            subjects.append(copy.deepcopy(subject_object))

        return subjects

    def _eval_statement(self, stmt: Statement) -> TransformObject | SubjectObject:
        match stmt:
            case Subject():
                return self._eval_expression(stmt.expression())
            case AtomTransform():
                return self._eval_atom_transform(stmt)
            case Formula():
                raise NotImplementedError("Formula evaluation not implemented yet.")
            case LineError():
                raise NotImplementedError("LineError evaluation not implemented yet.")
            case _:
                raise NotImplementedError(
                    f"{type(stmt)} evaluation not implemented yet."
                )

    def _eval_expression(self, expr: Expression) -> TransformObject | SubjectObject:
        match expr:
            case Infix(_op=op, _lhs=lhs, _rhs=rhs) if op.ttype == TokenType.EQUALS:
                return EquationObject(
                    self._convert_expression(lhs),
                    self._convert_expression(rhs),
                )
            case Infix() | Prefix() | Number() | Identifier():
                return ExpressionObject(self._convert_expression(expr))
            case _:
                raise ValueError(f"Can't eval type: {type(expr)}")

    def _convert_expression(self, expr: Expression) -> Node:
        tree = convert_to_expression_tree(expr)
        assert tree
        return tree.reduce()

    def _eval_atom_transform(self, transform: AtomTransform) -> AtomTransformObject:
        operator = transform.operator()
        expr_node = self._convert_expression(transform.expression())
        return AtomTransformObject(operator, expr_node)
