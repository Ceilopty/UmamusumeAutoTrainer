from .define import *
from typing import Dict as _Dict
from collections import namedtuple as _nt
from abc import abstractmethod as _abm, ABC as _ABC

FiveAttr = _nt('FiveAttr', ('speed', 'stamina', 'pow', 'guts', 'wiz'),
               defaults=(0, 0, 0, 0, 0))
Birthday = _nt('Birth', ('year', 'month', 'day'))
TimeMinMax = _nt('TimeMinMAx', ('min', 'max'))


class Color(int):
    def __new__(cls, *args, **kwargs):
        res = args[0]
        if isinstance(res, (bytes, str)):
            res = int(res, 16)
        return super().__new__(cls, res)

    @property
    def _t(self):
        return self // 256

    @property
    def r(self):
        return self._t // 256

    @property
    def g(self):
        return self._t % 256

    @property
    def b(self):
        return self % 256

    def __str__(self):
        return '%X' % self

    __repr__ = __str__


class TextData(dict):
    """
    文字信息
    text_data

    已知对应：
    1 系统
    2 错误
    3, 63 教程
    4 养成优骏少女全名
    5 养成优骏少女前缀
    6 角色名
    7 CV
    8 宿舍
    9 体重
    10, 24 道具说明
    13, 26 扭蛋
    14, 15 服装
    16 歌名
    17 词曲编
    23 道具名
    25 道具来源
    27 解说台词
    28, 32, 36 赛事全称(28为养成赛事)
    29, 33, 38 赛事简称(距离在33 2XXXX)
    31, 34 赛场
    35 地名
    39 商店交换
    40 交换详情
    41 功能解锁说明
    42, 49 课金道具名、说明
    47 技能名
    48 技能说明
    55 养成指令
    59 mob名
    64 报酬说明
    65, 66 称号、获得条件
    67 任务目标
    68, 69 过场Hint与小秘密标题、内容
    70 登录奖励
    75 支援卡全名
    76 支援卡前缀
    77 支援卡角色
    78 支援卡角色注音
    88 角色获得台词
    92 角色剧情标题
    93, 112 主线章节编号、标题
    94 主线各话标题
    95 主线相关角色、比赛等
    96 课金限定项目、主线各话编号
    97 绿帽建议
    111 胜鞍
    113 碎片
    114 碎片说明
    119, 120 剧本名称、说明
    121 段位
    128 歌曲说明
    130, 131 冠名、取得方式
    133 优胜rei Shoes GradeMedal
    136 观众AB 2人3人
    138 养成回合标题 1-25训练 26-28出行 29-33合宿训练 34合宿出行 35温泉 59-66后面剧本的
    139 理事长碎碎念
    140, 141 竞技场得分项目、说明
    142, 143 养成状态、说明
    144 角色简介
    147, 172 因子、说明
    148 竞技场Bonus
    150, 155 支援卡固有效果名（即卡名(76)）、说明
    151, 154 支援卡效果、说明
    152, 264 NPC
    157-162 角色生日、Scale、脚质、场地、距离适性、学部
    163-169 角色自我介绍、爱好、苦手、耳朵、尾巴、鞋码、家人
    170 角色名（档案）
    171 语音标题
    173 职业
    174 担当马娘
    175 档案项目
    258 My Rule
    259 手机壁纸
    260 赛前
    261 得意科目
    262 自满
    263 常购
    176, 197 碎钻回TP、RP
    177 抽奖奖品
    178-180 养成给的各种纪念品
    181 养成事件
    182 角色注音
    184 TP满提示
    185 RP满提示
    186 支援卡强化
    187, 188 限定活动、说明
    189 限定活动名称
    190 限定任务
    191 任务剧情标题
    192 地点
    193-195 队名等
    196 广告
    198-200 剧本链接卡说明
    201-204 解说实况台词
    205 嘚瑟
    206 外国比赛用语
    207-208 各种效果
    209 👆效果来源
    210 歌
    211 活动预告标题
    212 预告内容
    214 活动标题
    215-216 XX的马娘
    217 介绍条件
    218 青春杯比赛
    220 介绍谢语
    221 周年活动标题
    222 周年剧场标题
    223 地点
    225, 226 道具、说明
    227 对应193
    228 某台词
    229-232 实况解说往空里填的词
    233 564模式和鬼564模式
    234-236 报酬 ゲージ ShowTime
    237 剧本名
    238 效果
    239 模式说明
    240 后面剧本计数
    241-242 Racing Carnival
    243, 244 竞技场得分项、说明
    245 模式效果
    246 富士和564发奖
    247 看上去很强的Title
    248 Top Uma Dol Project
    249 247的条件
    250 Grand Live的Live
    251 同248
    252 GL育成任务
    253-256 说明
    257 CP出走
    265 目指せ！最強チーム
    266 广告
    267 LArc的种种
    268
    294 协助卡效果
    """

    def __init__(self, data: list):
        t = {}
        for datum in data:
            assert datum['id'] == datum['category']
            t.setdefault(datum['id'], {})
            t[datum['id']][datum['index']] = datum['text']
        super().__init__(t)


