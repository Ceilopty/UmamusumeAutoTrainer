from module.umamusume.context import UmamusumeContext, TurnInfo
from module.umamusume.define import Condition
from ..cultivate_task.event.parse import EventEffect
from ..cultivate_task.event.event_ai import context_copy
from .parse.event_effect import EventEffects
from .parse.skill import Skill
from .parse.chara import Chara, CharaNotFoundError, SupportCardChara
from .database import DataBase

__all__ = ["EventLogger"]

MAX_VIEW = 5
LOG_PATH = ".\\event.log"


class EventLoggingError(Exception):
    pass


class EventLogger:
    viewed: int = 0
    origin: TurnInfo | None = None
    effects: list[EventEffect] = []
    logging: bool = False
    trigger_name: str
    event_name: str
    story_id: int
    choice_index: int
    choice_str: str
    select_index: int
    is_success: int
    effect: EventEffects
    choice_len: int

    @classmethod
    def init(cls):
        cls.viewed = 0
        cls.origin = None
        cls.effects.clear()
        cls.logging = False

    @classmethod
    def start(cls, ctx: UmamusumeContext,
              trigger_name: str,
              event_name: str,
              story_id: int,
              choice_index: int,
              choice_str: str,
              select_index: int,
              is_success: int,
              effect: EventEffects,
              choice_len: int,
              ):
        if cls.logging:
            cls.log("已在记录中，将重置")
        cls.origin = context_copy(ctx).cultivate_detail.turn_info
        cls.trigger_name = trigger_name
        cls.event_name = event_name
        cls.story_id = story_id
        cls.choice_index = choice_index
        cls.choice_str = choice_str
        cls.select_index = select_index
        cls.is_success = is_success
        cls.effect = effect
        cls.choice_len = choice_len
        cls.logging = True

    @classmethod
    def view(cls, ctx: UmamusumeContext):
        if not cls.logging:
            return
        if cls.viewed > MAX_VIEW:
            print("未发现变动")
            cls.log()
        cls.viewed += 1
        if cls.diff(context_copy(ctx).cultivate_detail.turn_info):
            cls.log()

    @classmethod
    def log(cls, extra_information=""):
        log = ""
        log += f"来源：{cls.trigger_name}\n"
        log += f"事件名称：{cls.event_name}\n"
        log += f"选择选项{cls.choice_index}：{cls.choice_str}\n"
        log += f"声称效果：\n{cls.effect}\n"
        log += f"实际检测：{cls.effect_str()}\n"
        log += f"js格式：\n{cls.js()}\n"
        log += f"额外信息：{extra_information}\n\n"
        with open(LOG_PATH, 'a+', encoding='utf-8') as f:
            f.write(log)
        cls.init()

    @classmethod
    def diff(cls, ti: TurnInfo) -> bool:
        cls.attr(ti)
        cls.motivation(ti)
        cls.vital(ti)
        cls.skill(ti)
        cls.condition(ti)
        cls.favor(ti)
        return bool(cls.effects)

    @classmethod
    def effect_str(cls):
        return '、'.join(EventEffects.effect_str(effect)for effect in cls.effects)

    @classmethod
    def js(cls):
        js = {
            'Id': cls.story_id,
            'Choices': []
        }
        for i in range(cls.choice_len):
            if i == cls.choice_index:
                js['Choices'].append([
                    {
                        "SelectIndex": cls.select_index,
                        "Scenario": 0,
                        "State": cls.is_success,
                        "Effect": cls.effect_str()
                    }
                ])
            else:
                js['Choices'].append([])
        return js

    @classmethod
    def attr(cls, now: TurnInfo):
        me = cls.origin.uma_attribute
        other = now.uma_attribute
        standard = ['speed', 'stamina', 'power', 'guts', 'wiz', 'skill_point']
        here = ['speed', 'stamina', 'power', 'will', 'intelligence', 'skill_point']
        for x, y in zip(here, standard):
            if dif := getattr(other, x) - getattr(me, x):
                cls.effects.append(EventEffect(**{y+'_incr': dif}))
        me = cls.origin.uma_attribute_limit_list
        other = cls.origin.uma_attribute_limit_list
        for x, y in enumerate(standard[:5]):
            if dif := other[x] - me[x]:
                cls.effects.append(EventEffect(**{y + '_limit_incr': dif}))

    @classmethod
    def motivation(cls, now: TurnInfo):
        if dif := now.motivation_level.value - cls.origin.motivation_level.value:
            cls.effects.append(EventEffect(motivation=dif))

    @classmethod
    def vital(cls, now: TurnInfo):
        if dif := now.max_vital - cls.origin.max_vital:
            cls.effects.append(EventEffect(max_vital=dif))
        if dif := now.remain_stamina - cls.origin.remain_stamina:
            cls.effects.append(EventEffect(vital=dif))

    @classmethod
    def skill(cls, now: TurnInfo):
        for learnt in now.learnt_skill_list:
            if any(found for found in cls.origin.learnt_skill_list if found.skill_id == learnt.skill_id):
                continue
            skill = Skill(DataBase.get_skill_by_id(learnt.skill_id).name)
            cls.effects.append(EventEffect(skill=skill))
        for hint in now.skill_hint_list:
            skill = Skill(DataBase.get_skill_group_by_id_and_rarity(hint.group_id, hint.rarity)[0].name)
            if same := list(found for found in cls.origin.skill_hint_list
                            if found.group_id == hint.group_id
                            and found.rarity == hint.rarity):
                if dif := hint.level - same[0].level:
                    cls.effects.append(EventEffect(skill_hint=(skill, dif)))
            else:
                cls.effects.append(EventEffect(skill_hint=(skill, hint.level)))

    @classmethod
    def condition(cls, now: TurnInfo):
        me = cls.origin.uma_condition_list
        other = now.uma_condition_list
        for get in (c for c in other if c not in me):
            cls.effects.append(EventEffect(condition=get))
        for clear in (c for c in me if c not in other):
            cls.effects.append(EventEffect(condition_clear=clear))

    @classmethod
    def favor(cls, now: TurnInfo):
        pass
