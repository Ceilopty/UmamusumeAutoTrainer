from module.umamusume.context import UmamusumeContext, SupportCardInfo
from module.umamusume.script.cultivate_task.parse import logger, parse_debut_race
from module.umamusume.define import SupportCardType, MotivationLevel
from .database import get_info_filepath, NameManager
from .database.define import CommandType
from .parse import TurnInfo
import json

log = logger.get_logger(__name__)


def ura_parse_cultivate_main_menu(ctx: UmamusumeContext, img):
    try:
        with open(get_info_filepath(), 'rb') as f:
            ura_info = TurnInfo(json.load(f))
    except FileNotFoundError:
        log.warning("未发现URA回合信息，使用原始方法。")
        return
    ctx_info = ctx.cultivate_detail.turn_info
    if convert_date(ura_date := ura_info.turn) != (uat_date := ctx_info.date):
        log.warning("日期匹配失败，UAT日期%s, URA日期%s, 请核对！", uat_date, ura_date)
        return
    command_array = ura_info.available_command_array
    if CommandType.Race in command_array:
        ctx_info.race_available = True
    if CommandType.Hoken in command_array:
        ctx_info.medic_room_available = True
    ctx.cultivate_detail.turn_info.remain_stamina = ura_info.vital
    (ctx_info.uma_attribute.speed,
     ctx_info.uma_attribute.stamina,
     ctx_info.uma_attribute.power,
     ctx_info.uma_attribute.will,
     ctx_info.uma_attribute.intelligence) = ura_info.fiveStatus
    ctx.cultivate_detail.turn_info.uma_attribute.skill_point = ura_info.skillPt
    ctx_info.motivation_level = MotivationLevel(ura_info.motivation)
    parse_debut_race(ctx, img)
    ctx.cultivate_detail.turn_info.parse_main_menu_finish = True
    ura_parse_training(ctx, ura_info)


def convert_date(ura_date: int) -> int:
    """
    将URA中的日期转换成UAT中的日期
    @param ura_date: URA中的turn（从0开始，第四年继续编号，即0-77）
    @return: UAT中的日期（从1开始，总决赛三个自由行动回合为97-99）
    @rtype: int
    @bug: UAT在URA总决赛决赛时被97捞走了，避免耽误时间这边妥协一下
    """
    # TODO UAT修复了日期识别bug的话去掉if
    if ura_date == 76:
        return 97
    return ura_date + 1 if ura_date < 72 else ura_date // 2 + 61


def convert_support_type(train_type: int) -> SupportCardType:
    """
    将URA生成的TurnInfo里的支援卡类型转换成UAT中的
    @param train_type: TurnInfo里persons里人头的trainType, 101-106没有104
    @return: UAT中支援卡类型SupportCardType
    @rtype: SupportCardType
    """
    _dict = {101: 1, 102: 3, 103: 4, 105: 2, 106: 5, 0: 6, -1: 0}
    return SupportCardType(_dict[train_type])


def ura_parse_training(ctx: UmamusumeContext, info: TurnInfo):
    training_info_list = ctx.cultivate_detail.turn_info.training_info_list
    for train, value in enumerate(info.trainValue):
        (training_info_list[train].speed_incr,
         training_info_list[train].stamina_incr,
         training_info_list[train].power_incr,
         training_info_list[train].will_incr,
         training_info_list[train].intelligence_incr,
         training_info_list[train].skill_point_incr,
         training_info_list[train].vital_incr) = value
    else:
        ura_parse_support_card(ctx, info)
        ctx.cultivate_detail.turn_info.parse_train_info_finish = True


def ura_parse_support_card(ctx: UmamusumeContext, info: TurnInfo):
    for train, distribution in enumerate(info.personDistribution):
        for person in distribution:
            if person == -1:
                break
            sc = info.persons[person]
            sid = info.cardId[sc.cardIdInGame] // 10  # 凸是%10
            scn = NameManager.get_support(sid) if NameManager else None
            sci = SupportCardInfo(card_type=convert_support_type(sc.trainType),
                                  favor_num=sc.friendship,
                                  has_event=sc.isHint,
                                  name=("%s %s" % (scn.name, scn.nickname)) if NameManager else "support card")
            ctx.cultivate_detail.turn_info.training_info_list[train].support_card_info_list.append(sci)
