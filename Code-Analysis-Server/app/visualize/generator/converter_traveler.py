from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import ForStmtObj
from app.visualize.analysis.stmt.models.func_def_stmt_obj import FuncDefStmtObj
from app.visualize.analysis.stmt.models.if_stmt_obj import IfStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType
from app.visualize.analysis.stmt.models.user_func_stmt_obj import UserFuncStmtObj
from app.visualize.analysis.stmt.models.while_stmt_obj import WhileStmtObj
from app.visualize.generator.converter.assign_converter import AssignConverter
from app.visualize.generator.converter.expr_converter import ExprConverter
from app.visualize.generator.converter.flow_control_converter import FlowControlConverter
from app.visualize.generator.converter.for_header_converter import ForHeaderConvertor
from app.visualize.generator.converter.func_def_converter import FuncDefConverter
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.converter.return_converter import ReturnConverter
from app.visualize.generator.converter.user_func_converter import UserFuncConverter
from app.visualize.generator.converter.while_converter import WhileConverter
from app.visualize.generator.visualization_manager import VisualizationManager
from app.web.exception.code_visualize_error import CodeVisualizeError
from app.web.exception.error_enum import ErrorEnum


class ConverterTraveler:

    @staticmethod
    def travel(analysis_objs, viz_manager: VisualizationManager) -> list:
        viz_objs = []
        for analysis_obj in analysis_objs:
            if analysis_obj.type == StmtType.ASSIGN:
                viz_objs.extend(ConverterTraveler._convert_to_assign_vizs(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.FOR:
                for_viz_list = ConverterTraveler._for_convert(analysis_obj, viz_manager)
                viz_objs.extend(for_viz_list)

            elif analysis_obj.type == StmtType.EXPR:
                viz_objs.extend(ConverterTraveler._convert_to_expr_vizs(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.IF:
                viz_objs.extend(ConverterTraveler._if_convert(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.FLOW_CONTROL:
                viz_objs.extend(ConverterTraveler._convert_to_flow_control_viz(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.RETURN:
                viz_objs.extend(ConverterTraveler._convert_to_return_control_viz(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.WHILE:
                viz_objs.extend(ConverterTraveler._convert_to_while_viz(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.FUNC_DEF:
                viz_objs.append(ConverterTraveler._convert_to_func_def_viz(analysis_obj, viz_manager))

            elif analysis_obj.type == StmtType.USER_FUNC:
                viz_objs.extend(ConverterTraveler._convert_to_user_func_viz(analysis_obj, viz_manager, ()))

            else:
                raise TypeError(f"지원하지 않는 노드 타입입니다.: {analysis_obj.type}")

        if len(viz_objs) > 10000:
            raise CodeVisualizeError(ErrorEnum.VISUALIZE_TIMEOUT)

        return viz_objs

    @staticmethod
    def _convert_to_assign_vizs(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        steps = []

        if assign_obj.expr_stmt_obj.type == StmtType.USER_FUNC:
            steps.extend(
                ConverterTraveler._convert_to_user_func_viz(assign_obj.expr_stmt_obj, viz_manager, assign_obj.targets)
            )
            steps.append(AssignConverter.convert_user_func(assign_obj, viz_manager))
        else:
            steps.extend(ConverterTraveler._convert_to_expr_vizs(assign_obj.expr_stmt_obj, viz_manager))
            steps.append(AssignConverter.convert(assign_obj, viz_manager))

        return steps

    @staticmethod
    def _for_convert(for_stmt: ForStmtObj, viz_manager: VisualizationManager):
        steps = []
        # header
        header_viz = ForHeaderConvertor.convert(for_stmt, viz_manager)
        viz_manager.increase_depth()
        for body_obj in for_stmt.body_objs:
            # header step 추가
            steps.append(ForHeaderConvertor.get_updated_header(header_viz, body_obj.cur_value))
            # body step 추가
            steps.extend(ConverterTraveler.travel(body_obj.body_steps, viz_manager))
        viz_manager.decrease_depth()

        return steps

    @staticmethod
    def _if_convert(if_stmt: IfStmtObj, viz_manager: VisualizationManager):
        steps = list()
        # 1. if-else 구조 define
        steps.append(IfConverter.convert_to_if_else_define_viz(if_stmt.conditions, viz_manager))
        # 2. if header
        steps.extend(IfConverter.convert_to_if_else_change_viz(if_stmt.conditions, viz_manager))
        # 3. if header 결과 값이 true인 if 문의 body obj의 viz 생성
        if if_stmt.body_steps:
            steps.extend(ConverterTraveler._get_if_body_viz_list(if_stmt.body_steps, viz_manager))

        return steps

    @staticmethod
    def _get_if_body_viz_list(if_body_steps: list, viz_manager):
        viz_manager.increase_depth()
        body_steps_viz = ConverterTraveler.travel(if_body_steps, viz_manager)
        viz_manager.decrease_depth()

        return body_steps_viz

    @staticmethod
    def _convert_to_expr_vizs(expr_stmt_obj, viz_manager: VisualizationManager):
        return ExprConverter.convert(expr_stmt_obj, viz_manager)

    @staticmethod
    def _convert_to_flow_control_viz(flow_control_obj, viz_manager: VisualizationManager):
        flow_control_viz = FlowControlConverter.convert(flow_control_obj, viz_manager)

        return flow_control_viz

    @staticmethod
    def _convert_to_return_control_viz(return_obj, viz_manager: VisualizationManager):
        return_viz = ReturnConverter.convert(return_obj, viz_manager)

        return return_viz

    @staticmethod
    def _convert_to_while_viz(while_obj: WhileStmtObj, viz_manager: VisualizationManager):
        steps = []
        depth = viz_manager.get_depth()

        while_define_viz = WhileConverter.convert_to_while_define_viz(while_obj, viz_manager, depth)

        for while_cycle in while_obj.while_cycles:
            # condition convert
            steps.append(while_define_viz)
            steps.extend(
                WhileConverter.convert_to_while_change_condition_viz(while_obj.id, viz_manager, while_cycle, depth)
            )
            # body convert
            viz_manager.increase_depth()
            steps.extend(ConverterTraveler.travel(while_cycle.body_objs, viz_manager))
            viz_manager.decrease_depth()

        return steps

    @staticmethod
    def _convert_to_func_def_viz(func_def_stmt_obj: FuncDefStmtObj, viz_manager: VisualizationManager):
        return FuncDefConverter.convert(func_def_stmt_obj, viz_manager)

    @staticmethod
    def _convert_to_user_func_viz(user_func_stmt_obj: UserFuncStmtObj, viz_manager: VisualizationManager, targets):
        user_func_viz = []

        user_func_viz.append(UserFuncConverter.convert_to_call_user_func(user_func_stmt_obj, viz_manager))
        user_func_viz.append(UserFuncConverter.convert_to_create_call_stack(user_func_stmt_obj, viz_manager))

        viz_manager.increase_depth()
        user_func_viz.extend(ConverterTraveler.travel(user_func_stmt_obj.body_steps, viz_manager))
        viz_manager.decrease_depth()

        user_func_viz.append(UserFuncConverter.convert_to_end_user_func(user_func_stmt_obj, targets, viz_manager))

        return user_func_viz
