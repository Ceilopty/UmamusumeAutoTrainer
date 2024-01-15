from . import Data, Array
from .EvaluationInfo import GroupOutingInfo


class GuestOutingInfo(Data):
    support_card_id: int
    story_step: int
    group_out_info_array: Array[GroupOutingInfo]
