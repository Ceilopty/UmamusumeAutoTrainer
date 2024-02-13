import os.path
import time

from module.umamusume.context import UmamusumeContext, Condition, SupportCardInfo, LearntSkill, SkillHint
from module.umamusume.script.cultivate_task.parse import logger, parse_debut_race
from module.umamusume.define import SupportCardType, MotivationLevel
from module.umamusume.script.cultivate_task.event.event_ai import score_context, context_plus_effect, context_copy
from .database import get_info_filepath, DataBase
from .database.define import CommandType
from .parse import TurnInfo, EventInfo, UraPerson, UraPersonType
from .event_logger import EventLogger
import json

log = logger.get_logger(__name__)

TIMEOUT = 60


def ura_parse_cultivate_main_menu(ctx: UmamusumeContext, img=None):
    try:
        if (now := time.time()) - (file := os.path.getmtime(get_info_filepath())) > TIMEOUT:
            log.warning("超时, 当前时间：%s，文件时间：%s",
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file)))
            return
        with open(get_info_filepath(), 'rb') as f:
            ura_info = TurnInfo(json.load(f))
    except FileNotFoundError:
        log.warning("未发现URA回合信息，使用原始方法。")
        return
    ctx_info = ctx.cultivate_detail.turn_info
    if convert_date(ura_date := ura_info.turn) != (uat_date := ctx_info.date):
        log.warning("日期匹配失败，UAT日期%s, URA日期%s, 请核对！", uat_date, ura_date)
        # return  # 一般还是URA准确，所以继续
        ctx_info.date = convert_date(ura_date)
    ctx.cultivate_detail.uma_rarity, ctx.cultivate_detail.uma_id = divmod(ura_info.umaId, 1000000)
    ctx.cultivate_detail.card_id_list[:] = ura_info.cardId  # 前五位id，最后一位凸数
    ctx.cultivate_detail.talent_level = ura_info.talent_level
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
    ctx_info.uma_condition_list[:] = map(Condition, ura_info.chara_effect_id_array)
    ctx_info.max_vital = ura_info.maxVital
    ctx_info.uma_attribute_limit_list[:] = ura_info.fiveStatusLimit
    ctx_info.proper_info[:] = ura_info.proper_info
    ctx_info.parse_main_menu_finish = True
    ura_parse_person_list(ctx, ura_info)
    ura_parse_training(ctx, ura_info)
    ura_parse_skills(ctx, ura_info)
    ura_parse_ura_info(ctx, ura_info)
    # 检查是否需要log event effect
    EventLogger.view(ctx)


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
        return DataBase.get_chara_by_id(sid).name if DataBase else "support card"
    sc = DataBase.get_support_by_id(sid) if DataBase else None
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
            sc = ctx.cultivate_detail.turn_info.person_list[card]
            person = info.persons[card]
            sc.has_event = person.isHint
            sc.favor_num = person.friendship
            ctx.cultivate_detail.turn_info.training_info_list[train].support_card_info_list.append(sc)


def ura_parse_skills(ctx: UmamusumeContext, info: TurnInfo):
    learnt_skill_list = []
    skill_hint_list = []
    for skill in info.skills:
        skill_id = skill.skill_id
        learnt = LearntSkill()
        learnt.name = get_skill_name_by_id(skill_id)
        learnt.level = skill.level
        learnt.is_inherent = skill_id < 200000 or skill_id > 900000
        learnt.skill_id = skill_id
        learnt_skill_list.append(learnt)
    for tip in info.skillTips:
        hint = SkillHint()
        hint.group_id = tip.group_id
        hint.level = tip.level
        hint.rarity = tip.rarity
        hint.name = get_hint_name_by_id_and_rarity(hint.group_id, hint.rarity)
        skill_hint_list.append(hint)
    ctx.cultivate_detail.turn_info.learnt_skill_list[:] = learnt_skill_list
    ctx.cultivate_detail.turn_info.skill_hint_list[:] = skill_hint_list
    ctx.cultivate_detail.turn_info.disable_skill_id_array[:] = info.disable_skill_id_array

    before_race_learnt = True
    for need_learn in (DataBase.get_skill_by_name(need_learn)
                       for level in ctx.cultivate_detail.learn_skill_list[0:1]
                       for need_learn in level):
        if (need_learn is not None and
           [x for x in skill_hint_list if x.group_id == need_learn.group_id and x.rarity == need_learn.rarity] and
           not [x for x in learnt_skill_list if x.skill_id == need_learn.id]):
            before_race_learnt = False
            break
    ctx.cultivate_detail.learn_skill_before_race_done = before_race_learnt


def get_skill_name_by_id(skill_id):
    return DataBase.get_skill_by_id(skill_id).name if DataBase else ""


def get_hint_name_by_id_and_rarity(group_id, rarity):
    if not DataBase:
        return ""
    group = DataBase.get_skill_group_by_id_and_rarity(group_id, rarity)
    if not group:
        return ""
    for skill in group:
        if skill.name[-1] in "×○◎":
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


def ura_parse_person_list(ctx: UmamusumeContext, info: TurnInfo):
    for person in info.persons:
        if not person.personType.value:
            ctx.cultivate_detail.turn_info.person_list.append(SupportCardInfo())
            continue
        ctx.cultivate_detail.turn_info.person_list.append(
            SupportCardInfo(card_type=convert_support_type(person),
                            favor_num=person.friendship,
                            has_event=person.isHint,
                            name=get_name_from_person_and_ids(person, info.cardId)))


