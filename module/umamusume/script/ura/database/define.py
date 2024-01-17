from enum import Enum


class Proper(Enum):
    S = 8
    A = 7
    B = 6
    C = 5
    D = 4
    E = 3
    F = 2
    G = 1


class GroundType(Enum):
    NONE = 0
    TURF = 1  # SHIBA
    DIRT = 2


class DistanceType(Enum):
    NONE = 0
    SHORT = 1
    MILE = 2
    MIDDLE = 3
    LONG = 4


class StyleType(Enum):
    NONE = 0
    NIGE = 1
    SENKO = 2
    SASHI = 3
    OIKOMI = 4


class ConditionType(Enum):
    """master.mdb中的状态（142, 143）"""
    YOFUKASHIGIMI = 1
    NAMAKEGUSE = 2
    HADAARE = 3
    FUTORIGIMI = 4
    KATAZUTSUU = 5
    RENSHUUBETA = 6
    KIREMONO = 7
    AIKYOU_MARU = 8
    CHUUMOKUKABU = 9
    RENSHUUJOUZU_MARU = 10
    RENSHUUJOUZU_NIJUUMARU = 11
    CHIISANAHOKOROBI = 12
    TAIRINNOKAGAYAKI = 13
    FANTONOYAKUSOKU_HOKKAIDO = 14
    FANTONOYAKUSOKU_HOKUTOU = 15
    FANTONOYAKUSOKU_NAKAYAMA = 16
    FANTONOYAKUSOKU_KANSAI = 17
    FANTONOYAKUSOKU_KOKURA = 18
    MADAMADAJUNBICHUU = 19
    GLASSNOASHI = 20
    AYASHIIKUMOYUKI = 21
    FANTONOYAKUSOKU_KAWASAKI = 22
    EIYUUNOKOUKI = 23
    HARUMATSUTSUBOMI = 24
    POSITIVE_SHIKOU = 25
    KOUUNTAISHITSU = 26
    JOUNETSU_ZONE_TEAM_SIRIUS = 100
    JOUNETSU_ZONE_OUZANITSUDOISHIMONOTACHI = 101
    JOUNETSU_ZONE_SONISHITEMICHIBIKUMONO = 102


class WinsSaddle(Enum):
    """
    胜鞍
    single_mode_wins_saddle
    text_data_111
    """
    NONE = 0
    ARIMA_KINEN = 10  # 102301
    JAPAN_CAP = 11   # 101901
    NIPPON_DERBY = 12  # 101001
    TENNOUSHOU_HARU = 13  # 100601
    TAKARADZUKA_KINEN = 14  # 101201
    TENNOUSHOU_AKI = 15  # 101601
    KIKKASHOU = 16  # 101501
    OOSAKAHAI = 17  # 100301
    SATSUKISHOU = 18  # 100501
    OAKS = 19  # 100901
    TAKAMATSUMIYA_KINEN = 20   # 100201
    YASUDA_KINEN = 21  # 101101
    SPRINTER_STAKES = 22  # 101301
    MILE_CHAMPIONSHIP = 23  # 101801
    OUKASHOU = 24  # 100401
    VICTORIA_MILE = 25  # 100801
    ELISABETH_JOOUHAI = 26  # 101701
    NHK_MILE_CUP = 27  # 100701
    SHUUKASHOU = 28  # 101401
    CHAMPIONS_CUP = 29  # 102001
    FEBURARY_STAKES = 30  # 100101
    JBC_CLASSIC = 31  # 110501
    TOKYODAISHOUTEN = 32  # 110601
    ASAHIHAI_FUTURITY_STAKES = 33  # 102201
    HOPEFUL_STAKES = 34  # 102401
    HANSHIN_JUVENILE_FILLIES = 35  # 102101
    TEIOUSHOU = 36  # 110101
    JBC_SPRINT = 37  # 110401
    JAPAN_DIRT_DERBY = 38  # 110201
    JBC_LADIES_CLASSIC = 39  # 110301
    TAKARADZUKA_KINEN_ = 147  # 102501
    KIKKASHOU_ = 148  # 102601
    TENNOUSHOU_HARU_ = 153 
    SATSUKISHOU_ = 155
    JBC_LADIES_CLASSIC_ = 156
    JBC_SPRINT_ = 157
    JBC_CLASSIC_ = 158
    JBC_LADIES_CLASSIC__ = 159
    JBC_SPRINT__ = 160
    JBC_CLASSIC__ = 161
    JBC_LADIES_CLASSIC___ = 162
    JBC_SPRINT___ = 163
    JBC_CLASIC___ = 164
    KAWASAKI_KINEN = 165
    ZENNIPPON_JUNIOR_YUUSHUN = 166
    KAWASHI_KINEN = 167
    MILE_CHAMPIONSHIP_NANBUHAI = 168
    TENNOUSHOU_AKI__ = 184
    