class Effect:
    """事件效果，text_data 238"""

    def __init__(self, effect: str):
        self._effect_raw = effect
        self._effect_list_raw = effect.split('、')


class Choice:
    option: str
    success_effect: Effect
    failed_effect: Effect

    def __init__(self, choice: list):
        self._choice_raw = choice[0].copy()
        self.option = self._choice_raw.get('Option')
        self.success_effect = Effect(self._choice_raw.get('SuccessEffect'))
        self.failed_effect = Effect(self._choice_raw.get('FailedEffect'))


class Event:
    """养成事件"""
    id: int
    "记录在master.mdb中的story_id"
    name: str
    "记录在master.mdb中的事件名(181)"
    trigger_name: str
    "事件所属角色，通用事件为马娘名，决胜服/S卡事件为全名"
    choices: list[Choice]

    def __init__(self, event: dict):
        self.id = event.get('Id')
        self.name = event.get('Name')
        self.trigger_name = event.get('TriggerName')
        self.choices = list(map(Choice, event.get('Choices')))
        self._event_raw = event.copy()

    def __str__(self):
        name = '  ' * (15 - len(self.name)) + self.name
        return "%s@%s: %s from %s" % (self.__class__.__name__,
                                      self.id,
                                      name,
                                      self.trigger_name)

    __repr__ = __str__


class SuccessEffect:
    select_index: int
    state: StoryState
    scenario: ScenarioType
    effect: Effect

    def __init__(self, choice: dict):
        self.select_index = choice.get('SelectIndex')
        self.state = StoryState(choice.get('State'))
        self.scenario = ScenarioType(choice.get('Scenario'))
        self.effect = Effect(choice.get('Effect'))
        self._choice_raw = choice.copy()


class SuccessEvent:
    id: int
    choice: list[list[SuccessEffect]]

    def __init__(self, success_event: dict):
        self.id = success_event.get('Id')
        self.choices = list(map(lambda x: list(map(SuccessEffect, x)), success_event.get('Choices')))
        self._success_event_raw = success_event.copy()

    def __str__(self):
        return "%s@%s with %s choice(s)" % (self.__class__.__name__,
                                            self.id,
                                            len(self.choices))

    __repr__ = __str__


class Meta(type):
    _cls = {}

    def __new__(metacls, name, base, attrs):
        if (args := (metacls, name, base, str(attrs.keys()))) not in metacls._cls:
            metacls._cls[args] = super().__new__(*args[:-1], attrs)
        return metacls._cls[args]

    def __call__(cls, *args, **kw):
        if kw:
            kw.update(cls.__dict__)
            return type(cls)(cls.__name__, cls.__bases__, kw)
        return super().__call__(*args)


class IdList(list):
    def __new__(cls, it, subscript='id'):
        self = super().__new__(cls, it)
        self._s = subscript
        return self

    def __init__(self, it, _s='id'):
        super().__init__(it)

    def __getitem__(self, s):
        s = getattr(s, self._s, s)
        return target[0] if (target := [x for x in self if getattr(x, self._s) == s]) \
            else super().__getitem__(s)


class Name:
    """角色名@6"""
    id: str
    "角色ID，通常为4位数字，且马娘均为1xxx"
    name: str
    "角色的本名，如美浦波旁"
    nickname: str
    "长度限定为2汉字的简称，如美浦波旁=>波旁"

    def __init__(self,
                 name: dict):
        self.id = name.get('Id')
        self.name = name.get('Name')
        self.nickname = name.get('Nickname')
        self._name_raw = name.copy()

    def __str__(self):
        return "%s @ %s aka %s" % (self.name,
                                   self.id,
                                   self.nickname)

    __repr__ = __str__


