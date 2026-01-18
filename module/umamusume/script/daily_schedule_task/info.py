from .race import (script_daily_race_detail,
                   script_daily_race_multi_race,
                   script_daily_race_result,
                   script_daily_race_buy_ticket,
                   )
from ..common.info import common_script_info
from ..time_sale.info import TITLE as TS_TITLE

TITLE = {
    "赛事详情": script_daily_race_detail,
    "一键参赛": script_daily_race_multi_race,
    "参赛结果": script_daily_race_result,
    "购买日常赛事入场券": script_daily_race_buy_ticket,
}


def dr_script_info(ctx):
    return common_script_info(ctx, __name__, TITLE, TS_TITLE)
