class SkillNotFoundError(Exception):
    pass


class Skill:
    """技能规范化
    先放个架子，细节有空再说"""
    group_id: int
    name: str
    rarity: int
    id: int

    def __init__(self, skill: str):
        from ..database import DataBase
        self._name_raw = skill
        self.skill = DataBase.get_skill_by_name(skill)
        if not self.skill:
            self.skill = DataBase.get_skill_by_name(skill + '○')
        if not self.skill:
            raise SkillNotFoundError(skill)
        self.group_id = self.skill.group_id
        self.rarity = self.skill.rarity
        self.name = self.skill.name
        self.id = self.skill.id

    def __str__(self):
        return self.name or self._name_raw or ''

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Skill):
            return NotImplemented
        return self.id == other.id
