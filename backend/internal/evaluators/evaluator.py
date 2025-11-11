import copy

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
            case [Subject() as subject, *stmts]:
                return self._eval_statements(subject, stmts)
            case stmts if not stmts:
                return [ErrorObject("No input")]
            case _:
                return [ErrorObject("First line must be equation or expression")]

    def _eval_statements(
        self, subject: Subject, stmts: list[Statement]
    ) -> list[SubjectObject]:
        subject_object = self._eval_expression(subject.expr)
        assert isinstance(subject_object, SubjectObject)

        subjects: list[SubjectObject] = [copy.deepcopy(subject_object)]

        for stmt in stmts:
            match self._eval_statement(stmt):
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

            subjects.append(copy.deepcopy(subject_object))

        return subjects

    def _eval_statement(self, stmt: Statement) -> Object:
        match stmt:
            case Subject(_expr=expr):
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
        return tree

    def _eval_atom_transform(self, transform: AtomTransform) -> AtomTransformObject:
        expr_node = self._convert_expression(transform.expr)
        return AtomTransformObject(transform.operator, expr_node)

    def _eval_formula(self, formula: Formula) -> FormulaObject | ErrorObject:
        name = formula.name.literal
        if not BuiltIns.is_present(name):
            return ErrorObject(f"No formula `{name}`")

        param_nodes = [self._convert_expression(expr) for expr in formula.params]
        return FormulaObject(formula.name, param_nodes)
