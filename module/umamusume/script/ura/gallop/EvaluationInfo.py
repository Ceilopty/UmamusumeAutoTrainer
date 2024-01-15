from . import Data, Array


class GroupOutingInfo(Data):
    chara_id: int
    is_outing: int
    story_step: int


class EvaluationInfo(Data):
    target_id: int
    training_partner_id: int
    evaluation: int
    is_outing: int
    story_step: int
    is_appear: int
    group_outing_info_array: Array[GroupOutingInfo]
