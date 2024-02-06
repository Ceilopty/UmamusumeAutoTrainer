import cv2
from bot.recog.image_matcher import image_match
from bot.recog.ocr import ocr_line, find_similar_text
from module.umamusume.context import UmamusumeContext
from module.umamusume.asset.point import (UI_INFO,
                                          NETWORK_ERROR_CONFIRM,
                                          UNLOCK_STORY_TO_HOME_PAGE,
                                          UNLOCK_STORY_TO_HOME_PAGE2,
                                          ACTIVITY_STORY_UNLOCK_CONFIRM,
                                          ACTIVITY_STORY_UNLOCK_CONFIRM2,
                                          CLOSE_NEWS,
                                          RECEIVE_GIFT,
                                          RECEIVE_GIFT_SUCCESS_CLOSE,
                                          DATE_CHANGE_CONFIRM,
                                          CONNECTION_LOST_RESUME,
                                          )
import bot.base.log as logger

TITLE = {
    "网络错误": lambda ctx: ctx.ctrl.click_by_point(NETWORK_ERROR_CONFIRM),
    "解锁角色剧情":
        lambda ctx: ctx.ctrl.click_by_point(UNLOCK_STORY_TO_HOME_PAGE) or
        ctx.ctrl.click_by_point(UNLOCK_STORY_TO_HOME_PAGE2),
    "活动剧情解锁":
        lambda ctx: ctx.ctrl.click_by_point(ACTIVITY_STORY_UNLOCK_CONFIRM) or
        ctx.ctrl.click_by_point(ACTIVITY_STORY_UNLOCK_CONFIRM2),
    "公告": lambda ctx: ctx.ctrl.click_by_point(CLOSE_NEWS),
    "礼物箱": lambda ctx: ctx.ctrl.click_by_point(RECEIVE_GIFT),
    "领取成功": lambda ctx: ctx.ctrl.click_by_point(RECEIVE_GIFT_SUCCESS_CLOSE),
    "日期变化": lambda ctx: ctx.ctrl.click_by_point(DATE_CHANGE_CONFIRM),
    "连接已断开": lambda ctx: ctx.ctrl.click_by_point(CONNECTION_LOST_RESUME),
    "数据下载": lambda ctx: ctx.ctrl.click(520, 830, "数据下载确认"),
}


def common_script_info(ctx: UmamusumeContext, logger_name: str, *titles: dict):
    log = logger.get_logger(logger_name)
    title = TITLE.copy()
    for t in titles:
        title.update(t)
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    result = image_match(img, UI_INFO)
    if result.find_match:
        pos = result.matched_area
        title_img = img[pos[0][1] - 5:pos[1][1] + 5, pos[0][0] + 150: pos[1][0] + 405]
        title_text = ocr_line(title_img)
        log.debug(title_text)
        title_text = find_similar_text(title_text, title, 0.8)
        if title_text == "":
            log.warning("未知的选项框")
            return
        title[title_text](ctx)
