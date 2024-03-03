"""抄的URA"""

from .database import DataBase
from .database.skill_manager import SkillData
from module.umamusume.context import UmamusumeContext
import bot.base.log as logger

log = logger.get_logger(__name__)

DEBUG = True
MAX_RETRY = 30


def ura_script_cultivate_learn_skill(ctx: UmamusumeContext,
                                     learn_skill_list: list[list[str]],
                                     learn_skill_blacklist: list[str]
                                     ):
    from .cultivate import ura_parse_basic_information, context_copy
    origin_ctx = ctx
    ctx = context_copy(ctx)
    ura_parse_basic_information(ctx)  # 刷新下状态
    ctx.cultivate_detail.turn_info.log_turn_info(False, True)
    # 找出最佳技能
    target_skill_list = []
    learn = parse_skill_tips_response(ctx,
                                      normalize_priority_and_blacklist(learn_skill_list),
                                      normalize_priority_and_blacklist(learn_skill_blacklist))
    learnt_id = [x.skill_id for x in ctx.cultivate_detail.turn_info.learnt_skill_list]
    for skill in learn:
        if skill.rate == 2 and skill.rarity == 1:  # "◎" skills or inherent skills
            if skill.inferior is not None and skill.inferior.id not in learnt_id:  # "○" unlearn
                if skill.inferior.inferior is not None and skill.inferior.inferior.id in learnt_id:  # got "×"
                    target_skill_list.append(skill.inferior.inferior.name_while_learning)
                target_skill_list.append(skill.inferior.name_while_learning)
        if skill.rate == 1 and skill.rarity == 1:  # "○" and normal skills:
            if skill.inferior is not None and skill.inferior.id in learnt_id:  # got "×"
                target_skill_list.append(skill.inferior.name_while_learning)
        target_skill_list.append(skill.name_while_learning)

    # 点技能
    import time
    retry = 0
    while True:
        img = ctx.ctrl.get_screen()
        found = find_skill(origin_ctx, img, target_skill_list, learn_any_skill=False)
        if len(target_skill_list) == 0:
            break
        if found:  # 针对一个技能点多次的情况，找到并点到了先不翻页
            continue
        retry += 1
        if retry > MAX_RETRY:
            log.warning(f"以下技能没找到: %s", target_skill_list)
            if DEBUG:
                raise
            else:
                break
        if retry * 2 < MAX_RETRY:
            ctx.ctrl.swipe(x1=23, y1=1000, x2=23, y2=636, duration=1000, name="")
        else:
            ctx.ctrl.swipe(x1=23, y1=636, x2=23, y2=1000, duration=1000, name="")
        time.sleep(1)

    origin_ctx.cultivate_detail.learn_skill_done = True
    origin_ctx.cultivate_detail.turn_info.turn_learn_skill_done = True


def normalize_priority_and_blacklist(skills: list[str | list[str]]) -> list[SkillData | list[SkillData]]:
    if not skills:
        return []
    if isinstance(skills[0], str):
        return normalize_skill_list(skills)
    return list(filter(None, map(normalize_skill_list, skills)))


def normalize_skill_list(skills: list[str]) -> list[SkillData]:
    return list(filter(None, map(try_get_skill_by_name, skills)))


def try_get_skill_by_name(skill: str) -> SkillData | None:
    suspect = DataBase.get_skill_by_name(skill)
    if suspect:
        return suspect
    return DataBase.get_skill_by_name(skill + '○')


