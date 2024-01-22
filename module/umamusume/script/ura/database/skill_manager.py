from ..parse import TurnInfo
from ..database.klass import Propers, Skill, _Nameable
from copy import copy


class SkillData(_Nameable):
    """养成结束即将学习的技能"""
    _name_index = 47
    j_name: str
    id: int
    group_id: int
    rarity: int
    rate: int
    grade: int
    cost: int
    display_order: int
    propers: tuple[Propers]

    def __init__(self, skill: Skill | dict):
        if not isinstance(skill, Skill):
            skill = Skill(skill)
        self.j_name = skill.j_name
        self.id = skill.id
        self.group_id = skill.group_id
        self.rarity = skill.rarity
        self.rate = skill.rate
        self.grade = skill.grade
        self.cost = skill.cost
        self.display_order = skill.display_order
        self.propers = skill.propers

    @property
    def deconstruction(self):
        return self.group_id, self.rarity, self.rate

    def clone(self):
        clone = copy(self)
        if hasattr(self, "superior"):
            if self.superior is not None:
                clone.superior = self.superior.clone()
            else:
                clone.superior = None
        if hasattr(self, "inferior"):
            if self.inferior is not None:
                clone.inferior = self.inferior.clone()
            else:
                clone.inferior = None
        return clone


class SkillManager(list):
    @property
    def id_map(self):
        return {x.id: x for x in self}

    @property
    def rate_map(self):
        return {(x.group_id, x.rarity, x.rate): x for x in self}

    @property
    def rarity_map(self):
        return {(x.group_id, x.rarity):
                [y for y in self if y.group_id == x.group_id and y.rarity == x.rarity] for x in self}

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) == 3:
                item: tuple[int, int, int]
                return self.rate_map.get(item)
            elif len(item) == 2:
                item: tuple[int, int]
                return self.rarity_map.get(item)
        if isinstance(item, int):
            res = self.id_map.get(item)
            if res:
                return res
        return super().__getitem__(item)

    def get_all_by_group_id(self, group_id):
        return [x for x in self if x.group_id == group_id]


class SkillManagerGenerator:
    default: SkillManager
    __new__ = None

    @staticmethod
    def apply_hint(skill: SkillData, chara_info: TurnInfo, level: int):
        cut = 10 if 7 in chara_info.chara_effect_id_array else 0
        off = {0: 0, 1: 10, 2: 20, 3: 30, 4: 35, 5: 40}.get(level)
        skill.cost = (skill.cost * (100 - off - cut) + 50) // 100

    @staticmethod
    def apply_proper(skill: SkillData, chara_info: TurnInfo):
        def apply_proper_level(grade: int, level: int) -> int:
            match level:
                case 8 | 7:
                    return round(grade * 1.1)  # S, A
                case 6 | 5:
                    return round(grade * 0.9)  # B, C
                case 4 | 3 | 2:
                    return round(grade * 0.8)  # D, E, F
                case 1:
                    return round(grade * 0.7)  # G
                case _:
                    return 0

        def apply_proper_from_propers(proper: Propers) -> int:
            grade = skill.grade
            # 泥地技能似乎不受适性影响，gamewith报告为1.0，bwiki报告为+120，按gw的试试
            # grade = apply_proper_level(grade, chara_info.proper_info[0][proper.ground.value - 1])
            grade = apply_proper_level(grade, chara_info.proper_info[1][proper.distance.value - 1])
            grade = apply_proper_level(grade, chara_info.proper_info[2][proper.style.value - 1])
            return grade
        if skill.propers:
            skill.grade = max(map(apply_proper_from_propers, skill.propers))

    @classmethod
    def apply(cls, chara_info: TurnInfo) -> SkillManager:
        skills = [skill.clone() for skill in cls.default]
        for skill in skills:
            level = [tip.level for tip in chara_info.skillTips
                     if tip.group_id == skill.group_id and tip.rarity == skill.rarity]
            level = level[0] if level else 0
            # 计算折扣
            cls.apply_hint(skill, chara_info, level)
            # 计算分数
            cls.apply_proper(skill, chara_info)
        for skill in skills:
            # 同组技能
            group = [s for s in skills if s.group_id == skill.group_id]
            if group:
                # 同稀有度的上位技能(双圈白)
                normal_superior = [s for s in group
                                   if s.rarity == skill.rarity
                                   and s.rate == skill.rate + 1]
                # 高一级稀有度的上位技能(金)
                rare_superior = [s for s in group
                                 if s.rarity == skill.rarity + 1
                                 and s.rate == skill.rate + 1]
                if normal_superior:
                    skill.superior = normal_superior[0]
                elif rare_superior:
                    skill.superior = rare_superior[0]
                else:
                    skill.superior = None

                # 同稀有度的下位技能(单圈白)
                normal_inferior = [i for i in group
                                   if i.rarity == skill.rarity
                                   and i.rate == skill.rate - 1]
                # 低一级稀有度的下位技能(白/双圈白)
                lower_inferior = [i for i in group
                                  if i.rarity == skill.rarity - 1
                                  and i.rate == skill.rarity - 1]
                if normal_inferior:
                    skill.inferior = normal_inferior[0]
                elif lower_inferior:
                    skill.inferior = lower_inferior[0]
                else:
                    skill.inferior = None
        for skill in sorted(skills, key=lambda x: x.rate, reverse=True):
            inferior = skill.inferior
            while inferior is not None:
                # 学了
                # if [learnt for learnt in chara_info.skills if learnt.skill_id == inferior.id]:
                if any(filter(lambda learnt: learnt.skill_id == inferior.id, chara_info.skills)):
                    skill.grade -= inferior.grade
                    break
                else:
                    skill.cost += inferior.cost
                    inferior = inferior.inferior
        return SkillManager(skills)
