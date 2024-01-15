from . import Data, Array
from .Skill import SkillTips


class _NotGainCharaEffect(Data):
    effected_chara_effect_id: int
    not_gain_chara_effect_id: int


class NotDownParameterInfo(Data):
    evaluation_chara_id_array: Array[int]


class NotUpParameterInfo(NotDownParameterInfo):
    status_type_array: Array[int]
    chara_effect_id_array: Array[int]
    skill_id_array: Array[int]
    skill_tips_array: Array[SkillTips]
    skill_lv_id_array: Array[int]
    command_lv_array: Array[int]
    has_chara_effect_chara_id_array: Array[int]
    unsupported_evaluation_chara_id_array: Array[int]
    not_gain_chara_effect_array: Array[_NotGainCharaEffect]
