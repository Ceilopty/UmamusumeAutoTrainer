class Skill:
    """技能规范化
    先放个架子，细节有空再说"""
    def __init__(self, skill: str):
        self.skill = skill

    def __str__(self):
        return str(self.skill)

    __repr__ = __str__
