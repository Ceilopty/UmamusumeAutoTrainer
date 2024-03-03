from ....context import UmamusumeContext, TurnInfo, Condition
from ..database.klass import Propers, Skill, _Nameable, TalentSkill
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
    actual_grade: int

    def __init__(self, skill: Skill | dict):
        if not isinstance(skill, Skill):
            skill = Skill(skill)
        self._j_name = skill.j_name
        self.id = skill.id
        self.group_id = skill.group_id
        self.rarity = skill.rarity
        self.rate = skill.rate
        self.grade = skill.grade
        self.cost = skill.cost
        self.display_order = skill.display_order
        self.propers = skill.propers
        self.inferior = None
        self.superior = None
        self.actual_grade = self.grade

    @property
    def name_while_learning(self):
        if self.rate == -1:
            return "消除" + self.name
        return self.name.replace("（", "").replace("）", "")

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

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id


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
                [y for y in self if y.group_id == x.group_id and y.rarity == x.rarity]
                for x in self}

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

    def deconstruction(self, skill_id: int) -> (int, int, int):
        return self[skill_id].deconstruction


class SkillManagerGenerator:
    default: SkillManager
    __new__ = None

    @staticmethod
    def apply_hint(skill: SkillData, chara_info: TurnInfo, level: int):
        cut = 10 if Condition.CONDITION_KIREMONO in chara_info.uma_condition_list else 0
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
            # 泥地技能似乎不受适性影响，game_with报告为1.0，b_wiki报告为+120，按gw的试试
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
            level = [tip.level for tip in chara_info.skill_hint_list
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
                # 负面技能的上位(单圈)
                superior_of_negative = [s for s in group
                                        if s.rarity == skill.rarity
                                        and s.rate == skill.rate + 2 == 1]
                if normal_superior:
                    skill.superior = normal_superior[0]
                elif rare_superior:
                    skill.superior = rare_superior[0]
                elif superior_of_negative:
                    skill.superior = superior_of_negative[0]
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
                # 同稀有度的下下位技能(×)
                negative_inferior = [i for i in group
                                     if i.rarity == skill.rarity
                                     and i.rate == skill.rate - 2 == -1]
                if normal_inferior:
                    skill.inferior = normal_inferior[0]
                elif lower_inferior:
                    skill.inferior = lower_inferior[0]
                elif negative_inferior:
                    skill.inferior = negative_inferior[0]
                else:
                    skill.inferior = None
        for skill in sorted(skills, key=lambda x: x.rate, reverse=True):
            inferior = skill.inferior
            while inferior is not None:
                # 学了
                # if [learnt for learnt in chara_info.learnt_skill_list if learnt.skill_id == inferior.id]:
                if any(filter(lambda learnt: learnt.skill_id == inferior.id, chara_info.learnt_skill_list)):
                    if inferior.rate == -1:
                        # 带有负面技能（未消除），则其上位一定未学
                        # 仅在第一次遇到时操作
                        if inferior.grade > 0:
                            break
                        inferior.grade = -inferior.grade
                        superior = inferior.superior
                        while superior is not None:
                            superior.grade += inferior.grade
                            superior.cost += inferior.cost
                            superior = superior.superior
                        break
                    skill.grade -= inferior.grade
                    break
                elif inferior.rate > 0:
                    skill.cost += inferior.cost
                    inferior = inferior.inferior
                else:
                    inferior.superior.inferior = None
                    break
        return SkillManager(skills)

    @staticmethod
    def calculate_skill_score_cost(ctx: UmamusumeContext,
                                   skills: SkillManager,
                                   talent_set: list[TalentSkill] | None,
                                   remove_inferiors: bool,
                                   target_list: list[list[SkillData]],
                                   black_list: list[SkillData]) -> list[SkillData]:
        """
        抄的URA的Handler.CalculateSkillScoreCost，按性价比排序技能。
        顺便优先找出target中的技能，排除black中的技能。
        当养成过程中学习技能时，若仅学习给定技能，则只返回target中有的技能；若赛前学习技能，则只返回target[0]中有的技能
        """
        has_unknown_skills = False
        tips_raw = ctx.cultivate_detail.turn_info.skill_hint_list
        tips_exist_in_database = [tip for tip in tips_raw if skills[tip.group_id, tip.rarity]]
        tips_not_exist_in_database = [tip for tip in tips_raw if not skills[tip.group_id, tip.rarity]]
        for tip in tips_not_exist_in_database:
            has_unknown_skills = True
            line_to_print = f"警告：未知技能，group_id={tip.group_id}, rarity={tip.rarity}"
            for rarity in range(10):
                maybe_inferior_skills = skills[tip.group_id, rarity]
                if maybe_inferior_skills:
                    for inferior_skill in maybe_inferior_skills:
                        line_to_print += f"，可能是 {inferior_skill.name} 的上位技能"
            print(f"[red]{line_to_print}[/]")
        # 翻译技能tips方便使用
        tips: list[SkillData] = []
        for tip in tips_exist_in_database:
            tips.extend(skills[tip.group_id, tip.rarity])
        tips = list(filter(lambda x: x.rate > 0, tips))
        # 添加天赋技能
        unknown_uma = False
        if talent_set:
            for talent in filter(lambda skill: skill.rank <= ctx.cultivate_detail.talent_level, talent_set):
                if not any(filter(lambda tip: tip.id == talent.skill_id, tips)) and \
                        not any(filter(lambda _learnt: _learnt.skill_id == talent.skill_id,
                                       ctx.cultivate_detail.turn_info.learnt_skill_list)):
                    tips.append(skills[talent.skill_id])
        else:
            unknown_uma = True
        # 添加上位技能缺少的下位技能（为方便计算切者技能点）
        for group in {x.group_id: list(filter(lambda tip: tip.group_id == x.group_id, tips))
                      for x in tips}.items():
            max_rarity = max(skill.rarity for skill in group[1])
            max_rate = max(skill.rate for skill in group[1])
            additional_skills = list(filter(lambda skill: (
                                            skill.rarity < max_rarity
                                            or skill.rate < max_rate)
                                            and skill.rate > 0,
                                            skills.get_all_by_group_id(group[0])))
            already_have = set(tip.id for tip in tips)
            tips.extend(skill for skill in additional_skills if skill.id not in already_have)
        # 当存在负面技能时添加自身及其上位
        for learnt in ctx.cultivate_detail.turn_info.learnt_skill_list:
            negative = skills[learnt.skill_id]
            if not negative.rate < 0:
                continue
            additional_skills = skills[negative.group_id, negative.rarity]
            already_have = set(tip.id for tip in tips)
            tips.extend(skill for skill in additional_skills if skill.id not in already_have)
        # 当存在已消除的负面技能时添加其上位
        for disabled in ctx.cultivate_detail.turn_info.disable_skill_id_array:
            negative = skills[disabled]
            if not negative.rate < 0:
                continue
            additional_skills = skills[negative.group_id, negative.rarity]
            already_have = set(tip.id for tip in tips)
            tips.extend(skill for skill in additional_skills if skill.id not in already_have and skill.id != disabled)
        if remove_inferiors:
            # 保证技能列表中的列表都是最上位技能（有下位技能则去除）
            # 理想中tips里应只保留最上位技能，其所有的下位技能都去除
            inferiors = []
            for tip in tips:
                inferiors.extend(skills.get_all_by_group_id(tip.group_id))
            temp = {x.id: x for x in inferiors}
            inferiors = list(temp.values())
            inferiors.sort(key=lambda x: x.rate, reverse=True)
            inferiors.sort(key=lambda x: x.rarity, reverse=True)
            inferiors = {x.group_id: list(filter(lambda tip: tip.group_id == x.group_id, inferiors))
                         for x in inferiors}
            inferiors = {x[0]: x[1] for x in inferiors.items() if x[1]}
            temp = []
            for k in inferiors:
                foo = list(filter(lambda tip: tip.group_id == k, tips))
                foo.sort(key=lambda x: x.rate, reverse=True)
                foo.sort(key=lambda x: x.rarity, reverse=True)
                if not foo:
                    continue
                foo = foo[1:]  # 跳过当前有的最高级的hint
                temp.extend(x.id for x in foo)
            tips = [tip for tip in tips if tip.id not in temp]  # 只保留最上位技能，下位技能去除
        # if

        # 把已买技能和它们的下位去掉
        for learnt in ctx.cultivate_detail.turn_info.learnt_skill_list:
            if 1000000 < learnt.skill_id < 2000000:  # 嘉年华&LoH技能
                continue

            skill: SkillData = skills[learnt.skill_id]
            if skill is None:
                has_unknown_skills = True
                print(f"[red]警告：未知已购买技能，id={learnt.skill_id}[/]")
                continue
            # 只学习了负面技能自身就不要动
            if skill.rate == -1:
                continue
            skill.cost = 9999999
            while hasattr(skill, 'inferior') and (inferior := skill.inferior):
                skill = inferior
                skill.cost = 9999999

        if unknown_uma:
            print(f"[red]未知马娘：{ctx.cultivate_detail.uma_id}，无法获取觉醒技能，请自己决定是否购买。[/]")
        if has_unknown_skills:
            print(f"[red]警告：存在未知技能[/]")

        # 寻找target和black中的技能
        # 黑名单全家拉黑，白名单只加指定技能
        # 黑名单直接学不起。白名单共五档，价值分别6-2倍。
        for black_skill in black_list:
            for dont_learn in skills.get_all_by_group_id(black_skill.group_id):
                dont_learn.cost = 9999999
                dont_learn.grade = -999999
        for level, priority_level in enumerate(target_list):
            for target_skill in priority_level:
                skills[target_skill.id].grade *= 6 - level

        # 育成中学习技能的调整
        if not ctx.cultivate_detail.cultivate_finish:
            if ctx.cultivate_detail.learn_skill_only_user_provided:
                group_ids = set(x.group_id for level in target_list for x in level)
            elif ctx.cultivate_detail.learn_skill_before_race and ctx.cultivate_detail.turn_info.racing:
                # 赛前仅学习第一级
                group_ids = set(x.group_id for level in target_list[0:1] for x in level)
            else:
                return tips
            for tip in tips:
                if tip.group_id not in group_ids:
                    for dont_learn in skills.get_all_by_group_id(tip.group_id):
                        if dont_learn.rate > 0:  # 负面技能不剔除
                            dont_learn.cost = 9999999
                            dont_learn.grade = -999999
        return tips

    @staticmethod
    def dp(tips: list[SkillData],
           total_sp: int):
        learn = []
        # 01背包变种
        _dp = [0] * (total_sp + 1)  # 多计算100pt，用于计算“边际性价比” 就算了吧 节约时间 py好慢的
        dp_log = []  # 记录dp时所选的技能，存技能Id
        for i in range(total_sp + 1):
            dp_log.append([])

        for i in range(len(tips)):
            s = tips[i]
            # 读取此技能可以点的所有情况
            superior_id = [0, 0, 0, 0]
            superior_cost = [99999, 99999, 99999, 99999]
            superior_grade = [-99999, -99999, -99999, -99999]

            superior_id[0] = s.id
            superior_cost[0] = s.cost
            superior_grade[0] = s.grade

            if superior_cost[0] != 0 and hasattr(s, 'inferior') and s.inferior is not None:
                s = s.inferior
                superior_id[1] = s.id
                superior_cost[1] = s.cost
                superior_grade[1] = s.grade
                if superior_id[1] != 0 and hasattr(s, 'inferior') and s.inferior is not None:
                    s = s.inferior
                    superior_id[2] = s.id
                    superior_cost[2] = s.cost
                    superior_grade[2] = s.grade
                    if superior_id[2] != 0 and hasattr(s, 'inferior') and s.inferior is not None:
                        s = s.inferior
                        superior_id[3] = s.id
                        superior_cost[3] = s.cost
                        superior_grade[3] = s.grade

            if superior_grade[0] == 0:
                superior_cost[0] = 99999
            if superior_grade[1] == 0:
                superior_cost[1] = 99999
            if superior_grade[2] == 0:
                superior_cost[2] = 99999
            if superior_grade[3] == 0:
                superior_cost[3] = 99999

            # 退化技能到最低级，方便选择
            for j in range(total_sp, -1, -1):
                # 背包五种选法
                # 0 - 不选
                # 1 - 只选此技能
                # 2 - 选这个技能和它的上一级技能
                # 3 - 选这个技能的最高位技（全点）
                choice = [0, 0, 0, 0, 0]
                choice[0] = _dp[j]
                choice[1] = _dp[j - superior_cost[0]] + superior_grade[0] if j - superior_cost[0] > 0 else -1
                choice[2] = _dp[j - superior_cost[1]] + superior_grade[1] if j - superior_cost[1] > 0 else -1
                choice[3] = _dp[j - superior_cost[2]] + superior_grade[2] if j - superior_cost[2] > 0 else -1
                choice[4] = _dp[j - superior_cost[3]] + superior_grade[3] if j - superior_cost[3] > 0 else -1

                # 判断是否为四种选法中的最优选择
                def is_best_option(index: int):
                    is_best = True
                    for k in range(5):
                        is_best = choice[index] >= choice[k] and is_best
                    return is_best

                if is_best_option(0):
                    _dp[j] = choice[0]
                elif is_best_option(1):
                    _dp[j] = choice[1]
                    dp_log[j][:] = dp_log[j - superior_cost[0]] + superior_id[0:1]
                elif is_best_option(2):
                    _dp[j] = choice[2]
                    dp_log[j][:] = dp_log[j - superior_cost[1]] + superior_id[1:2]
                elif is_best_option(3):
                    _dp[j] = choice[3]
                    dp_log[j][:] = dp_log[j - superior_cost[2]] + superior_id[2:3]
                elif is_best_option(4):
                    _dp[j] = choice[4]
                    dp_log[j][:] = dp_log[j - superior_cost[3]] + superior_id[3:4]
            # for j
        # for i
        # 读取最终选择的技能
        learn_skill_id = dp_log[total_sp]
        for _id in learn_skill_id:
            for skill in tips:
                inferior = skill.inferior
                more_inferior = inferior.inferior if inferior is not None else None
                most_inferior = more_inferior.inferior if more_inferior is not None else None
                if skill.id == _id:
                    learn.append(skill)
                    total_sp -= skill.cost
                    continue
                elif inferior is not None and inferior.id == _id:
                    learn.append(inferior)
                    total_sp -= inferior.cost
                    continue
                elif more_inferior is not None and more_inferior.id == _id:
                    learn.append(more_inferior)
                    total_sp -= more_inferior.cost
                    continue
                elif most_inferior is not None and most_inferior.id == _id:
                    learn.append(most_inferior)
                    total_sp -= most_inferior.cost
        learn.sort(key=lambda x: x.display_order)
        return learn, _dp, total_sp
