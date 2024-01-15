"""巅峰杯"""
from ... import Data, Array
from ..CommandInfo import CommandInfoBasic
from ..HorseCommonData import HorseInfoBasic


class FreeUserItem(Data):
    item_id: int
    num: int


class FreePickUpItem(Data):
    shop_item_id: int
    item_id: int
    coin_num: int
    original_coin_num: int
    item_buy_num: int
    limit_buy_count: int
    limit_turn: int


class NpcResult:
    npc_id: int
    result_rank: int


class FreeTwinkleRaceNpcInfo(HorseInfoBasic):
    npc_id: int
    chara_id: int
    dress_id: int
    win_points: int
    power: int


class RivalRaceInfo:
    program_id: int
    chara_id: int


class FreeTwinkleRaceNpcResult(Data):
    turn: int
    program_id: int
    race_result_array: Array[NpcResult]


class FreeItemEffect(Data):
    use_id: int
    item_id: int
    effect_type: int
    effect_value_1: int
    effect_value_2: int
    effect_value_3: int
    effect_value_4: int
    begin_turn: int
    end_turn: int


class FreeDataSet(Data):
    shop_id: int
    sale_value: int
    win_points: int
    gained_coin_num: int
    coin_num: int
    twinkle_race_ranking: int
    user_item_info_array: Array[FreeUserItem]
    pick_up_item_info_array: Array[FreePickUpItem]
    twinkle_race_npc_info_array: Array[FreeTwinkleRaceNpcInfo]
    item_effect_array: Array[FreeItemEffect]
    twinkle_race_npc_result_array: Array[FreeTwinkleRaceNpcResult]
    rival_race_info_array: Array[RivalRaceInfo]
    command_info_array: Array[CommandInfoBasic]
    unchecked_event_achievement_id: int
