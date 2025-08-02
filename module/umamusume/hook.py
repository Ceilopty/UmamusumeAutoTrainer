import cv2

from bot.recog.image_matcher import image_match
from module.umamusume.context import UmamusumeContext, TurnOperationType
from module.umamusume.script.cultivate_task.ai import get_operation
from module.umamusume.asset.point import *
from module.umamusume.task import UmamusumeTaskType
import bot.base.log as logger

log = logger.get_logger(__name__)


def before_hook(ctx: UmamusumeContext):
    pass


def after_hook(ctx: UmamusumeContext):
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, BTN_SKIP).find_match:
        ctx.ctrl.click_by_point(SKIP)
    if ctx.task.task_type == UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE:
        if image_match(img, BTN_SKIP_OFF).find_match:
            ctx.ctrl.click_by_point(SCENARIO_SKIP_OFF)
        if image_match(img, BTN_SKIP_SPEED_1).find_match:
            ctx.ctrl.click_by_point(SCENARIO_SKIP_SPEED_1)
        detail = ctx.cultivate_detail
        if detail and detail.turn_info is not None:
            if detail.turn_info.parse_train_info_finish and detail.turn_info.parse_main_menu_finish:
                if detail.turn_info.turn_operation is None:
                    detail.turn_info.turn_operation = get_operation(ctx)
                    if not detail.turn_info.turn_info_logged:
                        detail.turn_info.log_turn_info(ctx.task.detail.scenario,
                                                       detail.turn_info.turn_operation.turn_operation_type in (
                                                           TurnOperationType.TURN_OPERATION_TYPE_TRAINING,
                                                           TurnOperationType.TURN_OPERATION_TYPE_REST,
                                                       ))
                        detail.turn_info.turn_info_logged = True
                    detail.turn_info.turn_operation.log_turn_operation()
    elif ctx.task.task_type == UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM:
        if image_match(img, BTN_SKIP).find_match:
            ctx.ctrl.click_by_point(SKIP)
