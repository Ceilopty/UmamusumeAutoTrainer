from enum import Enum
from ....define import Condition as _ConditionType


class UraPersonType(Enum):
    """
    0代表未加载（例如前两个回合的npc），
    1代表桐生院支援卡（R或SR都行），
    2代表普通支援卡，3绿帽，
    4理事长，5记者，6不带卡的桐生院，
    暂不支持其他友人/团队卡"""
    Unknown = 0
    KiryuuinS = 1
    Normal = 2
    HayakawaS = 3
    Akikawa = 4
    Otonashi = 5
    Kiryuuin = 6


class EventState(Enum):
    Unknown = -1
    Fail = 0
    Success = 1
    GreatSuccess = 2
    NONE = 2147483647


class OutType(Enum):
    Other = 0
    River = 1
    Karaoke = 2
    Jinja = 3


ConditionType = _ConditionType