class Propers:
    def __init__(self, propers: dict):
        self.ground = GroundType(propers.get('Ground'))
        self.distance = DistanceType(propers.get('Distance'))
        self.style = StyleType(propers.get('Style'))
        self._propers_raw = propers.copy()

    def __str__(self):
        return str(self._propers_raw)

    __repr__ = __str__


class UpgradeSkill:
    def __init__(self, upgrade_skill: dict):
        self.condition_id = upgrade_skill.get('ConditionId')
        self.type = upgrade_skill.get('type')
        self.requirement = upgrade_skill.get('Requirement')
        self.additional_require = upgrade_skill.get('AdditionalRequirement')
        self._upgrade_skill_raw = upgrade_skill.copy()


class TalentSkill(metaclass=Meta):
    def __init__(self, talent_skill: dict):
        self.skill_id = talent_skill.get('SkillId')
        self.rank = talent_skill.get('Rank')
        self.upgrade_skills = dict(map(lambda x: (x[0], list(map(UpgradeSkill, x[1]))),
                                       talent_skill.get('UpgradeSkills').items()))
        self._talent_skill_raw = talent_skill.copy()

    def __str__(self):
        name = self.skills[self.skill_id].name if hasattr(self, 'skills') else ""
        return "%s@%s: %s" % (self.__class__.__name__,
                              self.skill_id,
                              name)

    __repr__ = __str__


class _Nameable(_ABC):
    """
    在text_data中有名字的类
    类应当有_name_index, 实例应当有id
    若设置了text_data,
    定义名称name为text_data[_name_index][id]
    """
    id: int
    "master.mdb中的id"

    @_abm
    def _name_index(self):
        """text_data中的id或category"""

    @staticmethod
    def set_text(text: dict):
        _Nameable._text = text

    @staticmethod
    def set_text_alter(text: dict):
        _Nameable._text_alter = text

    @property
    def name(self):
        """如果配置了text, 返回对应名称，否则返回空串"""
        try:
            string = self._text[self._name_index][self.id] if hasattr(self, '_text') else ''
        except KeyError:
            string = ''
        return string

    @property
    def name_alter(self):
        """如果配置了text_alter, 返回对应名称，否则返回空串"""
        try:
            string = self._text_alter[self._name_index][self.id] if hasattr(self, '_text_alter') else ''
        except KeyError:
            string = ''
        return string

    def __str__(self):
        return '%s: %s @ %4d' % (self.__class__.__name__,
                                 self.name, self.id)

    __repr__ = __str__


class TalentGroup:
    """
    各养成优骏少女觉醒所需材料
    card_talent_upgrade
    """


class SkillSet:
    pass


class Chara(_Nameable):
    """
    角色
    chara_data
    """
    name: Name
    id: int
    birth: Birthday
    last_year: int
    sex: Sex
    image_color_main: Color
    image_color_sub: Color
    ui_color_main: Color
    ui_color_sub: Color
    ui_training_color_1: Color
    ui_training_color_2: Color
    ui_border_color: Color
    ui_num_color_1: Color
    ui_num_color_2: Color
    ui_wipe_color_1: Color
    ui_wipe_color_2: Color
    ui_wipe_color_3: Color
    ui_speech_color_1: Color
    ui_nameplate_color_1: Color
    ui_nameplate_color_2: Color
    height: int
    bust: int
    scale: int
    skin: int
    shape: int
    socks: int
    personal_dress: int
    tail_model_id: int
    race_running_type: int
    ear_random_time: TimeMinMax
    tail_random_time: TimeMinMax
    story_ear_random_time: TimeMinMax
    story_tail_random_time: TimeMinMax
    attachment_model_id: int
    mini_mayu_shader_type: int
    start_date: int
    chara_category: int
    love_rank_limit: int
    _name_index = 6

    def __init__(self, chara: dict):
        self._chara = chara.copy()
        self.birth = Birthday(chara.pop('birth_year'),
                              chara.pop('birth_month'),
                              chara.pop('birth_day'))
        self.sex = Sex(chara.pop('sex'))
        for key in chara:
            if 'color' in key:
                setattr(self, key, Color(chara[key]))
            elif 'time' in key:
                time = getattr(self, key[:-4], TimeMinMax(0, 0))
                _min = time.min if 'max' in key else chara[key]
                _max = time.max if 'min' in key else chara[key]
                setattr(self, key[:-4], TimeMinMax(_min, _max))
            else:
                setattr(self, key, chara[key])


