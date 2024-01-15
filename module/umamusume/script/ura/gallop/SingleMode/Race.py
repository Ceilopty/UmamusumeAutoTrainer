from .. import Data, Array
from .HorseCommonData import HorseCommonData


class SingleModeRaceCondition(Data):
    program_id: int
    weather: int
    ground_condition: int


class RaceResult(Data):
    race_num: int
    turn: int
    result_rank: int


class RaceHorseRaceResult(SingleModeRaceCondition, RaceResult):
    viewer_id: int
    single_mode_chara_id: int
    frame_order: int
    running_style: int
    popularity: int
    result_time: int
    bashin_diff: int
    bashin_diff_from_top: int
    skill_activate_count: int
    start_dash_state: int
    motivation: int
    is_excitement: int
    is_running_alone: int
    last_straight_line_rank: int
    auto_continue_num: int
    state: int


class RaceHorseData(HorseCommonData):
    viewer_id: int
    owner_viewer_id: int
    trainer_name: str
    owner_trainer_name: str

    trained_chara_id: int
    nickname_id: int
    frame_order: int
    pow: int
    running_style: int
    race_dress_id: int
    chara_color_type: int
    npc_type: int
    final_grade: int
    popularity: int
    popularity_mark_array: Array[int]
    mob_id: int
    win_saddle_id_array: Array[int]
    race_result_array: Array[RaceHorseRaceResult]


class SingleModeRaceStartInfo(SingleModeRaceCondition):
    random_seed: int
    race_horse_data: Array[RaceHorseData]
    continue_num: int


class RaceRewardData(Data):
    item_type: int
    item_id: int
    item_num: int


class CharaRaceReward(Data):
    result_rank: int
    result_time: int
    race_reward: Array[RaceRewardData]
    race_reward_bonus: Array[RaceRewardData]
    race_reward_plus_bonus: Array[RaceRewardData]
    race_reward_bonus_win: Array[RaceRewardData]
    gained_fans: int
    campaign_id_array: Array[int]
