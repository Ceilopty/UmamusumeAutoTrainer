from enum import Enum


class ScenarioType(Enum):
    SCENARIO_TYPE_UNKNOWN = 0
    SCENARIO_TYPE_URA = 1


class SupportCardType(Enum):
    SUPPORT_CARD_TYPE_UNKNOWN = 0
    SUPPORT_CARD_TYPE_SPEED = 1
    SUPPORT_CARD_TYPE_STAMINA = 2
    SUPPORT_CARD_TYPE_POWER = 3
    SUPPORT_CARD_TYPE_WILL = 4
    SUPPORT_CARD_TYPE_INTELLIGENCE = 5
    SUPPORT_CARD_TYPE_FRIEND = 6
    SUPPORT_CARD_TYPE_GROUP = 7
    SUPPORT_CARD_TYPE_NPC = 10

    def __str__(self):
        return {1: '速', 2: '耐', 3: '力', 4: '根', 5: '智', 6: '友', 7: '队', 10: 'NPC', 0: "未知"}.get(self.value, "")


class SupportCardFavorLevel(Enum):
    SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN = 0
    SUPPORT_CARD_FAVOR_LEVEL_1 = 1
    SUPPORT_CARD_FAVOR_LEVEL_2 = 2
    SUPPORT_CARD_FAVOR_LEVEL_3 = 3
    SUPPORT_CARD_FAVOR_LEVEL_4 = 4

    def __str__(self):
        return {1: '松', 2: '绿', 3: '金', 4: '满', 0: "未知"}.get(self.value, "")


class TrainingType(Enum):
    TRAINING_TYPE_UNKNOWN = 0
    TRAINING_TYPE_SPEED = 1
    TRAINING_TYPE_STAMINA = 2
    TRAINING_TYPE_POWER = 3
    TRAINING_TYPE_WILL = 4
    TRAINING_TYPE_INTELLIGENCE = 5

    def __str__(self):
        return {1: '速', 2: '耐', 3: '力', 4: '根', 5: '智', 0: "未知"}.get(self.value, "")


class MotivationLevel(Enum):
    MOTIVATION_LEVEL_UNKNOWN = 0
    MOTIVATION_LEVEL_1 = 1
    MOTIVATION_LEVEL_2 = 2
    MOTIVATION_LEVEL_3 = 3
    MOTIVATION_LEVEL_4 = 4
    MOTIVATION_LEVEL_5 = 5

    def __str__(self):
        return {1: '絶不調', 2: '不調', 3: '普通', 4: '好調', 5: '絶好調', 0: "未知"}.get(self.value, "")


class TurnOperationType(Enum):
    TURN_OPERATION_TYPE_UNKNOWN = 0
    TURN_OPERATION_TYPE_TRAINING = 1
    TURN_OPERATION_TYPE_REST = 2
    TURN_OPERATION_TYPE_MEDIC = 3
    TURN_OPERATION_TYPE_TRIP = 4
    TURN_OPERATION_TYPE_RACE = 5

    def __str__(self):
        return {1: '训练', 2: '休息', 3: '医务室', 4: '外出', 5: '赛事', 0: "未知"}.get(self.value, "")


class SupportCardUma(Enum):
    SUPPORT_CARD_UMA_UNKNOWN = 0
    SUPPORT_CARD_UMA_AKIKAWA = 1
    SUPPORT_CARD_UMA_REPORTER = 2


class RaceTacticType(Enum):
    RACE_TACTIC_TYPE_UNKNOWN = 0
    RACE_TACTIC_TYPE_BACK = 1
    RACE_TACTIC_TYPE_MIDDLE = 2
    RACE_TACTIC_TYPE_FRONT = 3
    RACE_TACTIC_TYPE_ESCAPE = 4


class Condition(Enum):
    CONDITION_RENSHUUJOUZU_MARU = 10
    CONDITION_AIKYOU = 8
    CONDITION_CHUUMOKUKABU = 9
    CONDITION_KIREMONO = 7
    CONDITION_KOUUNTAISHITSU = 26
    CONDITION_POSITIVESHIKOU = 25
    CONDITION_YOFUKASHIGIMI = 1
    CONDITION_RENSHUUBETA = 6
    CONDITION_NAMAKEGUSE = 2
    CONDITION_FUTORIGIMI = 4
    CONDITION_KATAZUTSUU = 5
    CONDITION_HADAARE = 3
    CONDITION_CHIISANAHOKOROBI = 12
    CONDITION_TAIRINNOKAGAYAKI = 13
    CONDITION_RENSHUUJOUZU_NIJUUMARU = 11
    CONDITION_FANTONOYAKUSOKU_HOKUTOU = 15
    CONDITION_FANTONOYAKUSOKU_HOKKAIDO = 14
    CONDITION_FANTONOYAKUSOKU_NAMAYAMA = 16
    CONDITION_FANTONOYAKUSOKU_KANSAI = 17
    CONDITION_FANTONOYAKUSOKU_KOKURA = 18
    CONDITION_GLASSNOASHI = 20
    CONDITION_AYASHIIKUMOYUKI = 21
    CONDITION_FANTONOYAKUSOKU_KAWASAKI = 22
    CONDITION_MADAMADAJUNBICHUU = 19
    CONDITION_EIYUUNOKOUKI = 23
    CONDITION_HARUMATSUTSUBOMI = 24
    CONDITION_JOUNETSUZONE = 100
    CONDITION_ALL = 0

    def __str__(self):
        return {1: '夜ふかし気味', 2: 'なまけ癖', 3: '肌あれ', 4: '太り気味', 5: '片頭痛', 6: '練習ベタ', 7: '切れ者', 8: '愛嬌◯',
                9: '注目株', 10: '練習上手◯', 11: '練習上手◎', 12: '小さなほころび', 13: '大輪の輝き', 14: 'ファンとの約束・北海道',
                15: 'ファンとの約束・北東', 16: 'ファンとの約束・中山', 17: 'ファンとの約束・関西', 18: 'ファンとの約束・小倉',
                19: 'まだまだ準備中', 20: 'ガラスの脚', 21: '怪しい雲行き', 22: 'ファンとの約束・川崎', 23: '英雄の光輝',
                24: '春待つ蕾', 25: 'ポジティブ思考', 26: '幸運体質', 100: "情熱ゾーン", 0: "全部"}.get(self.value, "")
    __repr__ = __str__
