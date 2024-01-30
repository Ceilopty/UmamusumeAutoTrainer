"""
评价事件效果
最终应该按照预期养成结果计算。
现在先独立计算，以后再改造。
"""
from typing import Iterable
import bot.base.log as logger
from module.umamusume.context import (UmamusumeContext, TurnInfo, SkillHint, LearntSkill)
from module.umamusume.define import *
from module.umamusume.script.cultivate_task.event.parse import EventEffect

log = logger.get_logger(__name__)

# 以下Basic point的拍脑门依据为：
# 一级训练的体力消耗分别为21，19，20，22，-5
# 一回合等效50体力，7回合等效5次训练，不考虑协各种加成，1次训练的属性提升量与70体力评分应相近。
# 最后最后一回合体力没意义，倒数第二回合超过50以上的体力没意义，未超过的意义也不大，合宿前尽量高体力
# 干劲作为独立乘区，考虑边际效果，其得分应与羁绊正相关，与剩余回合数正相关，与训练等级正相关。
# 按医务室80%成功率计算，恶性不良状态约需花费1.25回合治疗，其他状态拍脑门赋值。
# 羁绊就是个彩头，合宿前如果能变彩的话给个高分

ATTRIBUTE_PREFERENCE = (1.0, 0.9, 0.8, 0.2, 0.3, 0.1)
ATTRIBUTE_BASIC_POINT = 2.0
MOTIVATION_BASIC = 100.0
VITAL_BASIC_POINT = 100.0
MAX_VITAL_BASIC_POINT = 1.0
CONDITION_BASIC_POINT = 60.0
SKILL_BASIC_POINT = 10.0
HINT_BASIC_POINT = 10.0
FAVOR_BASIC_POINT = 1.0


def _hp(ctx: UmamusumeContext) -> float:
    """
    体力得分
    参考URA四段折线，
    """

    def score_of_vital(_vital, _max_vital):
        """URA四段折线，初始满体力为2.5*50+1.7*25+1.2*15+0.7*10=192.5"""
        if _vital <= 50:
            return 2.5 * _vital
        elif _vital <= 75:
            return 1.7 * (_vital - 50) + score_of_vital(50, _max_vital)
        elif _vital <= _max_vital - 10:
            return 1.2 * (_vital - 75) + score_of_vital(75, _max_vital)
        else:
            return 0.7 * (_vital - (_max_vital - 10)) + score_of_vital(_max_vital - 10, _max_vital)

    date = ctx.cultivate_detail.turn_info.date
    vital = ctx.cultivate_detail.turn_info.remain_stamina
    max_vital = ctx.cultivate_detail.turn_info.max_vital

    if _is_gasshuku(ctx, date, 1):
        date_coefficient = 2
    elif date in _valid_date_list(ctx)[-1:]:
        date_coefficient = 0
    elif date in _valid_date_list(ctx)[-3:]:
        date_coefficient = 0.2
    else:
        date_coefficient = 1

    vital = date_coefficient * score_of_vital(vital, max_vital) / score_of_vital(max_vital, max_vital)

    return vital * VITAL_BASIC_POINT + max_vital * MAX_VITAL_BASIC_POINT


def _condition(ctx: UmamusumeContext) -> float:
    _ = {1: '夜ふかし気味', 2: 'なまけ癖', 3: '肌あれ', 4: '太り気味',
         5: '片頭痛', 6: '練習ベタ', 7: '切れ者', 8: '愛嬌◯', 9: '注目株',
         10: '練習上手◯', 11: '練習上手◎', 12: '小さなほころび',
         13: '大輪の輝き', 14: 'ファンとの約束・北海道', 15: 'ファンとの約束・北東',
         16: 'ファンとの約束・中山', 17: 'ファンとの約束・関西',
         18: 'ファンとの約束・小倉', 19: 'まだまだ準備中', 20: 'ガラスの脚',
         21: '怪しい雲行き', 22: 'ファンとの約束・川崎', 23: '英雄の光輝',
         24: '春待つ蕾', 25: 'ポジティブ思考', 26: '幸運体質', 100: "情熱ゾーン"}
    score = {1: -0.5, 2: -100, 3: -0.5, 4: -1,
             5: -1, 6: -0.5, 7: 0.8, 8: 2, 9: 0.5,
             10: 0.1, 11: 0.2, 12: 0,
             13: 0, 14: 0, 15: 0,
             16: 0, 17: 0,
             18: 0, 19: 0, 20: 0,
             21: 0, 22: 0, 23: 0,
             24: 0, 25: 0.5, 26: 0.5, 100: 0}
    date = 1 - ctx.cultivate_detail.turn_info.date / 100
    return CONDITION_BASIC_POINT * sum(score[x.value] for x in ctx.cultivate_detail.turn_info.uma_condition_list) * date


