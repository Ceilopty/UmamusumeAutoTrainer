from . import Data


class SkillData(Data):
    skill_id: int
    level: int


class SkillTips(Data):
    group_id: int
    rarity: int
    level: int


class SkillUpgradeInfo(Data):
    condition_id: int
    total_count: int
    current_count: int
