from types import FunctionType
from bot.base.context import BotContext
from module.umamusume.task import UmamusumeTask, UmamusumeTaskType
from module.umamusume.define import *
from module.umamusume.script.cultivate_task.types import TurnInfo
from module.umamusume.script.cultivate_task.scenario import base_scenario, ura_scenario, aoharuhai_scenario
import bot.base.log as logger

log = logger.get_logger(__name__)


class CultivateContextDetail:
    scenario: base_scenario.BaseScenario = None
    turn_info: TurnInfo | None
    turn_info_history: list[TurnInfo]
    learn_skill_done: bool
    learn_skill_selected: bool
    learn_skill_before_race_done: bool
    cultivate_finish: bool
    debut_race_win: bool
    clock_used: int
    parse_factor_done: bool
    catch_doll: int
    sasami: bool
    uma_id: int
    talent_level: int
    card_id_list: list[int]
    uma_rarity: int
    no_tp: bool
    borrowed: bool
    scenario_tried: int

    def __init__(self):
        self.turn_info = TurnInfo()
        self.turn_info_history = []
        self.learn_skill_done = False
        self.learn_skill_selected = False
        self.learn_skill_before_race_done = False
        self.cultivate_finish = False
        self.debut_race_win = False
        self.clock_used = 0
        self.parse_factor_done = False
        self.catch_doll = 0
        self.sasami = False
        self.uma_id = 0
        self.talent_level = 0
        self.card_id_list = []
        self.uma_rarity = 0
        self.no_tp = False
        self.borrowed = False
        self.scenario_tried = 0

    def reset_skill_learn(self):
        self.learn_skill_done = False
        self.learn_skill_selected = False


class TimeSaleContextDetail:
    buy: list[int]
    bought: list[int]
    buying: int | None
    refresh: FunctionType

    def __init__(self):
        self.buy = []
        self.bought = []
        self.buying = None


class TimeSaleTaskContextDetail:
    time_sale_detail: TimeSaleContextDetail

    def __init__(self):
        self.time_sale_detail = TimeSaleContextDetail()

    def get_refresh_method(self, time_sale):
        def refresh_time_sale():
            self.time_sale_detail.buy[:] = time_sale
            self.time_sale_detail.bought.clear()
            self.time_sale_detail.buying = None
        return refresh_time_sale


class TeamStadiumContextDetail(TimeSaleTaskContextDetail):
    raced: bool
    off: bool

    def __init__(self):
        super().__init__()
        self.raced = False
        self.off = False


class DonateContextDetail:
    donated: bool
    asked: bool
    swiped: int

    def __init__(self):
        super().__init__()
        self.donated = False
        self.asked = False
        self.swiped = 0


class DailyScheduleContextDetail(TimeSaleTaskContextDetail):
    raced: bool
    legend_raced: bool

    def __init__(self):
        super().__init__()
        self.raced = False
        self.legend_raced = False


class UmamusumeContext(BotContext):
    task: UmamusumeTask
    cultivate_detail: CultivateContextDetail
    team_stadium_detail: TeamStadiumContextDetail
    donate_detail: DonateContextDetail
    daily_schedule_detail: DailyScheduleContextDetail
    time_sale_detail: TimeSaleContextDetail

    def __init__(self, task, ctrl):
        super().__init__(task, ctrl)

    def is_task_finish(self) -> bool:
        return False


def build_context(task: UmamusumeTask, ctrl) -> UmamusumeContext:
    ctx = UmamusumeContext(task, ctrl)
    match task.task_type:
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE:
            detail = CultivateContextDetail()
            # 根据剧本类型初始化对应的继承类
            match task.detail.scenario:
                case ScenarioType.SCENARIO_TYPE_URA:
                    detail.scenario = ura_scenario.URAScenario()
                case ScenarioType.SCENARIO_TYPE_AOHARU:
                    detail.scenario = aoharuhai_scenario.AoharuHaiScenario()
                case _:  # 占位, 实际上不可能到达这里
                    log.error("未知的场景")
                    detail.scenario = None
            ctx.cultivate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM:
            detail = TeamStadiumContextDetail()
            ctx.team_stadium_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.get_refresh_method(task.detail.time_sale)
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DONATE:
            detail = DonateContextDetail()
            ctx.donate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DAILY_SCHEDULE:
            detail = DailyScheduleContextDetail()
            ctx.daily_schedule_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.get_refresh_method(task.detail.time_sale)
    return ctx
