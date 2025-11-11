import copy

from backend.internal.evaluators.error_msgs import EvaluatorErrorUserMsg
from backend.internal.evaluators.validator import Validator
from backend.internal.math_builtins import BuiltIns
from backend.internal.objects import (
    Object,
    SubjectObject,
    ExpressionObject,
    EquationObject,
    AtomTransformObject,
    FormulaObject,
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
            case []:
                return [ErrorObject(EvaluatorErrorUserMsg.no_input())]
            case [Subject() as subject, *stmts]:
                return self._eval_statements(subject, stmts)
            case [LineError(perr) as err, *stmts] if perr.highest_precedence():
                return [ErrorObject(str(err))]
            case _:
                return [ErrorObject(EvaluatorErrorUserMsg.no_expr())]

    def _eval_statements(
        self, subject: Subject, stmts: list[Statement]
    ) -> list[SubjectObject]:
        subject_object = self._eval_expression(subject.expr)
        assert isinstance(subject_object, SubjectObject)
        if err_msg := Validator.check(subject_object):
            return [ErrorObject(err_msg)]

        subjects: list[SubjectObject] = [copy.deepcopy(subject_object)]

        for stmt in stmts:
            obj = self._eval_statement(stmt)
            if err_msg := Validator.check(obj):
                return subjects + [ErrorObject(err_msg)]

            match obj:
                case SubjectObject() as sub:
                    subject_object = sub
                case (AtomTransformObject() | FormulaObject()) as t_obj:
                    try:
                        subject_object.apply(t_obj)
                    except ValueError as e:
                        subjects.append(ErrorObject(str(e)))
                        break
                case ErrorObject() as err:
                    subjects.append(err)
                    break
                case obj:
                    raise ValueError(f"Unimplemented transform type: {type(obj)}")

            if err_msg := Validator.check(subject_object):
                return subjects + [ErrorObject(err_msg)]
            subjects.append(copy.deepcopy(subject_object))

        return subjects

    def _eval_statement(self, stmt: Statement) -> Object:
        match stmt:
            case Subject(expr):
                return self._eval_expression(expr)
            case AtomTransform() as atom:
                return self._eval_atom_transform(atom)
            case Formula() as formula:
                return self._eval_formula(formula)
            case LineError() as err:
                return ErrorObject(str(err))
            case _:
                raise NotImplementedError(
                    f"{type(stmt)} evaluation not implemented yet."
                )

    def _eval_expression(self, expr: Expression) -> Object:
        match expr:
            case Infix(op, lhs, rhs) if op.ttype == TokenType.EQUALS:
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
        expr_node = self._convert_expression(transform.expr)
        return AtomTransformObject(transform.operator, expr_node)

    def _eval_formula(self, formula: Formula) -> FormulaObject | ErrorObject:
        name = formula.name.literal
        if not BuiltIns.is_present(name):
            return ErrorObject(EvaluatorErrorUserMsg.no_formula(name))

        param_nodes = [self._convert_expression(expr) for expr in formula.params]
        return FormulaObject(formula.name, param_nodes)
