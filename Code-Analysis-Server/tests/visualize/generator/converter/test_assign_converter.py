import pytest

from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.models.assign_viz import AssignViz
from app.visualize.generator.models.variable_vlz import Variable, SubscriptIdx
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture()
def create_assign():
    def _create_assign_obj(targets, value, expressions, var_type):
        return AssignStmtObj(
            targets=targets,
            expr_stmt_obj=ExprStmtObj(
                id=1, value=value, expressions=expressions, expr_type=var_type, call_stack_name="main"
            ),
            call_stack_name="main",
        )

    return _create_assign_obj


@pytest.mark.parametrize(
    "targets, value, expressions, var_type, expected",
    [
        pytest.param(
            ["a"],
            3,
            ["3"],
            ExprType.VARIABLE,
            AssignViz(variables=[Variable(id=1, name="a", expr="3", type="variable", code="")], callStackName="main"),
            id="a = 3: success case",
        ),
        pytest.param(
            ["b"],
            4,
            ["a + 1", "3 + 1", "4"],
            ExprType.VARIABLE,
            AssignViz(variables=[Variable(id=1, name="b", expr="4", type="variable", code="")], callStackName="main"),
            id="b = a + 1: success case",
        ),
        pytest.param(
            ["c", "d"],
            5,
            ["b + 1", "4 + 1", "5"],
            ExprType.VARIABLE,
            AssignViz(
                variables=[
                    Variable(id=1, name="c", expr="5", type="variable", code=""),
                    Variable(id=1, name="d", expr="5", type="variable", code=""),
                ],
                callStackName="main",
            ),
            id="c, d = b + 1: success case",
        ),
        pytest.param(
            ["e"],
            [1, 2, 3],
            ["[1,2,3]"],
            ExprType.LIST,
            AssignViz(
                variables=[
                    Variable(id=1, name="e", expr="[1,2,3]", type="list", code="", idx=SubscriptIdx(start=0, end=2))
                ],
                callStackName="main",
            ),
            id="e = [1, 2, 3]: success case",
        ),
        pytest.param(
            ["f"],
            ["Hello", "World"],
            ["['Hello','World']"],
            ExprType.LIST,
            AssignViz(
                variables=[
                    Variable(
                        id=1, name="f", expr="['Hello','World']", type="list", code="", idx=SubscriptIdx(start=0, end=1)
                    )
                ],
                callStackName="main",
            ),
            id="f = ['Hello', 'World']: success case",
        ),
        pytest.param(
            ["g"],
            [11, "Hello"],
            ["[a + 1,b]", "[10 + 1,10]", "[11,10]"],
            ExprType.LIST,
            AssignViz(
                variables=[
                    Variable(id=1, name="g", expr="[11,10]", type="list", code="", idx=SubscriptIdx(start=0, end=1))
                ],
                callStackName="main",
            ),
            id="g = [a + 1, b]: success case",
        ),
    ],
)
def test_convert(create_assign, targets, value, expressions, var_type, expected):
    result = AssignConverter.convert(create_assign(targets, value, expressions, var_type), VisualizationManager())

    assert result == expected
