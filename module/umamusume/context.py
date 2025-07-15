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
    expect_attribute: list[int] | None
    follow_support_card_name: str
    follow_support_card_level: int
    extra_race_list: list[int]
    learn_skill_list: list[list[str]]
    learn_skill_blacklist: list[str]
    learn_skill_done: bool
    learn_skill_selected: bool
    learn_skill_before_race_done: bool
    cultivate_finish: bool
    tactic_list: list[int]
    debut_race_win: bool
    clock_use_limit: int
    clock_used: int
    clock_use_day_limit: int
    learn_skill_threshold: int
    learn_skill_only_user_provided: bool
    learn_skill_before_race: bool
    allow_recover_tp_drink: bool
    allow_recover_tp_diamond: bool
    parse_factor_done: bool
    extra_weight: list
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
        self.expect_attribute = None
        self.turn_info = TurnInfo()
        self.turn_info_history = []
        self.extra_race_list = []
        self.learn_skill_list = []
        self.learn_skill_blacklist = []
        self.learn_skill_done = False
        self.learn_skill_selected = False
        self.learn_skill_before_race_done = False
        self.cultivate_finish = False
        self.tactic_list = []
        self.debut_race_win = False
        self.clock_use_limit = 0
        self.clock_used = 0
        self.clock_use_day_limit = 0
        self.allow_recover_tp_drink = False
        self.allow_recover_tp_diamond = False
        self.parse_factor_done = False
        self.extra_weight = []
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
    time_sale: list[int]
    time_sale_detail: TimeSaleContextDetail

    def __init__(self):
        self.time_sale = []
        self.time_sale_detail = TimeSaleContextDetail()

    def refresh_time_sale(self):
        self.time_sale_detail.buy[:] = self.time_sale
        self.time_sale_detail.bought.clear()
        self.time_sale_detail.buying = None


class TeamStadiumContextDetail(TimeSaleTaskContextDetail):
    opponent_index: int | None
    opponent_stamina: int | None
    raced: bool
    off: bool

    def __init__(self):
        super().__init__()
        self.raced = False
        self.off = False


class DonateContextDetail:
    ask_shoe_type: int
    donated: bool
    asked: bool
    swiped: int

    def __init__(self):
        super().__init__()
        self.donated = False
        self.asked = False
        self.swiped = 0


class DailyRaceContextDetail(TimeSaleTaskContextDetail):
    race: int | None
    difficulty: int | None
    raced: bool

    def __init__(self):
        super().__init__()
        self.raced = False


class UmamusumeContext(BotContext):
    task: UmamusumeTask
    cultivate_detail: CultivateContextDetail
    team_stadium_detail: TeamStadiumContextDetail
    donate_detail: DonateContextDetail
    daily_race_detail: DailyRaceContextDetail
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
            detail.expect_attribute = task.detail.expect_attribute
            detail.follow_support_card_name = task.detail.follow_support_card_name
            detail.follow_support_card_level = task.detail.follow_support_card_level
            detail.extra_race_list = task.detail.extra_race_list
            detail.learn_skill_list = task.detail.learn_skill_list
            detail.learn_skill_blacklist = task.detail.learn_skill_blacklist
            detail.tactic_list = task.detail.tactic_list
            detail.clock_use_limit = task.detail.clock_use_limit
            detail.clock_use_day_limit = task.detail.clock_use_day_limit
            detail.learn_skill_threshold = task.detail.learn_skill_threshold
            detail.learn_skill_only_user_provided = task.detail.learn_skill_only_user_provided
            detail.learn_skill_before_race = task.detail.learn_skill_before_race
            detail.allow_recover_tp_drink = task.detail.allow_recover_tp_drink
            detail.allow_recover_tp_diamond = task.detail.allow_recover_tp_diamond
            detail.extra_weight = task.detail.extra_weight
            ctx.cultivate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM:
            detail = TeamStadiumContextDetail()
            detail.opponent_index = task.detail.opponent_index
            detail.opponent_stamina = task.detail.opponent_stamina
            detail.time_sale[:] = task.detail.time_sale
            detail.refresh_time_sale()
            ctx.team_stadium_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.refresh_time_sale
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DONATE:
            detail = DonateContextDetail()
            detail.ask_shoe_type = task.detail.ask_shoe_type
            ctx.donate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DAILY_RACE:
            detail = DailyRaceContextDetail()
            detail.race = task.detail.daily_race_type
            detail.difficulty = task.detail.daily_race_difficulty
            detail.time_sale[:] = task.detail.time_sale
            detail.refresh_time_sale()
            ctx.daily_race_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.refresh_time_sale
    return ctx
