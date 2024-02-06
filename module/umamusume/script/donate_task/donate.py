import datetime
import random
import re
import time

import croniter
import cv2
from bot.recog.ocr import ocr_line
from bot.recog.image_matcher import image_match, compare_color_equal
from bot.base.task import TaskStatus, EndTaskReason
from module.umamusume.task import EndTaskReason as UEndTaskReason
from module.umamusume.context import UmamusumeContext, UmamusumeTaskType
from module.umamusume.asset.template import (REF_DONATE_REQUESTS, REF_DONATE_ASKED, REF_DONATE_ASKED_CLOSED,
                                             REF_DONATE_ASKED_TIMEOUT, REF_DONATE_ASKED_INCOMPLETE, REF_DONATE_ASKING,
                                             REF_DONATE_ASK_CONFIRM, BTN_DONATE_AVAILABLE, REF_DONATE_PLUS_UNAVAILABLE,
                                             REF_DONATE_UNAVAILABLE)
from module.umamusume.asset.point import (DONATE_ASK_1, DONATE_ASK_2, DONATE_ASK_3, DONATE_ASK_4, DONATE_ASK_5,
                                          TO_GUILD, DONATE_TO_REQ_LIST, DONATE_TO_ASK, GO_HOME_FROM_GUILD,
                                          DONATE_COMMON_CONFIRM, DONATE_RETURN_FROM_REQ, DONATE_ASK_SELECTED,
                                          DONATE_ASK_CONFIRM, DONATE_AVAILABLE_OFFER, DONATE_OFFER_PLUS,
                                          DONATE_OFFER_CONFIRM)
from module.umamusume.script.common.common import on_task as _on_task, get_timestamp, set_timestamp

ASKED_PENDING = 3600 * 8
NO_MORE_REQUEST_PENDING = 600
MAX_SWIPE = 3

ASK_SHOES = [DONATE_ASK_1, DONATE_ASK_2, DONATE_ASK_3, DONATE_ASK_4, DONATE_ASK_5]


def d_script_main_menu(ctx: UmamusumeContext):
    if on_task(ctx):
        if not (donated(ctx) or no_more_request(ctx)) or not just_asked(ctx):
            ctx.ctrl.click_by_point(TO_GUILD)
        elif ctx.donate_detail.asked or ctx.donate_detail.donated:
            ctx.task.end_task(TaskStatus.TASK_STATUS_SUCCESS, EndTaskReason.COMPLETE)
        elif donated(ctx):
            ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.DONATED)
        else:
            ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.NO_REQUESTS)


def script_guild_home(ctx: UmamusumeContext):
    if on_task(ctx):
        if not donated(ctx) and not no_more_request(ctx):
            img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)  # [550:650, 1:100]
            if image_match(img, REF_DONATE_REQUESTS).find_match:
                ctx.ctrl.click_by_point(DONATE_TO_REQ_LIST)
                return
            else:
                set_timestamp(ctx, 'no_more_request')
        if not just_asked(ctx):
            ctx.ctrl.click_by_point(DONATE_TO_ASK)
            return
    ctx.ctrl.click_by_point(GO_HOME_FROM_GUILD)