def parse_skill_tips_response(ctx: UmamusumeContext,
                              target_list: list[list[SkillData]],
                              black_list: list[SkillData]):
    """这段全抄的URA"""
    total_sp = ctx.cultivate_detail.turn_info.uma_attribute.skill_point
    skills = DataBase.skills.apply(ctx.cultivate_detail.turn_info)
    tips = DataBase.skills.calculate_skill_score_cost(ctx, skills,
                                                      DataBase.talent_skill[
                                                          ctx.cultivate_detail.uma_id], True,
                                                      target_list=target_list,
                                                      black_list=black_list)
    # TODO 进化部分以后再说
    dp_result = DataBase.skills.dp(tips, total_sp)
    learn = dp_result[0]
    will_learn_point = sum(x.actual_grade for x in learn)
    status_point = (DataBase.status_to_point[ctx.cultivate_detail.turn_info.uma_attribute.speed] +
                    DataBase.status_to_point[ctx.cultivate_detail.turn_info.uma_attribute.stamina] +
                    DataBase.status_to_point[ctx.cultivate_detail.turn_info.uma_attribute.power] +
                    DataBase.status_to_point[ctx.cultivate_detail.turn_info.uma_attribute.will] +
                    DataBase.status_to_point[ctx.cultivate_detail.turn_info.uma_attribute.intelligence])
    learnt_point = 0
    for learnt in ctx.cultivate_detail.turn_info.learnt_skill_list:
        if 1000000 < learnt.skill_id < 2000000:  # 嘉年华&LoH技能
            continue
        if str(learnt.skill_id).startswith('1') and 100000 < learnt.skill_id < 200000:  # 3*固有
            learnt_point += 170 * learnt.level
        elif len(str(learnt.skill_id)) == 5:  # 2*固有
            learnt_point += 120 * learnt.level
        else:
            if skills[learnt.skill_id] is None:
                continue
            learnt_point += skills[learnt.skill_id].actual_grade
    total_point = will_learn_point + learnt_point + status_point
    this_rank = None
    next_rank_point = 0

    def get_rank(_rank: str) -> str:
        result = ""
        flag = False
        for char in _rank:
            if char == '[':
                flag = False
                continue
            elif char == ']':
                flag = True
                continue
            if flag:
                result += char
        return result

    for rank in DataBase.grade_to_rank:
        if rank.min_value <= total_point <= rank.max_value:
            this_rank = get_rank(rank.rank)
            next_rank_point = rank.max_value + 1
            break
    print(
        f"预测总分: {learnt_point}(已学习技能) + {will_learn_point}(即将学习技能) + {status_point}(属性) = {total_point}({this_rank})")
    print(f"距离下一阶还差{next_rank_point - total_point}分")
    print("计划学习: ", end='')
    for x in learn:
        print(x, end=', ')
    print(f"\n现有技能点{total_sp}，学习技能后剩余{dp_result[2]}")
    return learn


def find_skill(ctx: UmamusumeContext, img, skill: list[str], learn_any_skill: bool) -> bool:
    """源自cultivate_task.parse, 由于识别问题需要魔改一下"""
    import re
    import cv2
    from bot.recog.image_matcher import image_match
    from bot.recog.ocr import ocr_line, find_similar_text
    from module.umamusume.asset import REF_SKILL_LIST_DETECT_LABEL, REF_SKILL_LEARNED
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    find = False
    while True:
        match_result = image_match(img, REF_SKILL_LIST_DETECT_LABEL)
        if match_result.find_match:
            pos = match_result.matched_area
            pos_center = match_result.center_point
            if 460 < pos_center[0] < 560 and 450 < pos_center[1] < 1050:
                skill_info_img = img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 470: pos[1][0] + 150]
                if not image_match(skill_info_img, REF_SKILL_LEARNED).find_match:
                    skill_name_img = skill_info_img[10: 47, 100: 445]
                    org_text = ocr_line(skill_name_img)
                    text = org_text.replace("曙", '踌躇').replace("凌房XDRIVE!", '凌厉×DRIVE！')  # 不知道咋搞，只能这样了
                    text = text.replace("（", "").replace("）", "")  # 诡计前后会混淆
                    text = text.replace("胜利著飞扑", "胜利者☆飞扑")
                    text = text.replace("万与力", "十万马力")
                    if text in ("领跑", "跟前", "居中", "后追"):
                        text += '踌躇'
                    result = find_similar_text(text, skill, 0.83)
                    if DEBUG:
                        print(org_text + "->" + text + "->" + result)  # DEBUG
                    if result != "" or learn_any_skill:
                        tmp_img = ctx.ctrl.get_screen()
                        pt_text = re.sub("\\D", "", ocr_line(tmp_img[400: 440, 490: 665]))
                        skill_pt_cost_text = re.sub("\\D", "", ocr_line(skill_info_img[69: 99, 525: 588]))
                        if pt_text != "" and skill_pt_cost_text != "":
                            pt = int(pt_text)
                            skill_pt_cost = int(skill_pt_cost_text)
                            if pt >= skill_pt_cost:
                                ctx.ctrl.click(match_result.center_point[0] + 128, match_result.center_point[1],
                                               "加点技能：" + text)
                                if result in skill:
                                    skill.remove(result)
                                ctx.cultivate_detail.learn_skill_selected = True
                                find = True

            img[match_result.matched_area[0][1]:match_result.matched_area[1][1],
                match_result.matched_area[0][0]:match_result.matched_area[1][0]] = 0

        else:
            break
    return find
