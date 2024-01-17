from module.umamusume.context import UmamusumeContext, SupportCardInfo, LearntSkill, SkillHint
from module.umamusume.script.cultivate_task.parse import logger, parse_debut_race
from module.umamusume.define import SupportCardType, MotivationLevel
from module.umamusume.script.cultivate_task.event.event_ai import score_context, context_plus_effect, context_copy
from .database import get_info_filepath, NAME_MANAGER
from .database.define import CommandType
from .parse import TurnInfo, EventInfo, UraPerson, UraPersonType
from .parse.event_effect import EventEffect
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
        # return  # 一般还是URA准确，所以继续
    command_array = ura_info.available_command_array
    if CommandType.Race in command_array:
        ctx_info.race_available = True
    if CommandType.Hoken in command_array:
        ctx_info.medic_room_available = True
    if CommandType.River in command_array:
        ctx_info.out_destination = 1
    if CommandType.Karaoke in command_array:
        ctx_info.out_destination = 2
    if CommandType.Jinja in command_array:
        ctx_info.out_destination = 3
    if CommandType.Sea in command_array:
        ctx_info.out_destination = 4
    ctx_info.remain_stamina = ura_info.vital
    (ctx_info.uma_attribute.speed,
     ctx_info.uma_attribute.stamina,
     ctx_info.uma_attribute.power,
     ctx_info.uma_attribute.will,
     ctx_info.uma_attribute.intelligence) = ura_info.fiveStatus
    ctx_info.uma_attribute.skill_point = ura_info.skillPt
    ctx_info.motivation_level = MotivationLevel(ura_info.motivation)
    parse_debut_race(ctx, img)
    ctx_info.uma_condition_list[:] = ura_info.chara_effect_id_array
    ctx_info.max_vital = ura_info.maxVital
    ctx_info.uma_attribute_limit_list[:] = ura_info.fiveStatusLimit
    ctx_info.parse_main_menu_finish = True
    ura_parse_training(ctx, ura_info)
    ura_parse_skills(ctx, ura_info)
    ura_parse_ura_info(ctx, ura_info)


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


def convert_support_type(person: UraPerson) -> SupportCardType:
    """
    将URA生成的TurnInfo里的人头类型转换成UAT中的支援卡类型
    包含传统的速耐力根智，友团（URA的URA举剧本还没搞）以及NPC
    @param person: TurnInfo里persons里的人头UraPerson，
    其trainType, 101-106没有104
    @return: UAT中支援卡类型SupportCardType
    @rtype: SupportCardType
    """
    _dict = {101: 1, 102: 3, 103: 4, 105: 2, 106: 5, 0: 6, -1: 0}
    match person.personType:
        case UraPersonType.Normal:
            return SupportCardType(_dict[person.trainType])
        case UraPersonType.Akikawa | UraPersonType.Otonashi | UraPersonType.Kiryuuin:
            return SupportCardType.SUPPORT_CARD_TYPE_NPC
        case UraPersonType.HayakawaS | UraPersonType.KiryuuinS:
            return SupportCardType.SUPPORT_CARD_TYPE_FRIEND
        case UraPersonType.Unknown | _:
            return SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN


def get_name_from_person_and_ids(person: UraPerson, card_ids: list[int]) -> str:
    if person.cardIdInGame == -1:  # NPC,
        sid = {1: 9004, 3: 9001, 4: 9002, 5: 9003, 6: 9004}[person.personType.value]
    else:
        sid = card_ids[person.cardIdInGame] // 10  # Id是 // 10，凸是 % 10
    if sid < 10000:
        return NAME_MANAGER.get_chara_by_id(sid).name if NAME_MANAGER else "support card"
    sc = NAME_MANAGER.get_support_by_id(sid) if NAME_MANAGER else None
    return "%s %s" % (sc.name, sc.chara.name) if sc else "support card"


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
        training_info_list[train].failure_rate = info.failRate[train]
    else:
        ctx.cultivate_detail.turn_info.train_level_count_list[:] = info.trainLevelCount[:]
        ura_parse_support_card(ctx, info)
        ctx.cultivate_detail.turn_info.parse_train_info_finish = True


