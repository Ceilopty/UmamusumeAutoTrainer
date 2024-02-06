import datetime
import cv2

from bot.base.task import TaskStatus, EndTaskReason
from bot.recog.image_matcher import image_match, compare_color_equal
from module.umamusume.task import EndTaskReason as UEndTaskReason
from module.umamusume.context import UmamusumeContext, UmamusumeTaskType
from module.umamusume.asset.template import REF_TEAM_STADIUM_OFF, REF_TEAM_STADIUM_OFF2
from module.umamusume.asset.point import (TO_RACE, TO_TEAM_STADIUM, GO_HOME_FROM_RACE, TO_TEAM_RACE, TEAM_STADIUM_RACE,
                                          TEAM_STADIUM_NEXT, TEAM_STADIUM_RETURN, TEAM_STADIUM_SHORTEN,
                                          TEAM_STADIUM_OPPO_UP, TEAM_STADIUM_OPPO_MID, TEAM_STADIUM_OPPO_DOWN,
                                          TEAM_STADIUM_OPPO_REFRESH, TEAM_STADIUM_CONTINUE, TEAM_STADIUM_CHECK_RESULTS,
                                          TEAM_STADIUM_CLAIM_REWARDS, TO_TIME_SALE,
                                          TEAM_STADIUM_RACE_AGAIN, TEAM_STADIUM_RP_CANCEL)
from .select_opponent import select_opponent

NO_RP_RETRY_PENDING = 7200


def ts_script_main_menu(ctx: UmamusumeContext):
    if on_task(ctx):
        if ctx.team_stadium_detail.off:
            ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.OFF)
            return
        if not no_rp(ctx):
            ctx.ctrl.click_by_point(TO_RACE)
        elif ctx.team_stadium_detail.raced:
            ctx.task.end_task(TaskStatus.TASK_STATUS_SUCCESS, EndTaskReason.COMPLETE)
        else:
            ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.RP_NOT_ENOUGH)


def ts_script_race_home(ctx: UmamusumeContext):
    if on_task(ctx) and not no_rp(ctx) and not ctx.team_stadium_detail.off:
        img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
        if image_match(img, REF_TEAM_STADIUM_OFF2).find_match:
            ctx.team_stadium_detail.off = True
            return
        ctx.ctrl.click_by_point(TO_TEAM_STADIUM)
    else:
        ctx.ctrl.click_by_point(GO_HOME_FROM_RACE)


def script_team_stadium_home(ctx: UmamusumeContext):
    if on_task(ctx) and not no_rp(ctx) and not ctx.team_stadium_detail.off:
        if parse_rp(ctx) < 2:
            set_no_rp(ctx)
        img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
        if image_match(img, REF_TEAM_STADIUM_OFF).find_match:
            ctx.team_stadium_detail.off = True
            return
        ctx.ctrl.click_by_point(TO_TEAM_RACE)
    else:
        ctx.ctrl.click_by_point(TEAM_STADIUM_RETURN)


def script_team_stadium_home_na(ctx: UmamusumeContext):
    ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.OFF)


def script_team_stadium_select_opponent(ctx: UmamusumeContext):
    match select_opponent(ctx):
        case 1:
            ctx.ctrl.click_by_point(TEAM_STADIUM_OPPO_UP)
        case 2:
            ctx.ctrl.click_by_point(TEAM_STADIUM_OPPO_MID)
        case 3:
            ctx.ctrl.click_by_point(TEAM_STADIUM_OPPO_DOWN)
        case 4:
            ctx.ctrl.click_by_point(TEAM_STADIUM_OPPO_REFRESH)


def script_team_stadium_before_race(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_CONTINUE)


def script_team_stadium_select_item(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_RACE)


def script_team_stadium_check_all_results(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_CHECK_RESULTS)


def script_team_stadium_check_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_SHORTEN)


def script_team_stadium_results(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_CONTINUE)


def script_team_stadium_reward(ctx: UmamusumeContext):
    ctx.team_stadium_detail.raced = True
    ctx.ctrl.click_by_point(TEAM_STADIUM_CLAIM_REWARDS)


def script_team_stadium_before_reward(ctx: UmamusumeContext):
    ctx.team_stadium_detail.raced = True
    ctx.ctrl.click_by_point(TEAM_STADIUM_CHECK_RESULTS)


def script_team_stadium_end(ctx: UmamusumeContext):
    ctx.team_stadium_detail.raced = True
    if no_rp(ctx):
        ctx.ctrl.click_by_point(TEAM_STADIUM_NEXT)
    else:
        ctx.ctrl.click_by_point(TEAM_STADIUM_RACE_AGAIN)


def script_team_stadium_no_rp(ctx: UmamusumeContext):
    set_no_rp(ctx)
    ctx.ctrl.click_by_point(TEAM_STADIUM_RP_CANCEL)


def script_team_stadium_high_score(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_CONTINUE)


def script_team_stadium_level_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TEAM_STADIUM_CONTINUE)


def no_rp(ctx: UmamusumeContext):
    if not (s := ctx.task.detail.timestamp['no_rp'].get(ctx.task.device_name or "default")):
        return False
    return datetime.datetime.now().timestamp() - s < NO_RP_RETRY_PENDING


def set_no_rp(ctx: UmamusumeContext):
    ctx.task.detail.timestamp['no_rp'][ctx.task.device_name or "default"] = datetime.datetime.now().timestamp()


def on_task(ctx: UmamusumeContext):
    return ctx.task.task_type == UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM


def parse_rp(ctx: UmamusumeContext) -> int:
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2RGB)
    base_x, base_y, inc, rp = 425, 66, 31, 5
    for i in range(5):
        if compare_color_equal(img[base_y, base_x], [81, 76, 89]):
            rp -= 1
        base_x += inc
    return rp
