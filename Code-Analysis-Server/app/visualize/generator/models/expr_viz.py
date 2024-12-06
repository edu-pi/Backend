from dataclasses import dataclass

from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType


@dataclass(frozen=True)
class ExprViz:
    id: int
    depth: int
    expr: ExprType
    code: str
    type: str