def ura_get_event_choice_by_effect(ctx: UmamusumeContext) -> int:
    try:
        if (now := time.time()) - (file := os.path.getmtime(get_info_filepath('E'))) > TIMEOUT:
            log.warning("超时, 当前时间：%s，文件时间：%s",
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file)))
            return 0
        with open(get_info_filepath('E'), 'rb') as f:
            info = EventInfo(json.load(f))
    except FileNotFoundError:
        log.warning("未发现URA事件信息，使用原始方法。")
        return 0
    if info.story_id % 1000 == 720:
        if ctx.cultivate_detail.sasami:
            log.info("刺刺美事件确认确认")
            return 1
        ctx.cultivate_detail.sasami = True
    ctx = context_copy(ctx)
    ura_parse_basic_information(ctx)  # 更新当前信息
    # 有些成功事件URA里没记录，干脆还是在UAT维护方便
    if DataBase:
        if info.story_id in DataBase.success_events:
            from .parse.define import EventState
            from .parse.event_effect import EventEffects
            for i, choice in enumerate(DataBase.success_events[info.story_id]["Choices"]):
                for select_index in choice:
                    if info.select_indices[i] == select_index["SelectIndex"]:
                        info.effect[i] = EventEffects(select_index["Effect"])
                        info.is_success[i] = EventState(select_index["State"])
                        break
    ura_log_event_effect(info)
    origin_ctx = ctx
    ctx.cultivate_detail.turn_info.log_turn_info(False)
    log.debug("计算初始得分：", )
    standard = score_context(ctx)
    score_of_choices = []
    for c, effects_of_choice in enumerate(info.effect):
        score_of_possible_effect = []
        log.debug("选项%d，效果%s：", c + 1, effects_of_choice)
        for p, possible in enumerate(effects_of_choice.all_effects):
            ctx = context_copy(origin_ctx)
            for effect in possible:
                ctx = context_plus_effect(ctx, effect)
            if len(effects_of_choice.all_effects) > 1:
                log.debug("其中，可能性%d：", p + 1)
            score_of_possible_effect.append(score_context(ctx) - standard)
        if score_of_possible_effect:
            score_of_choices.append(sum(score_of_possible_effect) / len(score_of_possible_effect))
            log.debug("本选项额外得分：%.2f", score_of_choices[-1])
        else:
            score_of_choices.append(0)
            log.warning("未发现效果 %s", effects_of_choice)
    max_score = max(score_of_choices)
    if score_of_choices.count(max_score) > 1:
        log.warning("有多项得分相同")
    choice_indices = [index for index, score in enumerate(score_of_choices) if score == max_score]
    log.info("最佳选项及效果为: %s",
             " ".join(f"{info.choices[index]}: {info.effect[index]}" for index in choice_indices))
    # 贪一点，如果能测试未知事件就搞一下
    for c in choice_indices:
        if len(info.effect[c].all_effects) > 1:
            EventLogger.start(origin_ctx, info.triggerName, info.eventName, info.story_id, c, info.choices[c],
                              info.select_indices[c], info.is_success[c].value, info.effect[c], len(info.choices))
            return c + 1
    else:
        return choice_indices[0] + 1


def ura_log_event_effect(info: EventInfo):
    name = DataBase.get_event_name_by_id(info.story_id) or info.eventName
    log.info("找到事件%s from %s @%s", name, info.triggerName, info.story_id)
    for index, effect in enumerate(info.effect):
        log.info("选项%d：%s, 效果：%s", index + 1, info.choices[index], effect)


def ura_parse_basic_information(ctx: UmamusumeContext):
    """遇到事件或学技能时更新下基础信息"""
    try:
        with open(get_info_filepath(), 'rb') as f:
            ura_info = TurnInfo(json.load(f))
    except FileNotFoundError:
        log.warning("未发现URA回合信息，无法更新。")
        return
    ctx_info = ctx.cultivate_detail.turn_info

    ctx.cultivate_detail.uma_rarity, ctx.cultivate_detail.uma_id = divmod(ura_info.umaId, 1000000)
    ctx.cultivate_detail.card_id_list[:] = ura_info.cardId  # 前五位id，最后一位凸数
    ctx.cultivate_detail.talent_level = ura_info.talent_level
    ctx_info.remain_stamina = ura_info.vital
    (ctx_info.uma_attribute.speed,
     ctx_info.uma_attribute.stamina,
     ctx_info.uma_attribute.power,
     ctx_info.uma_attribute.will,
     ctx_info.uma_attribute.intelligence) = ura_info.fiveStatus
    ctx_info.uma_attribute.skill_point = ura_info.skillPt
    ctx_info.motivation_level = MotivationLevel(ura_info.motivation)
    ctx_info.uma_condition_list[:] = map(Condition, ura_info.chara_effect_id_array)
    ctx_info.max_vital = ura_info.maxVital
    ctx_info.uma_attribute_limit_list[:] = ura_info.fiveStatusLimit
    ctx_info.proper_info[:] = ura_info.proper_info
    ura_parse_skills(ctx, ura_info)
    ura_parse_person_list(ctx, ura_info)
    EventLogger.view(ctx)
