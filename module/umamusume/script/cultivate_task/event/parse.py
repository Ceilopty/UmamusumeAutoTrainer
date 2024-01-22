from collections import namedtuple
from module.umamusume.define import Condition

# 稀有事件
P_P = 0.9
P_Q = 0.1
P_R = 0.45
P_T = 0.45

# 普通成功失败判定
P_S = 0.5
P_F = 0.5

EventEffect = namedtuple('EventEffect', ('motivation', 'vital', 'max_vital',
                                         'speed_incr', 'stamina_incr', 'power_incr', 'guts_incr', 'wiz_incr',
                                         'speed_limit_incr', 'stamina_limit_incr', 'power_limit_incr',
                                         'guts_limit_incr', 'wiz_limit_incr', 'all_limit_incr', 'skill_point_incr',
                                         'skill_hint', 'skill', 'condition', 'condition_clear',
                                         'last_train', 'random_attr', 'train_lv', 'favor', 'fan', 'other'),
                         defaults=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   (None, 0), None, None, None,
                                   0, (0, 0), 0, (None, 0), 0, None))

EventChoice = namedtuple('EventChoice', ('possibility', 'event_effect'),
                         defaults=(1, None))


def parse_event(event: tuple):
    parsed_event = []
    for choice in event:
        parsed_choices = []
        for possibility, effect in choice:
            if type(possibility) is str:
                possibility = globals()['P_' + possibility]
            if 'condition' in effect:
                effect['condition'] = getattr(Condition, 'CONDITION_' + effect['condition'].upper())
            event_effect = EventEffect()._replace(**effect)
            parsed_choice = EventChoice()._replace(possibility=possibility, event_effect=event_effect)
            parsed_choices.append(parsed_choice)
        parsed_event.append(parsed_choices)
    return parsed_event