class _CharaBase(_Nameable):
    """
    与角色相关的类
    应具有chara_id
    若设置了角色表，可根据id返回角色
    """

    @_abm
    def _name_index(self):
        """text_data中的id或category"""

    def chara_id(self):
        """master.mdb中的角色id"""

    @staticmethod
    def set_chara(chara_list: IdList[Chara] | _Dict[int, Chara]):
        _CharaBase._chara = chara_list

    @property
    def chara(self):
        """如果配置了chara, 返回对应角色，否则返回空值"""
        return self._chara[self.chara_id] if hasattr(self, '_chara') else None

    def __str__(self):
        return '%s: %s%s @ %d' % (self.__class__.__name__,
                                  self.name, self.chara.name, self.id)

    __repr__ = __str__


class Card(_CharaBase):
    """
    养成优骏少女
    card_data
    全名4，前缀5
    """
    _name_index = 5
    id: int
    "master.mdb card_data中的id"
    name: str
    "前缀"
    chara_id: int
    "角色id"
    chara: Chara
    "角色"
    default_rarity: int
    "初始星数"
    limited_chara: bool
    "是否限定"
    available_skill_set: SkillSet
    "技能组"
    talent: FiveAttr
    "属性加成%"
    talent_group: TalentGroup
    "觉醒素材"
    running_style: StyleType
    "默认跑法"

    def __init__(self, card: dict):
        self._card = card.copy()
        self.limited_chara = bool(card.pop('limited_chara'))
        self.talent = FiveAttr(card.pop('talent_speed'),
                               card.pop('talent_stamina'),
                               card.pop('talent_pow'),
                               card.pop('talent_guts'),
                               card.pop('talent_wiz'))
        self.running_style = StyleType(card.pop('running_style'))
        for key in card:
            setattr(self, key, card[key])


class SupportCardEffect(dict):
    """
    协助卡效果数据，来源为support_card_effect_table

    # id: int
    # "master.mdb中的id，第一位为稀有度"
    # type: SupportCardEffectType
    # "效果类型"
    # limit: tuple[int]
    # "从初始到50级每5级的效果数值，共11项"
    """
    def __init__(self, effects: list[dict]):
        super().__init__(())
        for effect in effects:
            self.setdefault(effect['id'], {})
            self[effect['id']][effect['type']] = [effect['init']]
            limit = self[effect['id']][effect['type']]
            for lv in range(5, 51, 5):
                limit.append(effect[f'limit_lv{lv}'])


class SupportCardUniqueEffect:
    """
    协助卡特殊效果，即卡面固有加成
    来源为support_card_unique_effect
    卡片名称见text_data 150
    固有效果描述见text_data 155
    """
    id: int
    "master.mdb中的id，第一位为稀有度"
    lv: int
    "固有技能的发动等级"
    effect: _Dict[SupportCardEffectType, int]
    "效果：SupportCardEffectType: 数值"

    def __init__(self, effect: dict):
        self.id = effect['id']
        self.lv = effect['lv']
        self.effect = {
            effect['type_0']: effect['value_0'],
            effect['type_1']: effect['value_1'],
        }


class SupportCard(_CharaBase):
    _name_index = 76
    id: int
    command_id: CommandType
    support_card_type: SupportCardType

    def __init__(self, support: dict):
        self._support = support.copy()
        self.command_id = CommandType(support.pop('command_id'))
        self.support_card_type = SupportCardType(support.pop('support_card_type'))
        for key in support:
            setattr(self, key, support[key])


class SupportCardChara(SupportCard):
    _name_index = 77

    def __init__(self, support: SupportCard):
        super().__init__(support._support)


