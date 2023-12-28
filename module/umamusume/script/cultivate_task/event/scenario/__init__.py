from module.umamusume.context import UmamusumeContext
from module.umamusume.define import TurnOperationType
from .. import Event, EventHolder

__all__ = EventHolder.get_all(__name__)

from . import *


class Scenario(EventHolder):
    pass


# 第一年新年事件
def scenario_event_1(ctx: UmamusumeContext) -> int:
    if ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_REST or \
            ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_MEDIC and \
            ctx.cultivate_detail.turn_info.remain_stamina >= 50 or \
            ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_TRIP and \
            ctx.cultivate_detail.turn_info.remain_stamina >= 50:
        return 3
    elif ctx.cultivate_detail.turn_info.remain_stamina >= 90:
        return 1
    else:
        return 2


# 第二年新年事件
def scenario_event_2(ctx: UmamusumeContext) -> int:
    if ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_REST or \
            ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_MEDIC and \
            ctx.cultivate_detail.turn_info.remain_stamina >= 40 or \
            ctx.cultivate_detail.turn_info.turn_operation == TurnOperationType.TURN_OPERATION_TYPE_TRIP and \
            ctx.cultivate_detail.turn_info.remain_stamina >= 50:
        return 3
    elif ctx.cultivate_detail.turn_info.remain_stamina >= 80:
        return 2
    else:
        return 1


event_map = {
        "安心～针灸师，登☆场": 5,
        "新年的抱负": scenario_event_1,
        "新年参拜": scenario_event_2,
        "新年祈福": scenario_event_2
    }

for event_name in event_map:
    Event.register(event_name, event_map[event_name])

for scenario in __all__:
    Scenario.load(scenario)
