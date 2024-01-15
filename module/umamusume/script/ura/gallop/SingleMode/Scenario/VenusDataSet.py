"""女神杯"""
from ... import Data, Array
from ..CommandInfo import CommandInfoBasic
from ..Race import (SingleModeRaceStartInfo,
                    SingleModeRaceCondition,
                    RaceResult as VenusRaceHistory,
                    CharaRaceReward)


class VenusEvaluationInfo(Data):
    target_id: int
    chara_id: int
    member_state: int


class VenusSpiritInfo(Data):
    spirit_num: int
    spirit_id: int
    effect_group_id: int


class VenusActiveSpiritEffect(Data):
    chara_id: int
    effect_group_id: int
    begin_turn: int
    end_turn: int


class VenusCharaInfo(Data):
    chara_id: int
    venus_level: int


class VenusCharaCommandInfo(Data):
    command_type: int
    command_id: int
    spirit_id: int
    is_boost: int


class VenusDataSet(Data):
    race_start_info: SingleModeRaceStartInfo
    race_scenario: str
    command_info_array: Array[CommandInfoBasic]
    evaluation_info_array: Array[VenusEvaluationInfo]
    spirit_info_array: Array[VenusSpiritInfo]
    venus_spirit_active_effect_info_array: Array[VenusActiveSpiritEffect]
    venus_chara_info_array: Array[VenusCharaInfo]
    venus_chara_command_info_array: Array[VenusCharaCommandInfo]
    venus_race_condition: SingleModeRaceCondition
    venus_race_history_array: Array[VenusRaceHistory]
    race_reward_info: CharaRaceReward
    live_item_id: int