class Skill(_Nameable):
    """技能"""
    _name_index = 47
    name: str

    def __init__(self, skill: dict):
        self._j_name = skill.get('Name')
        self.id = skill.get('Id')
        self.group_id = skill.get('GroupId')
        self.rarity = skill.get('Rarity')
        self.rate = skill.get('Rate')
        self.grade = skill.get('Grade')
        self.cost = skill.get('Cost')
        self.display_order = skill.get('DisplayOrder')
        self.upgrade = skill.get('Upgrade')
        self.propers = tuple(map(Propers, skill.get('Propers')))
        self.category = skill.get('Category')
        self._skill_raw = skill.copy()

    @property
    def name(self):
        return super().name or self._j_name

    @property
    def name_alter(self):
        return super().name_alter or self._j_name

    @property
    def j_name(self):
        return self._j_name


class NullableIntStringDictionary(dict):
    def __getitem__(self, item):
        if item in self:
            return super().__getitem__(item)
        else:
            return "未知"


class GradeRank:
    id: int
    min_value: int
    "满足该评分所需的最低评价点"
    max_value: int
    "满足该评分所需的最高评价点"

    @property
    def rank(self):
        return {
            1: "[grey46]G[/]",
            2: "[grey46]G+[/]",
            3: "[mediumpurple3_1]F[/]",
            4: "[mediumpurple3_1]F+[/]",
            5: "[pink3]E[/]",
            6: "[pink3]E+[/]",
            7: "[deepskyblue3_1]D[/]",
            8: "[deepskyblue3_1]D+[/]",
            9: "[darkolivegreen3_1]C[/]",
            10: "[darkolivegreen3_1]C+[/]",
            11: "[palevioletred1]B[/]",
            12: "[palevioletred1]B+[/]",
            13: "[darkorange]A[/]",
            14: "[darkorange]A+[/]",
            15: "[lightgoldenrod2_2]S[/]",
            16: "[lightgoldenrod2_2]S+[/]",
            17: "[lightgoldenrod2_2]SS[/]",
            18: "[lightgoldenrod2_2]SS+[/]",
            19: "[mediumpurple1]U[mediumpurple2]G[/][/]",
            20: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]1[/][/]",
            21: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]2[/][/]",
            22: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]3[/][/]",
            23: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]4[/][/]",
            24: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]5[/][/]",
            25: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]6[/][/]",
            26: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]7[/][/]",
            27: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]8[/][/]",
            28: "[mediumpurple1]U[mediumpurple2]G[/][purple_2]9[/][/]",
            29: "[mediumpurple1]U[mediumpurple2]F[/][/]",
            30: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]1[/][/]",
            31: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]2[/][/]",
            32: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]3[/][/]",
            33: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]4[/][/]",
            34: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]5[/][/]",
            35: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]6[/][/]",
            36: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]7[/][/]",
            37: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]8[/][/]",
            38: "[mediumpurple1]U[mediumpurple2]F[/][purple_2]9[/][/]",
            39: "[mediumpurple1]U[mediumpurple2]E[/][/]",
            40: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]1[/][/]",
            41: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]2[/][/]",
            42: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]3[/][/]",
            43: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]4[/][/]",
            44: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]5[/][/]",
            45: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]6[/][/]",
            46: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]7[/][/]",
            47: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]8[/][/]",
            48: "[mediumpurple1]U[mediumpurple2]E[/][purple_2]9[/][/]",
            49: "[mediumpurple1]U[mediumpurple2]D[/][/]",
            50: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]1[/][/]",
            51: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]2[/][/]",
            52: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]3[/][/]",
            53: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]4[/][/]",
            54: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]5[/][/]",
            55: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]6[/][/]",
            56: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]7[/][/]",
            57: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]8[/][/]",
            58: "[mediumpurple1]U[mediumpurple2]D[/][purple_2]9[/][/]",
            59: "[mediumpurple1]U[mediumpurple2]C[/][/]",
            60: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]1[/][/]",
            61: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]2[/][/]",
            62: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]3[/][/]",
            63: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]4[/][/]",
            64: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]5[/][/]",
            65: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]6[/][/]",
            66: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]7[/][/]",
            67: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]8[/][/]",
            68: "[mediumpurple1]U[mediumpurple2]C[/][purple_2]9[/][/]",
            69: "[mediumpurple1]U[mediumpurple2]B[/][/]",
            70: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]1[/][/]",
            71: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]2[/][/]",
            72: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]3[/][/]",
            73: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]4[/][/]",
            74: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]5[/][/]",
            75: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]6[/][/]",
            76: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]7[/][/]",
            77: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]8[/][/]",
            78: "[mediumpurple1]U[mediumpurple2]B[/][purple_2]9[/][/]",
            79: "[mediumpurple1]U[mediumpurple2]A[/][/]",
            80: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]1[/][/]",
            81: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]2[/][/]",
            82: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]3[/][/]",
            83: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]4[/][/]",
            84: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]5[/][/]",
            85: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]6[/][/]",
            86: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]7[/][/]",
            87: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]8[/][/]",
            88: "[mediumpurple1]U[mediumpurple2]A[/][purple_2]9[/][/]",
            89: "[mediumpurple1]U[mediumpurple2]S[/][/]",
            90: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]1[/][/]",
            91: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]2[/][/]",
            92: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]3[/][/]",
            93: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]4[/][/]",
            94: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]5[/][/]",
            95: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]6[/][/]",
            96: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]7[/][/]",
            97: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]8[/][/]",
            98: "[mediumpurple1]U[mediumpurple2]S[/][purple_2]9[/][/]",
        }.get(self.id, "[mediumpurple1]US9[mediumpurple2]以上[/][/]")

    def __init__(self, _id, min_value, max_value):
        self.id = _id
        self.min_value = min_value
        self.max_value = max_value

    @classmethod
    def object_hook(cls, dct):
        return cls(dct['id'], dct['min_value'], dct['max_value'])


