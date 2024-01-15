from .. import Data, Array
from ..Skill import SkillData


class HorseInfoBasic(Data):
    proper_distance_short: int
    proper_distance_mile: int
    proper_distance_middle: int
    proper_distance_long: int
    proper_running_style_nige: int
    proper_running_style_senko: int
    proper_running_style_sashi: int
    proper_running_style_oikomi: int
    proper_ground_turf: int
    proper_ground_dirt: int
    skill_array: Array[SkillData]
    stamina: int
    speed: int
    # power不一样
    guts: int
    wiz: int
    talent_level: int


class HorseCommonData(HorseInfoBasic):
    single_mode_chara_id: int
    card_id: int
    rarity: int
    motivation: int