def ura_parse_support_card(ctx: UmamusumeContext, info: TurnInfo):
    for train, distribution in enumerate(info.personDistribution):
        for card in distribution:
            if card == -1:
                break
            person = info.persons[card]
            sci = SupportCardInfo(card_type=convert_support_type(person),
                                  favor_num=person.friendship,
                                  has_event=person.isHint,
                                  name=get_name_from_person_and_ids(person, info.cardId))
            ctx.cultivate_detail.turn_info.training_info_list[train].support_card_info_list.append(sci)


def ura_parse_skills(ctx: UmamusumeContext, info: TurnInfo):
    for skill in info.skills:
        skill_id = skill.skill_id
        learnt = LearntSkill()
        learnt.name = get_skill_name_by_id(skill_id)
        learnt.level = skill.level
        learnt.is_inherent = skill_id < 200000 or skill_id > 900000
        learnt.skill_id = skill_id
        ctx.cultivate_detail.turn_info.learnt_skill_list.append(learnt)
    for tip in info.skillTips:
        hint = SkillHint()
        hint.group_id = tip.group_id
        hint.level = tip.level
        hint.rarity = tip.rarity
        hint.name = get_hint_name_by_id_and_rarity(hint.group_id, hint.rarity)
        ctx.cultivate_detail.turn_info.skill_hint_list.append(hint)


def get_skill_name_by_id(skill_id):
    return NAME_MANAGER.get_skill_by_id(skill_id).name if NAME_MANAGER else ""


def get_hint_name_by_id_and_rarity(group_id, rarity):
    group = NAME_MANAGER.get_skill_group_by_id_and_rarity(group_id, rarity)
    if not group:
        return ""
    for skill in group:
        if skill.name.endswith("◎"):
            return skill.name[:-1]
    return " ".join(skill.name for skill in group)


def ura_parse_ura_info(ctx: UmamusumeContext, info: TurnInfo):
    ura_info = ctx.cultivate_detail.turn_info.ura_info
    ura_info.ura_tsyInfo.first_click = info.ura_tsyFirstClick
    ura_info.ura_tsyInfo.outgoing_unlocked = info.ura_tsyOutgoingUnlocked
    ura_info.ura_tsyInfo.outgoing_refused = info.ura_tsyOutgoingRefused
    ura_info.ura_tsyInfo.outgoing_used = info.ura_tsyOutgoingUsed
    ura_info.ura_lmInfo.first_click = info.ura_lmFirstClick
    ura_info.ura_lmInfo.outgoing_unlocked = info.ura_lmOutgoingUnlocked
    ura_info.ura_lmInfo.outgoing_refused = info.ura_lmOutgoingRefused
    ura_info.ura_lmInfo.outgoing_used = info.ura_lmOutgoingUsed


def ura_get_event_choice_by_effect(ctx: UmamusumeContext) -> int:
    try:
        with open(get_info_filepath('E'), 'rb') as f:
            info = EventInfo(json.load(f))
    except FileNotFoundError:
        log.warning("未发现URA事件信息，使用原始方法。")
        return 0
    ura_log_event_effect(info)
    origin_ctx = ctx
    score_of_choices = []
    for effects_of_choice in info.effect:
        score_of_possible_effect = []
        for possible in effects_of_choice.all_effects:
            ctx = context_copy(origin_ctx)
            for effect in possible:
                ctx = context_plus_effect(ctx, effect)
            score_of_possible_effect.append(score_context(ctx))
        if score_of_possible_effect:
            score_of_choices.append(sum(score_of_possible_effect) / len(score_of_possible_effect))
            log.debug("本选项得分：%s", score_of_choices[-1])
        else:
            log.warning("未发现效果 %s", effects_of_choice)
    max_score = max(score_of_choices)
    num = score_of_choices.count(max_score)
    if max_score == 0 or num == len(score_of_choices):
        log.warning("无效， 退回原始方法")
        return 0
    if num > 1:
        log.warning("未发现区别")
    choice_indices = [index for index, score in enumerate(score_of_choices) if score == max_score]
    log.info("最佳效果为: %s", " ".join(f"{info.choices[index]}: {info.effect[index]}" for index in choice_indices))
    return score_of_choices.index(max_score) + 1


def ura_log_event_effect(info: EventInfo):
    name = NAME_MANAGER.get_event_name_by_id(info.story_id) or info.eventName
    log.info("找到事件%s from %s @%s", name, info.triggerName, info.story_id)
    for index, effect in enumerate(info.effect):
        log.debug("选项%d：%s, 效果：%s", index, info.choices[index], effect)