class BaseName:
    id: int
    "角色ID，通常为4位数字，且马娘均为1xxx"
    name: str
    "角色的本名，如美浦波旁"
    nick_name: str = "未知"
    "长度限定为2汉字的简称，如美浦波旁 = > 波旁"

    def __init__(self, _id: int, _name: str):
        self.id = _id
        self.name = _name

    @classmethod
    def object_hook(cls, dct: dict):
        self = cls(dct['Id'], dct['Name'])
        if 'Nickname' in dct:
            self.nick_name = dct['Nickname']
        return self

    def __str__(self):
        if hasattr(self, 'full_name'):
            return f"<{self.full_name} @ {self.id} aka {self.nick_name}>"
        return f"{self.name} @ {self.id} aka {self.nick_name}"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self)}>"


class SupportCardName(BaseName):
    chara_id: int
    "支援卡ID"
    type: int
    "支援卡的类型（速耐力根智友团）"

    @property
    def character_name(self) -> str:
        """角色的本名，如美浦波旁"""
        try:
            database = eval('DataBase')
        except NameError:
            database = None
        if database:
            return database.Names[self.chara_id]
        return ""

    @property
    def type_name(self):
        """支援卡的类型(如[速])"""
        return {101: "[速]", 102: "[力]", 103: "[根]", 105: "[耐]", 106: "[智]", 0: "[友]"}.get(self.type, '')

    @property
    def full_name(self):
        """支援卡的全名，如[ミッション『心の栄養補給』] ミホノブルボン"""
        return f"{self.name}{self.character_name}"

    @property
    def simple_name(self):
        """支援卡的简称，如[智]波旁，不考虑同类型同马娘支援卡的区分"""
        return f"{self.type_name}{self.nick_name}"

    def __init__(self, _id: int, _name: str, _chara_id: int, _type: int):
        super().__init__(_id, _name)
        self.chara_id = _chara_id
        self.type = _type

    @classmethod
    def object_hook(cls, dct: dict):
        self = cls(dct['Id'], dct['Name'], dct['CharaId'], dct['Type'])
        if 'Nickname' in dct:
            self.nick_name = dct['Nickname']
        return self


class UmaName(BaseName):
    chara_id: int
    "马娘ID"
    character_name = SupportCardName.character_name
    full_name = SupportCardName.full_name
    "马娘的全名，如[CODE：グラサージュ] ミホノブルボン"

    def __init__(self, _id: int, _name: str, _chara_id: int = 0):
        super().__init__(_id, _name)
        if _chara_id == 0:
            if (_strid := str(_id))[0] == '9':
                self.chara_id = int(_strid[1:5])
            else:
                self.chara_id = int(_strid[:4])
        else:
            self.chara_id = _chara_id

    @classmethod
    def object_hook(cls, dct: dict):
        self = cls(dct['Id'], dct['Name'], dct['CharaId'])
        if 'Nickname' in dct:
            self.nick_name = dct['Nickname']
        return self
