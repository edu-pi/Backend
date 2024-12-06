from unittest.mock import patch

import pytest

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.flow_control_obj import PassStmtObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfConditionObj, IfStmtObj, ElifConditionObj
from app.visualize.analysis.stmt.parser.expr.models.expr_type import ExprType
from app.visualize.generator.converter.flow_control_converter import FlowControlConverter
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.converter_traveler import ConverterTraveler
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.fixture
def get_if_stmt_obj():
    def _get_if_stmt_obj():
        return IfStmtObj(
            conditions=(
                IfConditionObj(id=1, expressions=("9 == 10", "False"), result=False),
                ElifConditionObj(id=3, expressions=("9 < 10", "True"), result=True),
            ),
            body_steps=[
                ExprStmtObj(
                    id=4, value="world\n", expressions=("'world'",), expr_type=ExprType.PRINT, call_stack_name="main"
                )
            ],
        )

    return _get_if_stmt_obj


def test__if_convert(mocker, get_if_stmt_obj, mock_viz_manager_with_custom_depth):
    if_stmt_obj = get_if_stmt_obj()

    mock_get_header_define_viz = mocker.patch.object(IfConverter, "convert_to_if_else_define_viz")
    mock_get_header_change_steps = mocker.patch.object(IfConverter, "convert_to_if_else_change_viz")
    mock_get_if_body_viz_list = mocker.patch.object(ConverterTraveler, "_get_if_body_viz_list")
    mock_viz_manager = mock_viz_manager_with_custom_depth(1)

    ConverterTraveler._if_convert(if_stmt_obj, mock_viz_manager)

    # 함수들이 호출 되었는지 확인
    mock_get_header_define_viz.assert_called_once_with(if_stmt_obj.conditions, mock_viz_manager)
    mock_get_header_change_steps.assert_called_once_with(if_stmt_obj.conditions, mock_viz_manager)
    mock_get_if_body_viz_list.assert_called_once_with(if_stmt_obj.body_steps, mock_viz_manager)


def test__get_if_body_viz_list(mocker, get_if_stmt_obj):
    if_stmt_obj = get_if_stmt_obj()

    mock_travel = mocker.patch.object(ConverterTraveler, "travel")
    viz_manager = VisualizationManager()

    ConverterTraveler._get_if_body_viz_list(if_stmt_obj.body_steps, viz_manager)

    # travel 함수가 호출 되었는지 확인
    mock_travel.assert_called_once_with(if_stmt_obj.body_steps, viz_manager)


def test__convert_to_flow_control_viz_pass_호출(mock_viz_manager_with_custom_depth):
    node = PassStmtObj(id=1)
    mock_viz_manager = mock_viz_manager_with_custom_depth(1)

    with (patch.object(FlowControlConverter, "convert") as mock_convert_to_pass,):
        ConverterTraveler._convert_to_flow_control_viz(node, mock_viz_manager)

        mock_convert_to_pass.assert_called_once_with(node, mock_viz_manager)