def _motivation(ctx: UmamusumeContext) -> float:
    """
    独立计算就是拍脑门
    姑且按集训重要，越后期越重要？，临近末期又边际递减的原则
    """
    date = ctx.cultivate_detail.turn_info.date
    level = ctx.cultivate_detail.turn_info.motivation_level.value
    if _is_gasshuku(ctx, date, 1):  # 下回合是合宿
        coefficient = 2
    elif date > 96:  # 决赛
        coefficient = (100 - date) / 5
    elif date == 29:  # 经三上，固定加一格。古四上太复杂不搞了
        coefficient = 1
        level = min(level + 1, 5)
    else:
        coefficient = 1
    now = ctx.cultivate_detail.turn_info.uma_attribute.to_tuple()
    expect = ctx.cultivate_detail.expect_attribute
    process = sum(now[i] / expect[i] * ATTRIBUTE_PREFERENCE[i] for i in range(5)) / sum(ATTRIBUTE_PREFERENCE)
    return (level - 3) * coefficient * process * MOTIVATION_BASIC


def _is_gasshuku(ctx: UmamusumeContext, date: int, offset: int = 0) -> bool:
    date_to_check = _date_offset(ctx, date, offset)
    return 36 < date_to_check <= 40 or 60 < date_to_check <= 64


def _favor(ctx: UmamusumeContext) -> float:
    date = ctx.cultivate_detail.turn_info.date
    days = len([_date for _date in _valid_date_list(ctx) if _date not in _race_dates(ctx) and _date > date])
    if _is_gasshuku(ctx, date, 1):  # 下回合是合宿
        coefficient = 2
    else:
        coefficient = 1
    favor = 0
    for person in ctx.cultivate_detail.turn_info.person_list:
        if not person.card_type.value:
            continue
        match person.favor.value:
            case 1:
                favor += 0.3 * person.favor_num / 100
            case 2:
                if person.card_type.value > 5:
                    favor += 0.8
                else:
                    favor += 0.5 * person.favor_num / 100 - 0.16
            case 3 | 4:
                favor += 1
    return favor * coefficient * days / 50 * FAVOR_BASIC_POINT


def _skill(ctx: UmamusumeContext) -> float:
    hint_score = 0
    skill_score = 0
    prefer_list_list = ctx.cultivate_detail.learn_skill_list
    for hint in ctx.cultivate_detail.turn_info.skill_hint_list:
        for level, prefer_list in enumerate(prefer_list_list):
            if hint.name in prefer_list or hint.name[:-1] in prefer_list:
                hint_score += (10 - level) / 10 * (hint.level + 5) / 10
                break
        hint_score += (10 - 9) / 10 * (hint.level + 5) / 10
    for learnt in ctx.cultivate_detail.turn_info.learnt_skill_list:
        for level, prefer_list in enumerate(prefer_list_list):
            if learnt.name in prefer_list or learnt.name[:-1] in prefer_list:
                skill_score += (10 - level) / 10
                break
        skill_score += (10 - 9) / 10
    skill_point_score = ctx.cultivate_detail.turn_info.uma_attribute.skill_point * ATTRIBUTE_PREFERENCE[5]
    return hint_score * HINT_BASIC_POINT + skill_score * SKILL_BASIC_POINT + skill_point_score * ATTRIBUTE_BASIC_POINT


def _attribute(ctx: UmamusumeContext) -> float:
    """缺口越大越需要"""
    current = ctx.cultivate_detail.turn_info.uma_attribute.to_tuple()
    expect = ctx.cultivate_detail.expect_attribute
    return sum(current[i] * (1 + (short if (short := expect[i] - current[i]) > 0 else 0) / expect[i])
               * ATTRIBUTE_PREFERENCE[i] for i in range(5)
               ) / sum(ATTRIBUTE_PREFERENCE) * ATTRIBUTE_BASIC_POINT