class ScenarioType(Enum):
    """
    剧本，single_mode_scenario
    """
    URA = 1
    AOHARU = 2
    GRAND_LIVE = 3
    MAKE_A_NEW_TRACK = 4
    GRAND_MASTER = 5
    L_ARC = 6
    UNKNOWN = 0


class StoryState(Enum):
    UNKNOWN = -1
    FAIL = 0
    SUCCESS = 1
    GREAT_SUCCESS = 2
    NONE = 2147483647


class SkillType(Enum):
    """技能的性质(速度、加速度、恢复等)，仅用于计算技能进化条件"""
    Stat = 0
    "绿"
    Speed = 1
    "速度"
    Recovery = 2
    "蓝"
    Acceleration = 3
    "加速度"
    Lane = 8
    "跑道"
    Reaction = 7
    "出闸"
    Observation = 5
    "视野"
    Debuff = 6
    "红"
    Special = 12
    "特殊(大逃)"


class SkillCategory(Enum):
    """技能的种类（继承等）"""
    Inherent = 5


class SupportCardType(Enum):
    """
    支援卡种类
    support_card_data support_card_type
    """
    Normal = 1
    Friend = 2
    Group = 3


class CommandType(Enum):
    """
    养成指令种类
    command_id
    text_data 55
    """
    NotAvailable = -1
    Other = 0
    Speed = 101
    Stamina = 105
    Power = 102
    Guts = 103
    Wiz = 106
    Eat = 108
    Out = 109
    River = 301
    Karaoke = 302
    Jinja = 303
    Sea = 304
    Spring = 305
    SummerSpeed = 601
    SummerStamina = 602
    SummerPower = 603
    SummerGuts = 604
    SummerWiz = 605
    ParisSpeed = 1101
    ParisStamina = 1102
    ParisPower = 1103
    ParisGuts = 1104
    ParisWiz = 1105
    ParisSightSeeing1 = 1106
    ParisSightSeeing2 = 1107
    ParisSightSeeing3 = 1108
    Race = 401
    Friend = 390
    Rest = 701
    Hoken = 801


class SupportCardEffectType(Enum):
    """
    支援卡效果
    support_card_effect_table type 以及
    support_card_unique_effect type0 type1
    名称及说明见text_data 151 154
    """
    FriendBonus = 1
    MotivationEffect = 2
    SpeedBonus = 3
    StaminaBonus = 4
    PowerBonus = 5
    GutsBonus = 6
    WizBonus = 7
    TrainingBonus = 8
    InitSpeed = 9
    InitStamina = 10
    InitPower = 11
    InitGuts = 12
    InitWiz = 13
    InitFriendship = 14
    RaceBonus = 15
    FanBonus = 16
    HintLvBonus = 17
    HintPBonus = 18
    Rate = 19
    MaxSpeedUp = 20
    MaxStaminaUp = 21
    MaxPowerUp = 22
    MaxGutsUp = 23
    MaxWizUp = 24
    EventRecover = 25
    EventBonus = 26
    FailureRateDown = 27
    VitalCostDown = 28
    MinigameBonus = 29
    SkillPtBonus = 30
    WizRecoverBonus = 31


class Sex(Enum):
    Boba = 1
    Hinba = 2
