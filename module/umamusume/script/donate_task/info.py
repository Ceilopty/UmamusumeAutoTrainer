from .donate import (script_donate_requests,
                     script_donate_confirm,
                     script_donate_success,
                     )
from ..common.info import common_script_info

TITLE = {
    "道具捐赠请求": script_donate_requests,
    "捐赠确认": script_donate_confirm,
    "捐赠成功": script_donate_success,
    "一键捐赠确认": lambda ctx: ctx.ctrl.click(520, 1180, "进行一键捐赠"),
    "练习搭档分享": lambda ctx: ctx.ctrl.click(140, 1185, "取消分享"),
}


def d_script_info(ctx):
    return common_script_info(ctx, __name__, TITLE)
