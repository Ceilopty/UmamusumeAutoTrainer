from .. import Array
from ..Skill import SkillTips, SkillUpgradeInfo
from .SupportCard import SingleModeSupportCard
from ..EvaluationInfo import EvaluationInfo
from ..TrainingLevelInfo import TrainingLevelInfo
from ..GuestOutingInfo import GuestOutingInfo
from .HorseCommonData import HorseCommonData


class SingleModeChara(HorseCommonData):
    chara_grade: int
    power: int

    vital: int
    max_speed: int
    max_stamina: int
    max_power: int
    max_wiz: int
    max_guts: int
    default_max_speed: int
    default_max_stamina: int
    default_max_power: int
    default_max_wiz: int
    default_max_guts: int
    max_vital: int

    fans: int
    race_program_id: int
    reserve_race_program_id: int
    race_running_style: int
    is_short_race: int
    disable_skill_id_array: Array[int]
    skill_tips_array: Array[SkillTips]
    support_card_array: Array[SingleModeSupportCard]
    succession_trained_chara_id_1: int
    succession_trained_chara_id_2: int

    turn: int
    skill_point: int
    short_cut_state: int
    state: int
    playing_state: int
    scenario_id: int
    route_id: int
    start_time: str
    evaluation_info_array: Array[EvaluationInfo]
    training_level_info_array: Array[TrainingLevelInfo]
    nickname_id_array: Array[int]
    chara_effect_id_array: Array[int]
    route_race_id_array: Array[int]
    guest_outing_info_array: Array[GuestOutingInfo]
    skill_upgrade_info_array: Array[SkillUpgradeInfo]