def script_donate_requests(ctx: UmamusumeContext):
    """
    道具捐赠请求
    大部分东西都在这里
    分为：
    1、刚刚点进捐鞋列表的画面，寻找点亮的“捐赠”，点下去。若没有则往下滑。
      若有灰色“捐赠”，则今日捐满，若找不到亮“捐赠”，认为没有可捐的了。
    2、点捐赠请求（要鞋），如果显示捐鞋未满8小时，设置为7.5小时前“已要”。
    3、点捐赠请求（要鞋），如果达上限已结束，设置为7.5小时前“已要”。
    4、点捐赠请求（要鞋），如果显示时间已到，设置为8小时前“已要”。
    5、点捐赠请求（要鞋），如果显示剩余X小时，设置为X小时前“已要”。
    6、正常进入选鞋界面，底部应有“请选择需求道具”，根据任务设置点击。
    7、要鞋确认，底部会有“8小时内无法捐鞋”，点确定。
    2-7都有对应ref，处理完再搞1
    目前懒得做指定捐鞋，能捐统统捐
    """
    # 情况2：已要，已满
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, REF_DONATE_ASKED).find_match:
        set_timestamp(ctx, 'asked', -3600*7.5)
        ctx.ctrl.click_by_point(DONATE_COMMON_CONFIRM)
        return
    # 情况3：已要，刚满
    if image_match(img, REF_DONATE_ASKED_CLOSED).find_match:
        set_timestamp(ctx, 'asked', -3600*7.5)
        ctx.ctrl.click_by_point(DONATE_RETURN_FROM_REQ)
        return
    # 情况4：已要，超时
    if image_match(img, REF_DONATE_ASKED_TIMEOUT).find_match:
        set_timestamp(ctx, 'asked', -3600 * 8)
        ctx.ctrl.click_by_point(DONATE_RETURN_FROM_REQ)
        return
    # 情况4：已要，未满，解析剩余时间
    if image_match(img, REF_DONATE_ASKED_INCOMPLETE).find_match:
        offset = re.sub("\\D", "", ocr_line(img[1090:1120, 435:460]))
        offset = 3600*(int(offset)-8) if offset else None
        set_timestamp(ctx, 'asked', offset)
        ctx.ctrl.click_by_point(DONATE_RETURN_FROM_REQ)
        return
    # 情况5：选鞋 doublecheck
    if image_match(img, REF_DONATE_ASKING).find_match:
        index = ctx.donate_detail.ask_shoe_type or random.randint(1, 5)
        ctx.ctrl.click_by_point(ASK_SHOES[index - 1])
        time.sleep(0.5)
        ctx.ctrl.click_by_point(ASK_SHOES[index - 1])
        ctx.ctrl.click_by_point(DONATE_ASK_SELECTED)
        return
    # 情况6: 要鞋确认
    if image_match(img, REF_DONATE_ASK_CONFIRM).find_match:
        ctx.ctrl.click_by_point(DONATE_ASK_CONFIRM)
        ctx.donate_detail.asked = True
        set_timestamp(ctx, 'asked')
        return
    # 情况1-1：找亮鞋
    if image_match(img, BTN_DONATE_AVAILABLE).find_match:
        ctx.ctrl.click_by_point(DONATE_AVAILABLE_OFFER)
        return
    # 情况1-2 已捐  灰色已捐赠和黑色捐赠会相互干扰，匹配中心点<100认为是已捐赠，涂黑继续找。
    # 100-200之间认为是灰捐赠，表示今日捐满。
    while True:
        match_result = image_match(img, REF_DONATE_UNAVAILABLE)
        if match_result.find_match:
            pos = match_result.matched_area
            pos_center = match_result.center_point
            if img[pos_center[1], pos_center[0]] < 100:
                img[pos[0][1]:pos[1][1],
                    pos[0][0]:pos[1][0]] = 0
            else:
                set_timestamp(ctx, 'donated')
                ctx.ctrl.click_by_point(DONATE_RETURN_FROM_REQ)
                return
        else:
            break
    # 没找到，滑一下 不记得最开始往上滑还是往下滑了
    if ctx.donate_detail.swiped < MAX_SWIPE and (scroll := parse_scrollable(ctx)):
        if scroll == -1:
            ctx.ctrl.swipe(360, 800, 360, 400, 1000, "找可捐")
        else:
            ctx.ctrl.swipe(360, 400, 360, 800, 1000, "找可捐")
        ctx.donate_detail.swiped += 1
    else:
        set_timestamp(ctx, 'no_more_request')
        ctx.ctrl.click_by_point(DONATE_RETURN_FROM_REQ)


def script_donate_confirm(ctx: UmamusumeContext):
    """捐赠确认"""
    ctx.ctrl.click_by_point(DONATE_OFFER_PLUS)
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, REF_DONATE_PLUS_UNAVAILABLE).find_match:
        ctx.ctrl.click_by_point(DONATE_OFFER_CONFIRM)


def script_donate_success(ctx: UmamusumeContext):
    """捐赠成功"""
    ctx.ctrl.click_by_point(DONATE_COMMON_CONFIRM)
    ctx.donate_detail.donated = True


def donated(ctx: UmamusumeContext):
    if ts := get_timestamp(ctx, 'donated'):
        last = datetime.datetime.fromtimestamp(ts)
        refresh = croniter.croniter("0 5 * * *", last).get_next(datetime.datetime)
        return datetime.datetime.now() < refresh
    return False


def just_asked(ctx: UmamusumeContext):
    if ts := get_timestamp(ctx, 'asked'):
        return datetime.datetime.now().timestamp() - ts < ASKED_PENDING
    return False


def no_more_request(ctx: UmamusumeContext):
    if ts := get_timestamp(ctx, 'no_more_request'):
        return datetime.datetime.now().timestamp() - ts < NO_MORE_REQUEST_PENDING
    return False


def on_task(ctx: UmamusumeContext):
    return _on_task(ctx, UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DONATE)


def parse_scrollable(ctx: UmamusumeContext):
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2RGB)
    base_x, base_y_top, base_y_bot = 695, 115, 1105
    bright = [211, 209, 219]
    dark = [125, 120, 142]
    bg = [241, 241, 241]
    top, bottom = (list(compare_color_equal(img[base_y, base_x], target)
                        for target in (bright, dark, bg)
                        ) for base_y in (base_y_top, base_y_bot))
    match top, bottom:
        case (_, _, bool(x)), (_, _, bool(y)) if x or y:
            return 0
        case (True, False, False), (False, True, False):
            return 1  # 上浅下深，往下滑往前翻
        case (False, True, False), (True, False, False):
            return -1  # 上深下浅，往上滑往后翻
        case _:
            print(top, bottom)  # DEBUG
            print(list(img[base_y, base_x] for base_y in (base_y_top, base_y_bot)))
