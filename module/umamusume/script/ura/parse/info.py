from ..gallop import Data, Array
from .define import *
from .event_effect import *
from ..database.define import CommandType, ScenarioType
from collections import namedtuple


class Person(Data):
    charaId: int
    cardIdInGame: int
    friendship: int
    isHint: bool
    cardRecord: int
    trainType: int
    personType: Enum


class UraPerson(Person):
    personType: UraPersonType


class AoharuPerson(Person):
    personType: AoharuPersonType
    member_state: int       # 1为出现，0未出现
    soul_threshold_id: int  # 5为可魂爆
    soul_event_state: int   # 1为已魂爆
    isGuide: bool           # 青春训练
    isSoul: bool            # 魂爆


class BasePerson(Person):
    pass


TrainValue = namedtuple('TrainValue', ('speed',
                                       'stamina',
                                       'pow',
                                       'guts',
                                       'wiz',
                                       'sp',
                                       'vital',))


class Skill(Data):
    skill_id: int
    level: int


class SkillTip(Data):
    group_id: int
    rarity: int
    level: int


class TurnInfo(Data):
    scenario: ScenarioType
    umaId: int
    turn: int
    vital: int
    maxVital: int
    isQieZhe: bool
    isAiJiao: bool
    failureRateBias: int
    fiveStatus: Array[int]
    fiveStatusLimit: Array[int]
    skillPt: int
    skillScore: int
    motivation: int
    isPositiveThinking: bool
    trainLevelCount: Array[int]
    cardId: Array[int]
    persons: Array[Person]
    personDistribution: Array[Array[int]]
    trainValue: Array[Array[int]]
    failRate: Array[int]
    skills: Array[Skill]
    skillTips: Array[SkillTip]
    disable_skill_id_array: Array[int]
    chara_effect_id_array: Array[ConditionType]
    available_command_array: Array[CommandType]
    proper_info: Array[Array[int]]
    talent_level: int


class TurnInfoURA(TurnInfo):
    normalCardCount: int
    persons: Array[UraPerson]
    motivationDropCount: int
    ura_tsyFirstClick: bool
    ura_tsyOutgoingUnlocked: bool
    ura_tsyOutgoingRefused: bool
    ura_tsyOutgoingUsed: int
    ura_lmFirstClick: bool
    ura_lmOutgoingUnlocked: bool
    ura_lmOutgoingRefused: bool
    ura_lmOutgoingUsed: int


class TurnInfoAoharu(TurnInfo):
    persons: Array[AoharuPerson]
    friend_type: int    # 0没带友人卡，1ssr卡，2r卡
    friend_stage: int   # 0未点击，1点击还未解锁出行，2已解锁出行
    friend_outgoingUsed: bool
    umaStar: int
    islegal: bool
    ptScoreRate: float
    isRefreshMind: bool
    saihou: int
    isRacing: bool
    playing_state: int
    normalCardCount: int
    motivationDropCount: int
    lockedTrainingId: int
    friendship_noncard_yayoi: int
    friendship_noncard_reporter: int
    friend_cardId: int
    friend_personId:int

class TurnInfoBase(TurnInfo):
    umaStar: int
    ptScoreRate: float
    isRefreshMind: bool
    zhongMaBlueCount: Array[int]
    saihou: int
    isRacing: bool
    lockedTrainingId: int
    friendship_noncard_yayoi: int
    friendship_noncard_reporter: int
    friend_type: int
    friend_cardId: int
    friend_personId: int
    friend_stage: int
    friend_outgoingUsed: int
    playing_state: int


class OriginEventInfo(Data):
    class EventContentsInfo(Data):
        class Choice(Data):
            select_index: int
            receive_item_id: int
            target_race_id: int
        support_card_id: int
        show_clear: int
        show_clear_sort_id: int
        choice_array: Array[Choice]
        is_effected_multi_chara: int
    event_id: int
    chara_id: int
    story_id: int
    play_timing: int
    event_contents_info: EventContentsInfo


class EventInfo(Data):
    islegal: bool
    turn: int
    eventCount: int
    triggerName: str
    eventName: str
    story_id: int
    choices: Array[str]
    select_indices: Array[int]
    is_success: Array[EventState]
    effect: Array[EventEffects]
    eventInfo: OriginEventInfo