def _valid_date_list(ctx: UmamusumeContext) -> list[int]:
    if not hasattr(ctx.task.detail, "scenario_name") or ctx.task.detail.scenario_name == '1' \
            or ctx.task.detail.scenario_name == 1 or not ctx.task.detail.scenario_name:
        valid_dates = list(range(1, 73))
        valid_dates.extend((97, 98, 99))
    else:
        print("valid_date use origin")
        valid_dates = list(range(1, 73))
    return valid_dates


def _date_offset(ctx: UmamusumeContext, date: int, offset: int = 0) -> int:
    """计算跳过额外赛事后指定偏移量的日期"""
    if date < 1:
        return -1
    valid_dates = _valid_date_list(ctx)
    # valid_dates_without_race = sorted(list(set(valid_dates).difference(set(_race_dates(ctx)))))
    valid_dates_without_race = [_date for _date in valid_dates if _date not in _race_dates(ctx)]
    if date not in valid_dates_without_race:
        return _date_offset(ctx, date - 1, offset)
    res = valid_dates_without_race[valid_dates_without_race.index(date) + offset]
    if res not in valid_dates:
        return 0
    return res


def _race_dates(ctx: UmamusumeContext) -> list:
    return [race // 100 for race in ctx.cultivate_detail.extra_race_list]


def context_copy(origin_ctx: UmamusumeContext) -> UmamusumeContext:
    from copy import copy, deepcopy, Error
    ctx = UmamusumeContext(origin_ctx.task, origin_ctx.ctrl)
    try:
        ctx.cultivate_detail = deepcopy(origin_ctx.cultivate_detail)
    except Error:
        ctx = copy(ctx)
    return ctx


def context_plus_effect(ctx: UmamusumeContext, effect: EventEffect) -> UmamusumeContext:
    info = ctx.cultivate_detail.turn_info
    _add_vital(info, effect)
    _add_motivation(info, effect)
    _add_limit(info, effect)
    _add_attribute(info, effect)
    _add_last_train(info, effect)
    _add_condition(info, effect)
    _add_skill(info, effect)
    _add_hint(info, effect)
    _add_favor(info, effect)
    return ctx


def _add_motivation(info: TurnInfo, effect: EventEffect) -> None:
    level = info.motivation_level.value + effect.motivation
    level = max(1, level)
    level = min(5, level)
    info.motivation_level = MotivationLevel(level)


def _add_vital(info: TurnInfo, effect: EventEffect) -> None:
    info.max_vital += effect.max_vital
    info.remain_stamina += effect.vital
    info.remain_stamina = min(info.remain_stamina, info.max_vital)
    info.remain_stamina = max(info.remain_stamina, 0)


def _add_attribute(info: TurnInfo, effect: EventEffect) -> None:
    random_incr_average = effect.random_attr[0] * effect.random_attr[1] / 5
    info.uma_attribute.speed += effect.speed_incr + random_incr_average
    info.uma_attribute.stamina += effect.stamina_incr + random_incr_average
    info.uma_attribute.power += effect.power_incr + random_incr_average
    info.uma_attribute.will += effect.guts_incr + random_incr_average
    info.uma_attribute.intelligence += effect.wiz_incr + random_incr_average
    info.uma_attribute.skill_point += effect.skill_point_incr
    info.uma_attribute.speed = min(info.uma_attribute_limit_list[0], info.uma_attribute.speed)
    info.uma_attribute.stamina = min(info.uma_attribute_limit_list[1], info.uma_attribute.stamina)
    info.uma_attribute.power = min(info.uma_attribute_limit_list[2], info.uma_attribute.power)
    info.uma_attribute.will = min(info.uma_attribute_limit_list[3], info.uma_attribute.will)
    info.uma_attribute.intelligence = min(info.uma_attribute_limit_list[4], info.uma_attribute.intelligence)


def _add_limit(info: TurnInfo, effect: EventEffect) -> None:
    limit_incr = (effect.speed_limit_incr, effect.stamina_limit_incr, effect.power_limit_incr,
                  effect.guts_limit_incr, effect.wiz_limit_incr)
    info.uma_attribute_limit_list[:] = [info.uma_attribute_limit_list[i] +
                                        limit_incr[i] for i in range(5)]


def _add_hint(info: TurnInfo, effect: EventEffect) -> None:
    hints = info.skill_hint_list
    skill, level = effect.skill_hint
    if not skill:
        return
    for hint in hints:
        if hint.group_id == skill.group_id and hint.rarity == skill.rarity:
            hint.level = min(5, hint.level + level)
            break
    else:
        hints.append(SkillHint(skill.group_id, skill.rarity, level, skill.name))


def _add_skill(info: TurnInfo, effect: EventEffect) -> None:
    skill = effect.skill
    if not skill:
        return
    learnt_list = info.learnt_skill_list
    for learnt in learnt_list:
        if skill.id == learnt.skill_id:
            break
    else:
        learnt_list.append(LearntSkill(skill.id, 1, False, skill.name))


def _add_condition(info: TurnInfo, effect: EventEffect) -> None:
    def _discard_conditions(_info: TurnInfo, _values: Iterable[int]):
        _now = _info.uma_condition_list
        _now[:] = (x for x in _now if x.value not in _values)

    _ = {1: '夜ふかし気味', 2: 'なまけ癖', 3: '肌あれ', 4: '太り気味',
         5: '片頭痛', 6: '練習ベタ', 7: '切れ者', 8: '愛嬌◯', 9: '注目株',
         10: '練習上手◯', 11: '練習上手◎', 12: '小さなほころび',
         13: '大輪の輝き', 14: 'ファンとの約束・北海道', 15: 'ファンとの約束・北東',
         16: 'ファンとの約束・中山', 17: 'ファンとの約束・関西',
         18: 'ファンとの約束・小倉', 19: 'まだまだ準備中', 20: 'ガラスの脚',
         21: '怪しい雲行き', 22: 'ファンとの約束・川崎', 23: '英雄の光輝',
         24: '春待つ蕾', 25: 'ポジティブ思考', 26: '幸運体質', 100: "情熱ゾーン"}
    clearable_inferior = 1, 2, 3, 4, 5, 6,
    overwrite = {10: 6, 6: 10}

    now = info.uma_condition_list
    new: Condition | None = effect.condition
    clear: Condition = effect.condition_clear
    if clear:
        if clear.value:
            _discard_conditions(info, (clear.value,))
        else:
            _discard_conditions(info, clearable_inferior)
    if not new:
        return
    for k, v in overwrite.items():
        if Condition(k) in now:
            _discard_conditions(info, (v,))
    now.append(new)
    now.sort(key=lambda x: x.value)


def _add_last_train(info: TurnInfo, effect: EventEffect) -> None:
    train = info.turn_operation
    if not train:
        return
    train = train.training_type.value
    if not train:
        return
    train = ('speed', 'stamina', 'power', 'will', 'intelligence')[train - 1]
    setattr(info.uma_attribute, train, getattr(info.uma_attribute, train)
            + effect.last_train)


# TODO 实装了再说
def _add_train_level(info: TurnInfo, effect: EventEffect) -> None:
    for i in range(5):
        info.train_level_count_list += effect.train_lv * 4


def _add_favor(info: TurnInfo, effect: EventEffect) -> None:
    chara, favor = effect.favor
    if not favor:
        return
    for person in info.person_list:
        if chara.name in person.name:
            person.favor_num = min(100, person.favor_num + favor)
            break
    else:
        print('无事发生', chara)


def score_context(ctx: UmamusumeContext) -> float:
    log.debug("干劲得分：%.2f", motivation := _motivation(ctx))
    log.debug("属性得分：%.2f", attribute := _attribute(ctx))
    log.debug("状态得分：%.2f", condition := _condition(ctx))
    log.debug("体力得分：%.2f", hp := _hp(ctx))
    log.debug("技能得分：%.2f", skill := _skill(ctx))
    log.debug("友情得分：%.2f", favor := _favor(ctx))
    log.debug("合计得分：%.2f", total := motivation + attribute + condition + hp + skill + favor)
    return total
