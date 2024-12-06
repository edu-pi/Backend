import ast

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import NameObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.container.element_container import ElementContainer


class NameExpr:

    @staticmethod
    def parse(node: ast.Name, elem_container: ElementContainer):
        if isinstance(node.ctx, ast.Store):
            return NameObj(value=node.id, expressions=(node.id,), type=ExprType.NAME)

        elif isinstance(node.ctx, ast.Load):
            value = NameExpr._get_identifier_value(node.id, elem_container)
            expressions = NameExpr._create_expressions(node.id, value)
            return NameObj(value=value, expressions=expressions, type=ExprType.judge_collection_type(value))

        elif isinstance(node.ctx, ast.Del):
            raise NotImplementedError(f"Unsupported node type: {type(node.ctx)}")

        else:
            raise TypeError(f"[NameExpr] {type(node.ctx)}는 잘못된 타입입니다.")

    # 변수의 값을 가져오는 함수
    @staticmethod
    def _get_identifier_value(identifier_name, elem_container: ElementContainer):
        try:
            return elem_container.get_element(name=identifier_name)
        except NameError as e:
            raise NameError(f"[NameExpr]: {identifier_name}은 정의되지 않은 변수입니다.") from e

    # 변수의 변화 과정을 만들어 주는 함수
    @staticmethod
    def _create_expressions(identifier_name, value) -> tuple:
        if isinstance(value, str):
            return tuple([identifier_name, f"'{value}'"])

        return tuple([identifier_name, str(value)])
