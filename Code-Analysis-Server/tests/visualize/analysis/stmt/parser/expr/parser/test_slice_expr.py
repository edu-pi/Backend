import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import SliceObj, ConstantObj, NameObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.analysis.stmt.parser.expr.models.slice_expression import SliceExpression
from app.visualize.analysis.stmt.parser.expr.parser.slice_expr import SliceExpr


@pytest.mark.parametrize(
    "lower, upper, step, expected",
    [
        pytest.param(
            None,
            ConstantObj(value=10, expressions=("10",)),
            None,
            SliceObj(value=slice(None, 10, None), expressions=(SliceExpression(upper="10"),)),
            id="[:10]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            ConstantObj(value=10, expressions=("10",)),
            None,
            SliceObj(value=slice(0, 10, None), expressions=(SliceExpression(lower="0", upper="10"),)),
            id="[0:10]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            None,
            SliceObj(
                value=slice(0, 10, None),
                expressions=(
                    SliceExpression(lower="0", upper="a"),
                    SliceExpression(lower="0", upper="10"),
                ),
            ),
            id="[0:a]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            ConstantObj(value=10, expressions=("10",)),
            ConstantObj(value=2, expressions=("2",)),
            SliceObj(value=slice(0, 10, 2), expressions=(SliceExpression(lower="0", upper="10", step="2"),)),
            id="[0:10:2]: success case",
        ),
    ],
)
def test_parse(mocker, lower: ExprObj, upper: ExprObj, step: ExprObj, expected: SliceObj):
    mock_get_value = mocker.patch.object(SliceExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(SliceExpr, "_create_expressions", return_value=expected.expressions)

    result = SliceExpr.parse(lower, upper, step)

    assert isinstance(result, SliceObj)
    mock_get_value.assert_called_once_with(lower, upper, step)
    mock_create_expressions.assert_called_once_with(lower, upper, step)


@pytest.mark.parametrize(
    "lower, upper, step, expected",
    [
        pytest.param(
            ConstantObj(value=2, expressions=("2",)),
            ConstantObj(value=10, expressions=("10",)),
            None,
            slice(2, 10, None),
            id="[2:10]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            ConstantObj(value=10, expressions=("10",)),
            None,
            slice(0, 10, None),
            id="[0:a]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            ConstantObj(value=10, expressions=("10",)),
            ConstantObj(value=2, expressions=("2",)),
            slice(0, 10, 2),
            id="[0:10:2]: success case",
        ),
    ],
)
def test_get_value(lower: ExprObj, upper: ExprObj, step: ExprObj, expected):
    result = SliceExpr._get_value(lower, upper, step)

    assert result == expected


@pytest.mark.parametrize(
    "lower, upper, step, expected",
    [
        pytest.param(
            ConstantObj(value=2, expressions=("2",)),
            ConstantObj(value=10, expressions=("10",)),
            None,
            (SliceExpression(lower="2", upper="10"),),
            id="[2:10]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            NameObj(value=10, expressions=("a", "10"), type=ExprType.VARIABLE),
            None,
            (SliceExpression(lower="0", upper="a"), SliceExpression(lower="0", upper="10")),
            id="[0:a]: success case",
        ),
        pytest.param(
            ConstantObj(value=0, expressions=("0",)),
            ConstantObj(value=10, expressions=("10",)),
            ConstantObj(value=2, expressions=("2",)),
            (SliceExpression(lower="0", upper="10", step="2"),),
            id="[0:10:2]: success case",
        ),
        pytest.param(
            ConstantObj(value=2, expressions=("2",)),
            None,
            None,
            (SliceExpression(lower="2"),),
            id="[2:]: success case",
        ),
        pytest.param(
            None,
            ConstantObj(value=5, expressions=("5",)),
            None,
            (SliceExpression(upper="5"),),
            id="[:5]: success case",
        ),
        pytest.param(
            None,
            None,
            None,
            (SliceExpression(),),
            id="[:]: success case",
        ),
    ],
)
def test_create_expressions(lower: ExprObj, upper: ExprObj, step: ExprObj, expected: tuple[SliceExpression, ...]):
    result = SliceExpr._create_expressions(lower, upper, step)

    assert result == expected
