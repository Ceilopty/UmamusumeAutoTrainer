import datetime
import time

import croniter
import cv2

from bot.base.task import TaskStatus, EndTaskReason
from bot.recog.image_matcher import compare_color_equal, image_match
from module.umamusume.task import EndTaskReason as UEndTaskReason
from module.umamusume.context import UmamusumeContext, UmamusumeTaskType
from module.umamusume.asset.template import (REF_DAILY_RACE_MULTI_RACE_ON, REF_DAILY_RACE_MULTI_RACE_OFF,
                                             REF_DAILY_RACE_MOONLIGHT, REF_DAILY_RACE_JUPITER,
                                             REF_DAILY_RACE_EASY, REF_DAILY_RACE_NORMAL, REF_DAILY_RACE_HARD,
                                             )
from module.umamusume.asset.point import TO_RACE, GO_HOME_FROM_RACE
from ..common.common import on_task as _on_task


def dr_script_main_menu(ctx: UmamusumeContext):
    if ctx.daily_race_detail.raced:
        ctx.task.end_task(TaskStatus.TASK_STATUS_SUCCESS, EndTaskReason.COMPLETE)
    elif daily_raced(ctx):
        ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.DAILY_RACED)
    else:
        ctx.ctrl.click_by_point(TO_RACE)


def dr_script_race_home(ctx: UmamusumeContext):
    if daily_raced(ctx) or ctx.daily_race_detail.raced:
        ctx.ctrl.click_by_point(GO_HOME_FROM_RACE)
        return
    ctx.ctrl.click(200, 1050, "前往日常赛事")


def script_daily_race_dr_home(ctx: UmamusumeContext):
    if daily_raced(ctx) or ctx.daily_race_detail.raced:
        ctx.ctrl.click(80, 1080, "返回")
        return
    race = [REF_DAILY_RACE_MOONLIGHT, REF_DAILY_RACE_JUPITER][ctx.daily_race_detail.race]
    difficulty = [REF_DAILY_RACE_EASY, REF_DAILY_RACE_NORMAL, REF_DAILY_RACE_HARD][ctx.daily_race_detail.difficulty]
    retry = 3
    while retry := retry - 1:
        match_result = image_match(ctx.ctrl.get_screen(True), race)
        if match_result.find_match:
            ctx.ctrl.click(*match_result.center_point, "选择比赛")
            break
        match_result = image_match(ctx.ctrl.get_screen(True), difficulty)
        if match_result.find_match:
            ctx.ctrl.click(*match_result.center_point, "选择难度")
            break
        ctx.ctrl.swipe(360, 960, 360, 600, 500, "滑")
        time.sleep(0.5)
    time.sleep(0.5)


def script_daily_race_detail(ctx: UmamusumeContext):
    if daily_raced(ctx) or ctx.daily_race_detail.raced:
        ctx.ctrl.click(200, 1180, "取消")
        return
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, REF_DAILY_RACE_MULTI_RACE_OFF).find_match:
        ctx.ctrl.click(360, 1090, "多次参赛")
    if image_match(img, REF_DAILY_RACE_MULTI_RACE_ON).find_match:
        ctx.ctrl.click(500, 1180, "参赛！")


def script_daily_race_select_racer(ctx: UmamusumeContext):
    if daily_raced(ctx) or ctx.daily_race_detail.raced:
        ctx.ctrl.click(360, 1220, "回主页")
        return
    # 未触发限时特卖时有概率导致选择赛事和难度的页面左上确实选择参赛优骏少女，导致卡住。
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2RGB)
    if not compare_color_equal(img[1080, 360], [131, 208, 8]):
        ctx.ctrl.click(360, 1220, "回主页")
        return
    ctx.ctrl.click(360, 1080, "确认参赛选手")


def script_daily_race_multi_race(ctx: UmamusumeContext):
    ctx.ctrl.click(520, 830, "确认多次参赛")


def script_daily_race_result(ctx: UmamusumeContext):
    ctx.daily_race_detail.raced = True
    ctx.ctrl.click(360, 1180, "关闭参赛结果")
    time.sleep(2)


def script_daily_race_buy_ticket(ctx: UmamusumeContext):
    set_daily_raced(ctx)
    ctx.ctrl.click(200, 830, "放弃购买入场券")


def daily_raced(ctx: UmamusumeContext):
    if ts := ctx.task.detail.timestamp['daily_raced'].get(ctx.task.device_name or "default"):
        last = datetime.datetime.fromtimestamp(ts)
        refresh = croniter.croniter("0 5 * * *", last).get_next(datetime.datetime)
        return datetime.datetime.now() < refresh
    return False


def set_daily_raced(ctx: UmamusumeContext):
    ctx.task.detail.timestamp['daily_raced'][ctx.task.device_name or "default"] = datetime.datetime.now().timestamp()


def on_task(ctx: UmamusumeContext):
    return _on_task(ctx, UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DAILY_RACE)
