import os.path
import time
import json

from .database import get_info_filepath
from module.umamusume.context import UmamusumeContext
import bot.base.log as logger

log = logger.get_logger(__name__)

TIMEOUT = 20


def ura_select_opponent(ctx: UmamusumeContext):
    try:
        if (now := time.time()) - (file := os.path.getmtime(get_info_filepath('S'))) > TIMEOUT:
            log.warning("超时, 当前时间：%s，文件时间：%s",
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file)))
            return
        time.sleep(3.5)
        with open(get_info_filepath('S'), 'rb') as f:
            ura_info = json.load(f)
    except FileNotFoundError:
        log.warning("未发现团队竞技场信息，使用原始方法。")
        return
    target = ctx.team_stadium_detail.opponent_index
    stamina = ctx.team_stadium_detail.opponent_stamina
    average = list(list(sum(x := list(chara[attr] for chara in opponent if chara))/len(x)
                        for attr in range(5)) for opponent in ura_info['attribute'])
    stamina_list = list(opponent[1] for opponent in average)
    if target == 0:
        if (min_stamina := min(stamina_list)) < stamina:
            opponent = stamina_list.index(min_stamina)
            log.info("抓到了位于%s，平均属性为：%s的速智哥！",
                     "上中下"[opponent], list(x//1 for x in average[opponent]))
            return opponent + 1
        return 4
    if stamina_list[target-1] < stamina:
        log.info("抓到了平均属性为：%s的速智哥！", list(x//1 for x in average[target-1]))
        return target
    return 4
