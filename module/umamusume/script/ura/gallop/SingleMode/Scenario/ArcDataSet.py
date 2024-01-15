"""LArc"""
from ... import Data, Array
from ..CommandInfo import CommandInfoBasic
from ..FreeDataSet import RivalRaceInfo as ArcRivalRaceInfo
from ..CommandInfo import ParamsIncDecInfo as ArcParamsIncDecInfo


class ArcPotentialProgress(Data):
    condition_id: int
    total_count: int
    current_count: int


class ArcRivalPotential(Data):
    potential_id: int
    level: int


class ArcPotential(ArcRivalPotential):
    progress_array: Array[ArcPotentialProgress]


class ArcSelectionPeff:
    effect_num: int
    effect_group_id: int
    effect_value: int


class ArcInfo(Data):
    approval_rate: int
    potential_array: Array[ArcPotential]


class ArcRival(Data):
    chara_id: int
    speed: int
    stamina: int
    power: int
    guts: int
    wiz: int
    command_id: int
    rival_boost: int
    star_lv: int
    rank: int
    approval_point: int
    potential_array: Array[ArcRivalPotential]
    selection_peff_array: Array[ArcSelectionPeff]


class ArcSelectionRivalInfo(Data):
    chara_id: int
    mark: int
    win_approval_point: int
    lose_approval_point: int
    rival_win_approval_point: int
    rival_lose_approval_point: int


class ArcSelectionInfo(Data):
    all_win_approval_point: int
    params_inc_dec_info_array: Array[ArcParamsIncDecInfo]
    selection_rival_info_array: Array[ArcSelectionRivalInfo]
    is_special_match: int
    bonus_params_inc_dec_info_array: Array[ArcParamsIncDecInfo]


class ArcRaceHistory(Data):
    race_num: int
    turn: int
    result_rank: int


class ArcCommandInfo(CommandInfoBasic):
    add_global_exp: int


class ArcEvaluationInfo(Data):
    target_id: int
    chara_id: int


class NotUpArcParameterInfo(Data):
    rival_boost_chara_id_array: Array[int]
    all_rival_boost_flag: bool


class ArcDataSet(Data):
    arc_info: ArcInfo
    arc_rival_array: Array[ArcRival]
    rival_race_info_array: Array[ArcRivalRaceInfo]
    selection_info: ArcSelectionInfo
    race_history_array: Array[ArcRaceHistory]
    command_info_array: Array[ArcCommandInfo]
    evaluation_info_array: Array[ArcEvaluationInfo]
    not_up_arc_parameter_info: NotUpArcParameterInfo
