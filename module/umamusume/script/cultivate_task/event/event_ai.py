import bot.base.log as logger
from module.umamusume.context import UmamusumeContext, TurnInfo
from module.umamusume.define import *
from module.umamusume.script.cultivate_task.event.parse import EventEffect

log = logger.get_logger(__name__)

ATTRIBUTE_PREFERENCE = (1, 0.9, 0.8, 0.2, 0.3, 0.1)


def _hp(ctx: UmamusumeContext) -> float:
    return ctx.cultivate_detail.turn_info.remain_stamina + ctx.cultivate_detail.turn_info.max_vital


def _condition(ctx: UmamusumeContext) -> float:
    return 0.0


def _motivation(ctx: UmamusumeContext) -> float:
    return 0.0


def _skill(ctx: UmamusumeContext) -> float:
    return 0.0


def _attribute(ctx: UmamusumeContext) -> float:
    return 0.0


def _race_dates(ctx: UmamusumeContext) -> list:
    pass


def context_copy(origin_ctx: UmamusumeContext) ->UmamusumeContext:
    from copy import copy, deepcopy, Error
    ctx = UmamusumeContext(origin_ctx.task, origin_ctx.ctrl)
    try:
        ctx.cultivate_detail = deepcopy(origin_ctx.cultivate_detail)
    except Error:
        ctx = copy(ctx)
    return ctx


def context_plus_effect(ctx: UmamusumeContext, effect: EventEffect) -> UmamusumeContext:
    _add_vital(ctx.cultivate_detail.turn_info, effect)
    return ctx


def _add_motivation(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_vital(info: TurnInfo, effect: EventEffect) -> None:
    info.remain_stamina = min(info.max_vital + effect.max_vital, info.remain_stamina + effect.vital)


def _add_attribute(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_limit(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_hint(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_skill(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_condition(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_last_train(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_train_level(info: TurnInfo, effect: EventEffect) -> None:
    return


def _add_favor(info: TurnInfo, effect: EventEffect) -> None:
    return


def score_context(ctx: UmamusumeContext)->float:
    return _motivation(ctx) + _attribute(ctx) + _condition(ctx) + _hp(ctx) + _skill(ctx)