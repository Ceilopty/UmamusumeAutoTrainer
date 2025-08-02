from __future__ import annotations

from module.umamusume.define import *
import bot.base.log as logger


log = logger.get_logger(__name__)


class SupportCardInfo:
    name: str
    card_type: SupportCardType
    _favor: SupportCardFavorLevel
    has_event: bool
    favor_num: int | None
    # 青春杯部分
    can_incr_aoharu_train: bool

    def __init__(self,
                 name: str = "support_card",
                 card_type: SupportCardType = SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN,
                 favor: SupportCardFavorLevel = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN,
                 has_event: bool = False,
                 favor_num: int | None = None,
                 can_incr_aoharu_train: bool = False):
        self.name = name
        self.card_type = card_type
        self._favor = favor
        self.has_event = has_event
        self.favor_num = favor_num
        self.can_incr_aoharu_train = can_incr_aoharu_train

    @property
    def favor(self):
        """分四段，分别是绿松石(<60)，绿(<80)，金（<100），黄绿(100)"""
        if self.favor_num is not None:
            return SupportCardFavorLevel(1 if self.favor_num < 60 else self.favor_num // 20 - 1)
        else:
            return self._favor

    @favor.setter
    def favor(self, favor: SupportCardFavorLevel):
        if self.favor_num is None:
            self._favor = favor


class TrainingInfo:
    support_card_info_list: list[SupportCardInfo]
    speed_incr: int
    stamina_incr: int
    power_incr: int
    will_incr: int
    intelligence_incr: int
    skill_point_incr: int
    vital_incr: int
    failure_rate: int
    train_level_count: int

    def __init__(self):
        self.speed_incr = 0
        self.stamina_incr = 0
        self.power_incr = 0
        self.will_incr = 0
        self.intelligence_incr = 0
        self.skill_point_incr = 0
        self.support_card_info_list = []
        self.vital_incr = 0
        self.failure_rate = 0

    def log_training_info(self, scenario_type: ScenarioType):
        log.info("训练结果：速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s, %s体力：%s, 失败率: %3d", self.speed_incr,
                 self.stamina_incr, self.power_incr, self.will_incr,
                 self.intelligence_incr, self.skill_point_incr,
                 "消耗" if self.vital_incr < 0 else "回复" if self.vital_incr > 0 else "",
                 abs(self.vital_incr), self.failure_rate)
        text = "此训练附带支援卡列表：["
        if scenario_type == ScenarioType.SCENARIO_TYPE_AOHARU:
            for c in self.support_card_info_list:
                text += "[支援卡名称：" + str(c.name) + ", 支援卡类型：" + str(c.card_type.name) + ", 支援卡羁绊阶段：" + \
                        str(c.favor.name) + ", 可提升青春杯友情: " + str(c.can_incr_aoharu_train) + "] "
        else:
            for c in self.support_card_info_list:
                if c.favor != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                    text += "[支援卡名称：" + str(c.name) + ", 支援卡类型：" + str(
                        c.card_type) + ", 支援卡羁绊阶段：" + str(c.favor) + "] "
        text += "]"
        log.info(text)


class UmaAttribute:
    speed: int
    stamina: int
    power: int
    will: int
    intelligence: int
    skill_point: int

    def __init__(self):
        self.speed = 0
        self.stamina = 0
        self.power = 0
        self.will = 0
        self.intelligence = 0
        self.skill_point = 0

    def to_tuple(self):
        return self.speed, self.stamina, self.power, self.will, self.intelligence, self.skill_point


class SkillHint:
    group_id: int
    rarity: int
    level: int

    def __init__(self, group_id=0, rarity=0, level=0, name=""):
        self.group_id = group_id
        self.rarity = rarity
        self.level = level
        self.name = name

    def __str__(self):
        return f"{{{self.name}}}{self.level}级"


class LearntSkill:
    skill_id: int
    level: int
    is_inherent: bool
    name: str

    def __init__(self, skill_id=0, level=1, is_inherent=False, name=""):
        self.skill_id = skill_id
        self.level = level
        self.is_inherent = is_inherent
        self.name = name

    def __str__(self):
        name = self.name or "技能"
        return f"{name}@{self.skill_id} " + (f"等级{self.level:d}" if self.is_inherent else "")


class ScenarioInfo:
    class _LinkCardInfo:
        first_click: bool
        outgoing_unlocked: bool
        outgoing_refused: bool
        outgoing_used: int

        def __init__(self):
            self.first_click = False
            self.outgoing_unlocked = False
            self.outgoing_refused = False
            self.outgoing_used = 0


class UraInfo(ScenarioInfo):
    ura_tsyInfo: UraInfo._LinkCardInfo
    ura_lmInfo: UraInfo._LinkCardInfo

    def __init__(self):
        self.ura_tsyInfo = UraInfo._LinkCardInfo()
        self.ura_lmInfo = UraInfo._LinkCardInfo()


class AoharuInfo(ScenarioInfo):
    aoharu_kashimotoInfo: AoharuInfo._LinkCardInfo
    aoharu_race_index: int

    def __init__(self):
        self.aoharu_kashimotoInfo = AoharuInfo._LinkCardInfo()
        self.aoharu_race_index = 0


class TurnOperation:
    turn_operation_type: TurnOperationType
    turn_operation_type_replace: TurnOperationType
    training_type: TrainingType
    race_id: int

    def __init__(self):
        self.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN
        self.turn_operation_type_replace = TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN
        self.training_type = TrainingType.TRAINING_TYPE_UNKNOWN
        self.race_id = 0

    def log_turn_operation(self):
        log.info("本回合执行操作：%s", self.turn_operation_type)
        log.info("本回合备选操作：%s", self.turn_operation_type_replace)
        if self.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_TRAINING:
            log.info("训练类型：%s", self.training_type)


class TurnInfo:
    date: int

    parse_train_info_finish: bool
    training_info_list: list[TrainingInfo]
    parse_main_menu_finish: bool
    uma_attribute: UmaAttribute
    remain_stamina: int
    motivation_level: MotivationLevel
    medic_room_available: bool
    race_available: bool

    turn_operation: TurnOperation | None
    turn_info_logged: bool
    turn_learn_skill_done: bool

    uma_condition_list: list[Condition]
    skill_hint_list: list[SkillHint]
    learnt_skill_list: list[LearntSkill]
    disable_skill_id_array: list[int]
    uma_attribute_limit_list: list[int]
    max_vital: int
    train_level_count_list: list[int]
    scenario_info: ScenarioInfo
    out_destination: int | None
    person_list: list[SupportCardInfo]
    proper_info: list[list[int]]
    racing: bool
    race_tactic_exist: list[bool]

    # 青春杯
    aoharu_race_index: int

    def __init__(self):
        self.date = -1
        self.parse_train_info_finish = False
        self.training_info_list = [TrainingInfo(), TrainingInfo(), TrainingInfo(), TrainingInfo(), TrainingInfo()]
        self.parse_main_menu_finish = False
        self.uma_attribute = UmaAttribute()
        self.remain_stamina = -1
        self.motivation_level = MotivationLevel.MOTIVATION_LEVEL_UNKNOWN
        self.medic_room_available = False
        self.race_available = False
        self.turn_operation = None
        self.turn_info_logged = False
        self.turn_learn_skill_done = False
        self.uma_condition_list = []
        self.skill_hint_list = []
        self.learnt_skill_list = []
        self.disable_skill_id_array = []
        self.uma_attribute_limit_list = [0, 0, 0, 0, 0]
        self.max_vital = 100
        self.train_level_count_list = [0, 0, 0, 0, 0]
        self.scenario_info = ScenarioInfo()
        self.out_destination = None
        self.person_list = []
        self.proper_info = [[0, 0], [0, 0, 0, 0,], [0, 0, 0, 0]]
        self.racing = False
        self.race_tactic_exist = [False, False, False, False]
        self.aoharu_race_index = 0

    def log_turn_info(self, scenario_type: ScenarioType, train=True, show_skill_and_hint=False):
        log.info("当前回合时间 " + str(self.date))
        log.info("干劲状态 " + str(self.motivation_level))
        log.info("体力剩余 " + str(self.remain_stamina))
        log.info("当前属性值 速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s", self.uma_attribute.speed,
                 self.uma_attribute.stamina, self.uma_attribute.power, self.uma_attribute.will,
                 self.uma_attribute.intelligence, self.uma_attribute.skill_point)
        if train:
            log.info("速度训练结果：")
            self.training_info_list[0].log_training_info(scenario_type)
            log.info("耐力训练结果：")
            self.training_info_list[1].log_training_info(scenario_type)
            log.info("力量训练结果：")
            self.training_info_list[2].log_training_info(scenario_type)
            log.info("毅力训练结果：")
            self.training_info_list[3].log_training_info(scenario_type)
            log.info("智力训练结果：")
            self.training_info_list[4].log_training_info(scenario_type)
            if self.uma_condition_list:
                log.debug("当前状态：" + '，'.join(map(str, self.uma_condition_list)))
        if show_skill_and_hint:
            if len(self.learnt_skill_list) > 1:
                log.debug("已习得技能：" + '，'.join(map(str, self.learnt_skill_list)))
            if self.skill_hint_list:
                log.debug("已获得技能启示：" + '，'.join(map(str, self.skill_hint_list)))
