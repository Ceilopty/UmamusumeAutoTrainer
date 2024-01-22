"""
事件效果
充斥着大量个性化内容，可能需要经常维护。
不过大多数都对应无选项事件，无关痛痒。
"""
import os

from ...cultivate_task.event.parse import EventEffect as _Effect
from .define import ConditionType as _ConditionType
from .skill import Skill
from .chara import Chara, CharaNotFoundError, SupportCardChara


def _parse_event_raw(effect: str) -> _Effect:
    _debug = effect
    if effect.startswith("**") and effect.endswith("**"):
        return _Effect(other=effect)

    # 没啥歧义的误用，普遍的，在这里替换。容易出事的放在失败后。# 真没想到一个负号有那么多种
    # 先是部分替换
    rp = {
        # 状态的单圈是"◯"\25ef，技能的单圈是'○'\25cb
        "〇": '○',
        "◯」のヒント": "○」のヒント",
        "◯のヒント": "○のヒント",
        "◯」ヒント": "○」ヒント",
        "◯」+": "○」のヒントLv+",
        "◯』のヒント": "○』のヒント",
        "◯」スキルヒント": "○」のヒント",
        "◯」習得": "○」習得",
        "\u2212": "-",
        "\u2010": "-",
        "\uff0b": "+",
        "スキル+": "スキルPt+",
        "スキルpt+": 'スキルPt+',
        "の絆+": "の絆ゲージ+",
        "の絆ケージ": "の絆ゲージ",
        "の絆ゲージ↑": "の絆ゲージ+4",
        "の絆ゲージ+○": "の絆ゲージ+5",
        "のヒントLV": "のヒントLv",
        "のヒントlv": "のヒントLv",
        "のヒントLvL": "のヒントLv",
        "のヒント+": "のヒントLv+",
        "のヒントLv上昇": "のヒントLv+1",
        "」ヒントLv+": "」のヒントLv+",
        "」ヒント+": "」のヒントLv+",
        "全能力": "全ステータス",
        "全スタータス": "全ステータス",
        "全パフォーマンス値": '全ステータス',
        "全パフォーマンス": '全ステータス',
        "5種ステータス": '全ステータス',
        "ランダムな能力": 'ランダムな1つのステータス',
        "3つのランダムなステータス": 'ランダムな3つのステータス',
        "4つのランダムなステータス": 'ランダムな4つのステータス',
        "ランダムなステータス1種": 'ランダムな1つのステータス',
        "ランダムなステータス2種": 'ランダムな2つのステータス',
        "ランダムな2種のステータス": 'ランダムな2つのステータス',
        "ランダムな3ステータス": 'ランダムな3つのステータス',
        "ランダムな4つステータス": 'ランダムな4つのステータス',
        "ランダムなステータス": 'ランダムな1つのステータス',
        "ランダムステータス": 'ランダムな1つのステータス',
        "ランダムで": "ランダムな",
        "最大体力値": "体力の最大値",
        "ファン+": "ファン数+",
        "彗眼": '慧眼',
        "昂ぶる鼓動": '昂る鼓動',
        "出力1000%！": '出力1000％！',
        "「出力1000％」": '「出力1000％！」',
        "垂れ馬回避": '垂れウマ回避',
        "追い込みコーナー○": '追込コーナー○',
        "プチ☆アゲ↑バイブス": 'ブチ☆アゲ↑バイブス',
        "桐生院葵の絆ゲージ": '桐生院トレーナーの絆ゲージ',
        "桐生院の絆ゲージ": '桐生院トレーナーの絆ゲージ',
        "チーム<シリウス>": 'チーム＜シリウス＞',


        # 中文
        "随机两项属性": 'ランダムな2つのステータス',
        "智+": '賢さ+',
        "绊+": 'の絆ゲージ+',
        "绊-": 'の絆ゲージ-',
        "的hint+": 'のヒントLv+',
        "的HintLv+": 'のヒントLv+',
        "的Hint+": 'のヒントLv+',
        "直线一气": '直線一気',
    }
    for k, v in rp.items():
        effect = effect.replace(k, v)

    # 接下来是整体替换
    rp = {
        # Kamigame又Bug了
        # https://game8.jp/umamusume/486171
        # https://kamigame.jp/umamusume/page/260522360824719531.html
        "体力+": "体力+10",
        # タマモクロス たこ焼き粉のピンチ！、トーセンジョーダン ギャルのマストアイテム☆、ヒシアマゾン 懐かしの味
        # コパノリッキー 吉祥☆みんなでスマイル、ドゥラメンテ 流すべきこの汗 都只写了体力↑，懒得查了 就当+10吧
        "体力↑": "体力+10",
        # 安心沢刺々美 決戦☆あんし～んよ永遠に！
        "体力全回復": "体力+999",
        "やる気「絶好調」": "やる気+4",
        "やる気↓": "やる気-1",
        "やる気↑": "やる気+1",
        "やる気上昇": "やる気+1",
        # あんし～ん笹針師、参☆上, 印象中-2明确写了
        "やる気減少": "やる気-1",
        # ビワハヤヒデ 天皇賞（秋）の後に・プライズ 不知道加多少 猜是45
        "スキルPt上昇": "スキルPt+45",
        # [そこに“いる”幸せ]アグネスデジタル ヲタクの推し活 830085003
        "アグネスデジタル+5": 'アグネスデジタルの絆ゲージ+5',
        # アグネスデジタル 万能を超えて 501019119
        "「負けん気」のスキルLv+1": '「負けん気」のヒントLv+1',
        # アストンマーチャン SSBの謎を追え！ 501087520 宣伝スキルをあげ、協力させてほしい
        "「軽い足取り」ヒントLv+1": '「軽い足取り」のヒントLv+1',
        # アストンマーチャン いろいろおいしいみたいです 501087524 受けて立とう！
        "「逃げのコツ◯」ヒントLv+1": '「逃げのコツ◯」のヒントLv+1',
        # [心と足元は温かく]イクノディクタス U情 830063003
        "「大局観」のスキルLv+3": '「大局観」のヒントLv+3',
        # [副会長の一刺し]エアグルーヴ 凛と胡蝶蘭 820004001
        "パワ+5": 'パワー+5',
        # エアグルーヴ 阪神JFの後に・不屈たる様 501018305
        "スキル+1": 'スピード+1',
        # エイシンフラッシュ 想定外のお昼 801037001
        "絆ゲージ+5": 'の絆ゲージ+5',
        # キングヘイロー 『一流ウマ娘、キングヘイロー』 501061111
        " スキルPt+20": 'スキルPt+20',
        # グラスワンダー 有馬記念の後に・振り向かぬ背 501011309
        " スキルPt+51": 'スキルPt+51',
        # [ウマ王伝説・最強になった件]ゴールドシップ ゴルシ様、配下をそろえる 830057003
        "おひとり様◯ヒントLv +1": 'おひとり様◯のヒントLv+1',
        # [デッド・エンド【通せん坊】]ジャングルポケット “幻”（ゴースト）と“踊”（はし）れ 820056001
        "ジャングルポケット+5": 'ジャングルポケットの絆ゲージ+5',
        # シンコウウインディ 悪童が征く 501043704
        "スタミ+10": 'スタミナ+10',
        # スーパークリーク 菊花賞の後に・絆の勝利！ 501045307
        # "「良バ場◯」+1": '「良バ場◯」のヒントLv+1',
        # スペシャルウィーク あれもこれもで、悩んじゃいます！ 801001002
        "スペシャルウィーク絆ゲージ+5": 'スペシャルウィークの絆ゲージ+5',
        # ダイワスカーレット 天皇賞（秋）の後に・いつもの二人 501009321
        " スタミナ+3": 'スタミナ+3',
        # [Just keep going.]マチカネタンホイザ 目指せ、いたずらっ子！ 830030002
        "マチカネタンホイザの絆fゲージ+5": 'マチカネタンホイザの絆ゲージ+5',
        # メイショウドトウ にんじん……買ってくださいっ 801058002
        # "スキル「先行コーナー◯」スキルヒント+1": '「先行コーナー◯」のヒントLv+1',
        # [バカと笑え]メジロパーマー 振り逃げランナウェイ 830027001
        "メジロパーマー絆+5": 'メジロパーマーの絆ゲージ+5',
        # [アマゾネス・ラピス]ヒシアマゾン 友か、好敵手か 501012515
        "「練習上手○」獲得": '「練習上手◯」獲得',
        # [独奏・螺旋追走曲]マンハッタンカフェ ミツケテ 830075002
        "「夜更し気味」獲得": '「夜ふかし気味」獲得',
        "「怠け癖」獲得": '「なまけ癖」獲得',
        # スペシャルウィーク あんし～ん笹針師、参☆上 50XXXX720
        "スキル「直線回復○」習得": 'スキル「直線回復」習得',

        # 习得是技能用的 获得是状态 避免混淆
        "確率で「なまけ癖」習得": '「なまけ癖」獲得',
        "確率でマイナススキル獲得": 'マイナススキル習得',
        # スイープトウショウ デビュー戦の後に・ワガママヒート 501044303
        "「アタシに指図しないで！！！」獲得": '「アタシに指図しないで！！！」習得',
        # ダイタクヘリオス 新聞を読むウマ娘 501065524
        "「1番人気でヤバたん」獲得": '「1番人気でヤバたん」習得',
        # トーセンジョーダン 皐月賞の後に・はしりてー 501048306
        "「凸凹ネイル」獲得": '「凸凹ネイル」習得',
        # メイショウドトウ 天皇賞（春）の後に・盾の重さ 501058313
        "「良バ場×」獲得": '「良バ場×」習得',
        # 安心沢刺々美 全ての道は笹針に通じる 809005001
        "「引っ込み思案」獲得": '「引っ込み思案」習得',
        # 安心沢刺々美 あんし～んの練習台？ 809005004
        "「コーナー回復×」獲得": '「コーナー回復×」習得',

        # 中文部分 感谢好心人翻译
        "干劲提升": 'やる気+1',
        "【练习下脚】": '「練習ベタ」獲得',
    }
    effect = rp.get(effect, effect)

    # 还有些零七八碎
    # 帽子的最後の大一番 不知道发生了啥
    if effect.endswith("の絆ゲージ"):
        effect += '+1'
    # オグリの大食い選手権、スペシャルウィーク裏の顔
    if effect.startswith("体力が全回復"):
        effect = "体力+999"
    # [努力は裏切らない！]ダイワスカーレット 相手が誰でも負けないんだから！  # 把结尾多余的删掉
    if effect.startswith("体力") and effect.endswith("回復"):
        effect = effect.replace("回復", "")
    # https://kamigame.jp/umamusume/page/109898498022834183.html
    # サイレンススズカ 固定のイベント一覧--初詣  # 丢东西啦
    if effect.endswith("スキルPt+"):
        effect += '35'
    # 至此，预处理完毕

    # 一些关键要素（数值类）
    kw = {
        # success_events.br中还有些双语的 真的是辛苦了
        # 这是非要用re的节奏吗 没出现的先不写了
        "スピード(速度)": 'speed_incr',
        "パワー(力量)": 'power_incr',
        "根性(毅力)": 'guts_incr',
        "スキルPt(技能点数)": 'skill_point_incr',
        "SP+": 'skill_point_incr',

        # 现在是events.br中的
        "スピード": 'speed_incr',
        "スタミナ": 'stamina_incr',
        "パワー": 'power_incr',
        "根性": 'guts_incr',
        "賢さ": 'wiz_incr',
        "スキルPt": 'skill_point_incr',
        "体力の最大値": 'max_vital',
        "体力最大値": 'max_vital',  # 照顾下进王
        "やる気": 'motivation',
        "直前のトレーニングに応じたステータス": 'last_train',
        "直前のトレーニング能力": 'last_train',
        "行ったトレーニングの能力": 'last_train',
        "トレーニングLv": "train_lv",

        # 不知道什么时候掺进来一些中文
        "速度": 'speed_incr',
        "耐力": 'stamina_incr',
        "力量": 'power_incr',
        "智力": 'wiz_incr',
        "技能点": 'skill_point_incr',
        "体力最大值": 'max_vital',
        "上次训练属性": 'last_train',
        "上次训练": 'last_train',
        "心情": 'motivation',

        # 容易重的放最后
        "体力": 'vital',
    }
    # 状态名，这里没查到就当是技能了
    cd = {
        "夜ふかし気味": 1,
        "なまけ癖": 2,
        "肌あれ": 3,
        "太り気味": 4,
        "片頭痛": 5,
        "練習ベタ": 6,
        "切れ者": 7,
        "愛嬌◯": 8,
        "注目株": 9,
        "練習上手◯": 10,
        "練習上手◎": 11,
        "小さなほころび": 12,
        "大輪の輝き": 13,
        "ファンとの約束・北海道": 14,
        "ファンとの約束・北東": 15,
        "ファンとの約束・中山": 16,
        "ファンとの約束・関西": 17,
        "ファンとの約束・小倉": 18,
        "まだまだ準備中": 19,
        "ガラスの脚": 20,
        "怪しい雲行き": 21,
        "ファンとの約束・川崎": 22,
        "英雄の光輝": 23,
        "春待つ蕾": 24,
        "ポジティブ思考": 25,
        "幸運体質": 26,
        "情熱ゾーン": 100,
    }
    # 中文状态，就吃和刺刺美
    zt = {
        "『太り気味』": 4,
        "爱娇": 8,
    }
    # 开始对号入座
    if effect.startswith("やる気") and effect.endswith("段階上昇"):
        return _Effect(motivation=int(effect[3]))
    if "のヒント" in effect:
        skill, level = effect.split('のヒントLv')
        skill = skill[3:] if skill.startswith('スキル') else skill
        skill = skill[3:] if skill.startswith('ヒント') else skill
        skill = skill[1:-1] if skill.startswith('「') and skill.endswith('」') else skill
        skill = skill[1:-1] if skill.startswith('『') and skill.endswith('』') else skill
        return _Effect(skill_hint=(Skill(skill), int(level)))
    if "の絆ゲージ" in effect:
        chara, favor = effect.split("の絆ゲージ")
        try:
            chara = Chara(chara)
        except CharaNotFoundError:
            chara = SupportCardChara(chara)
        favor = int(favor)
        return _Effect(favor=(chara, favor))
    if "**進行イベント打ち切り**" == effect:
        return _Effect(other=effect)
    if "ファン数" in effect:
        return _Effect(fan=int(effect[5:None if effect[-1].isdecimal() else -1]))
    if effect.startswith("全ステータス上限"):  # 跟下一条太像了，不好放进kw里
        return _Effect(all_limit_incr=int(effect[8:]))
    if effect.startswith("全ステータス"):
        return _Effect(random_attr=(5, int(effect[6:])))
    if effect.startswith("全属性"):
        return _Effect(random_attr=(5, int(effect[3:])))
    if effect.startswith("ランダムな") and "つのステータス" in effect:
        return _Effect(random_attr=(int(effect[5]), int(effect[13:])))
    if effect.startswith("随机") and "属性" in effect:
        return _Effect(random_attr=(int(effect[2]), int(effect[5:])))
    for k in kw:
        if effect.startswith(k):
            return _Effect(**{kw[k]: int(effect[len(k):])})
    if effect.endswith("獲得") and not effect.endswith("つ獲得"):
        for condition in cd:
            if condition in effect:
                return _Effect(condition=_ConditionType(cd[condition]))
        else:
            # 状态没抓到，应该有问题
            print('原始:', _debug)
            print(f'"{effect}": \'{effect}\',')
            raise
    if effect.startswith("获得"):
        for condition in zt:
            if effect.endswith(condition):
                return _Effect(condition=_ConditionType(zt[condition]))
        else:
            if effect.endswith("】的Hint"):
                return _Effect(skill=Skill(effect[3:-6]))
            if effect not in {
                '获得随机技能Hint',
            }:
                # DEBUG 出现了奇怪的东西 姑且raise
                raise
    if effect.startswith("スキル") and effect.endswith("習得"):
        return _Effect(skill=Skill(effect[4:-3]))
    if effect == "治愈所有负面效果":
        return _Effect(condition_clear=_ConditionType(0))
    # 这条独一份
    if effect.endswith("が治った"):
        for condition in cd:
            if condition in effect:
                return _Effect(condition_clear=_ConditionType(cd[condition]))
    if "+" in effect or "-" in effect:
        # 这些有工夫了再搞
        if effect not in {"固有スキルLv+1",
                          '固有スキルのLv+1',
                          'パッション+20',
                          'メンタル+20',
                          'ボーカル+20',
                          '各ウマ娘のスターゲージ+1',
                          '適性Pt+50',


                          }:
            # 数值属性没抓到，应该有问题
            print('原始:', _debug)
            print(f'"{effect}": \'{effect}\',')
            raise
    if "【大成功】" in effect:
        raise
    return _Effect(other=effect)


def _parse_event(effect: str) -> _Effect:
    try:
        res = _parse_event_raw(effect)
    except ValueError:
        # 有可能丢东西或出歧义，容易出事，最后手段
        for taboo in "・":
            effect = effect.split(taboo)[-1]
        for taboo in "~〜～（":
            effect = effect.split(taboo)[0]
        rp = {
            "プラス": "+",
        }
        for k, v in rp.items():
            effect = effect.replace(k, v)
        res = _parse_event_raw(effect)
    return res


def unique(cls: type) -> type:
    old_new = cls.__new__

    def new_new(kls, *args, **kw):
        ins = getattr(kls, '_instances')
        try:
            if args not in ins:
                if cls.__base__ is object and len(cls.__bases__) == 1:
                    self = old_new(kls, **kw)
                else:
                    self = old_new(kls, *args, **kw)
                ins.setdefault(args, self)
            return ins.get(args)
        except TypeError:
            if cls.__base__ is object and len(cls.__bases__) == 1:
                return old_new(kls, **kw)
            else:
                return old_new(kls, *args, **kw)
    cls._instances = {}
    cls.__new__ = new_new
    return cls


@unique
class EventEffects:
    def __init__(self, effect: str):
        """某一个选项的所有可能效果"""
        import os
        self._effect_raw = effect
        self._effect = []
        # 做一些准备工作
        # 首先做一些整体替换 很多是有or捣乱
        rp = {
            # 06的 弥生賞の後に・生まれた戸惑い 竟然少了一堆顿号
            "スタミナ+1、パワー+1、根性+1賢さ+1スキルPt+36、秋川理事長の絆ゲージ+4":
                'スタミナ+1、パワー+1、根性+1、賢さ+1、スキルPt+36、秋川理事長の絆ゲージ+4',
            # 毎日王冠の後に・そして“光”へ 同上 简直重灾区
            "スタミナ+3、パワー+3、根性+3、賢さ+3スキルPt+43、「先駆け」のヒントLv+1、秋川理事長の絆ゲージ+4":
                'スタミナ+3、パワー+3、根性+3、賢さ+3、スキルPt+43、「先駆け」のヒントLv+1、秋川理事長の絆ゲージ+4',
            # https://kamigame.jp/umamusume/page/203844928390832315.html 不明觉厉
            "【大成功】、賢さ+30、シリウスシンボリの絆ゲージ+5、「起死回生」のヒントLv+3"
            "【成功】、賢さ+15、シリウスシンボリの絆ゲージ+5、「ワンチャンス」のヒントLv+3":
                '(成功时)賢さ+30、シリウスシンボリの絆ゲージ+5、「起死回生」のヒントLv+3' + os.linesep +
                '(失败时)賢さ+15、シリウスシンボリの絆ゲージ+5、「ワンチャンス」のヒントLv+3',
            # https://kamigame.jp/umamusume/page/152061530106507043.html 忽略1or3吧
            "体力-10、スピード+25、「先手必勝」のヒントLv+1or3、ツインターボの絆ゲージ↑":
                '(成功时)体力-10、スピード+25、「先手必勝」のヒントLv+3、ツインターボの絆ゲージ+5' + os.linesep +
                '(失败时)体力-10、スピード+25、「先手必勝」のヒントLv+1、ツインターボの絆ゲージ+5',
            # ナリタタイシン 菊花賞の後に・溢れる 501050311 確率负面技能
            "全ステータス+1、スキルPt+45、「非根幹距離×」獲得（確率）、秋川理事長の絆ゲージ+4"
            "2位:全ステータス+2、スキルPt+58、秋川理事長の絆ゲージ+4":
                '(成功时)全ステータス+1、スキルPt+45、秋川理事長の絆ゲージ+4' + os.linesep +
                '(失败时)全ステータス+1、スキルPt+45、「非根幹距離×」習得、秋川理事長の絆ゲージ+4',
            # 还是他，日経賞の後に・ここがいい 按说下手消没消应该前置吧
            "やる気+3、全ステータス+19〜27、スキルPt+78〜94、「練習上手◎」獲得、秋川理事長の絆ゲージ+4"
            " ※練習ベタがないときやる気+3、全ステータス+19〜20、スキルPt+78〜81、「練習ベタ」が治った、"
            "秋川理事長の絆ゲージ+4※練習ベタ状態のとき":
                '(成功时)やる気+3、全ステータス+19〜27、スキルPt+78〜94、「練習上手◎」獲得、秋川理事長の絆ゲージ+4' + os.linesep +
                '(失败时)やる気+3、全ステータス+19〜20、スキルPt+78〜81、「練習ベタ」が治った、秋川理事長の絆ゲージ+4',
            # マチカネフクキタル 開運カードはどれ！？ 经典大仙抽卡 但印象中是3种还是四种结果来着 按理说也应该直接拽进Fail几个
            # 忽略加属性的那个吧 反正三个选项差不多 但 https://gamewith.jp/uma-musume/article/show/301267 有不同想法
            "やる気↑、スキルPt+15orやる気−1（ランダムで変化）":
                '(成功时)やる気↑、スキルPt+15' + os.linesep + '(失败时)やる気−1',
            # ヒシアマゾン 有馬記念の後に・レースに勝って…… 菱亚也很迷 不知道为什么偏偏挑了这俩绿
            "全ステータス+3、スキルPt+51、「良バ場」or「晴れの日◯」のヒントLv+1、秋川理事長の絆ゲージ+4":
                '(成功时)全ステータス+3、スキルPt+51、「良バ場」のヒントLv+1、秋川理事長の絆ゲージ+4' + os.linesep +
                '(失败时)全ステータス+3、スキルPt+51、「晴れの日◯」のヒントLv+1、秋川理事長の絆ゲージ+4',
            # メジロマックイーン 天皇賞（秋）の後に・未踏の栄光 肥驹这个or的不明所以
            "全ステータス+3、スキルPt+49or51、秋川理事長の絆ゲージ+4":
                '全ステータス+3、スキルPt+45、秋川理事長の絆ゲージ+4',
            # [今宵、円舞曲にのせて]キングヘイロー 舞踏会の綺羅星 Failed的fFailed出问题了
            "体力-10、パワー+20、「詰め寄り」のヒントLv+3or+1":
                '(成功时)体力-10、パワー+20、「詰め寄り」のヒントLv+3' + os.linesep +
                '(失败时)体力-10、パワー+20、「詰め寄り」のヒントLv+1',
            # [Q≠0]アグネスタキオン 交感：走力の限界突破に関する質的研究 830101001
            "【大成功】、スピード+5、スタミナ+5、賢さ+5、「先行直線◯」のヒントLv+3、"
            "「ささやき」のヒントLv+1、アグネスタキオンの絆ゲージ+5、【成功】、・スピード+5、賢さ+5、"
            "「先行直線◯」のヒントLv+1、アグネスタキオンの絆ゲージ+5":
                '(成功时)スピード+5、スタミナ+5、賢さ+5、「先行直線◯」のヒントLv+3、'
                '「ささやき」のヒントLv+1、アグネスタキオンの絆ゲージ+5、' + os.linesep +
                '(失败时)スピード+5、賢さ+5、「先行直線◯」のヒントLv+1、アグネスタキオンの絆ゲージ+5',
            # [Lunatic Lab]アグネスタキオン モルモットの幸せ 501032802
            # 不知道说什么好了 这个自己没选项 根据之前的选择
            "勝負服イベント2種（ジュニア級8月→シニア級8月）の選択で変動、"
            "【上→上】・「中距離直線◯」のヒントLv+2、「テンポアップ」のヒントLv+2、"
            "【上→下/下→上】・パワー+20、スキルPt+25、【下→下】・「中距離コーナー◯」のヒントLv+2、"
            "「軽やかステップ」のヒントLv+2":
                '(成功时)「中距離直線◯」のヒントLv+2、「テンポアップ」のヒントLv+2' + os.linesep +
                '(失败时)パワー+20、スキルPt+25' + os.linesep +
                '(失败时)「中距離コーナー◯」のヒントLv+2、「軽やかステップ」のヒントLv+2',
            # [朔月のマ・シェリ]カレンチャン Rush Rush Rush Curren！ 501038802
            "【大成功】根性+30、「切れ者」獲得、【成功】根性+30":
                '【大成功】根性+30、「切れ者」獲得、' + os.linesep +
                '【成功时】根性+30',
            # シンボリクリスエス Oath 501083118
            "【9勝以上】・スタミナ+15、パワー+15、「コーナー巧者◯」のヒントLv+1、「垂れウマ回避」のヒントLv+1、"
            "【8勝】・スタミナ+10、パワー+10、「コーナー巧者◯」のヒントLv+1":
                "【9勝上】スタミナ+15、パワー+15、「コーナー巧者◯」のヒントLv+1、「垂れウマ回避」のヒントLv+1" + os.linesep +
                '【8勝下】スタミナ+10、パワー+10、「コーナー巧者◯」のヒントLv+1',
            # ウオッカ 安田記念の後に・サイレント連覇！ 501008319
            "パワー+20、全ステータス+1〜3（着順で変化）、スキルPt+58、確率で「垂れウマ回避」のヒントLv+1、"
            "確率で「練習上手◯」獲得、秋川理事長の絆ゲージ+4":
                '【都到手】パワー+20、全ステータス+1、スキルPt+58、「垂れウマ回避」のヒントLv+1、'
                '「練習上手◯」獲得、秋川理事長の絆ゲージ+4' + os.linesep +
                '【给技能】パワー+20、全ステータス+1、スキルPt+58、「垂れウマ回避」のヒントLv+1、'
                '秋川理事長の絆ゲージ+4' + os.linesep +
                '【给状态】パワー+20、全ステータス+1、スキルPt+58、「練習上手◯」獲得、'
                '秋川理事長の絆ゲージ+4' + os.linesep +
                '【都不给】パワー+20、全ステータス+1、スキルPt+58、秋川理事長の絆ゲージ+4',
            # オグリキャップ 天皇賞（秋）の後に・最後の大一番 501006310
            "全ステータス+3、スキルPt+48、秋川理事長の絆ゲージ、ランデムで「根幹距離」のヒントLv.1、「イナズマステップ」のヒントLv.1":
                '【给根干】全ステータス+3、スキルPt+48、秋川理事長の絆ゲージ、'
                '「根幹距離」のヒントLv.1、「イナズマステップ」のヒントLv.1' + os.linesep +
                '【没有给】全ステータス+3、スキルPt+48、秋川理事長の絆ゲージ、「イナズマステップ」のヒントLv.1',
            # スマートファルコン Connect Live☆～それから～ 501046525
            # 这个直接随便设一个好了
            "やる気+1、スタミナ+10、賢さ+10、スキルPt+10、「出走したレース場◯」のヒントLv+5、**「ファンとの約束・地方名」がなくなる**":
                'やる気+1、スタミナ+10、賢さ+10、スキルPt+10、'
                '「東京レース場◯」のヒントLv+5、**「ファンとの約束・地方名」がなくなる**',
            # 青春杯 チーム＜ファースト＞の宣戦布告 400002117
            "スキルPt+15、「アオハル点火」のヒントLv+3":
                '【给速度】スキルPt+15、「アオハル点火・速」のヒントLv+3' + os.linesep +
                '【给耐力】スキルPt+15、「アオハル点火・体」のヒントLv+3' + os.linesep +
                '【给力量】スキルPt+15、「アオハル点火・力」のヒントLv+3' + os.linesep +
                '【给毅力】スキルPt+15、「アオハル点火・根」のヒントLv+3' + os.linesep +
                '【给智力】スキルPt+15、「アオハル点火・賢」のヒントLv+3',
            # [魔力授かりし英雄]ゼンノロブロイ 読書少女とあるカエルの友人 830065003
            "スキルPt+20、「潜伏姿勢」のヒントLv+1": 'スキルPt+20、「潜伏態勢」のヒントLv+1',
            # [『ロードナイトと夢の石』]ゼンノロブロイ 虹色クッキング 830104002
            "スタミナ+10、スキルPt+10、「巻き直し」のヒントLv+1、ゼンノロブロイの絆ゲージ+5":
                'スタミナ+10、スキルPt+10、「まき直し」のヒントLv+1、ゼンノロブロイの絆ゲージ+5',
            # メジロブライト 菊花賞の後に・生来の強運 501074308
            "全ステータス+3、スキルPt+54、秋川理事長の絆ゲージ+4、確率で「抜け出し準備」のヒントLv+1":
                '【给技能】全ステータス+3、スキルPt+54、秋川理事長の絆ゲージ+4、「抜け出し準備」のヒントLv+1' + os.linesep +
                '【没有给】全ステータス+3、スキルPt+54、秋川理事長の絆ゲージ+4',
            # メジロブライト 菊花賞の後に・恐るべし福の壁 501074309
            # 这堆都是距离跑法之类的随机给的为什么放这里啊
            "全ステータス+1〜2、スキルPt+54、秋川理事長の絆ゲージ+4、確率で「抜け出し準備」のヒントLv+1":
                '全ステータス+1〜2、スキルPt+54、秋川理事長の絆ゲージ+4',
            # [『エース』として]メジロマックイーン “期待”に応える 830022003
            "体力-10、「深呼吸」か「クールダウン」のヒントLv+1":
                '【成功时】体力-10、「クールダウン」のヒントLv+1' + os.linesep +
                '【失败时】体力-10、「深呼吸」のヒントLv+1',

            # 下面这些多了个空格。别的地方有拿空格当分隔符的，只能整体搞了
            # ヤマニンゼファー 風の吹くまま……
            "体力+ 15、やる気−1、根性−1": '体力+15、やる気−1、根性−1',
            # [ウマ王伝説・最強になった件]ゴールドシップ ゴルシ様、配下をそろえる 830057003 し、四天王？ さっぱりわからない……
            "体力-10、スピード+10、スタミナ+10、「内的体験」のヒントLv +3 、ゴールドシップの絆ゲージ+5":
                '体力-10、スピード+10、スタミナ+10、「内的体験」のヒントLv+3 、ゴールドシップの絆ゲージ+5',
            "体力-10、スピード+5、スタミナ+5、「内弁慶」のヒントLv +3":
                '体力-10、スピード+5、スタミナ+5、「内弁慶」のヒントLv+3',
            "体力+10、おひとり様◯ヒントLv +1": '体力+10、おひとり様◯のヒントLv+1',
            # スマートファルコン ワールド・イズ・ウマドル♪ 501046111
            "全ステータス+5、スキルPt +20": '全ステータス+5、スキルPt+20',
            # [感謝は指先まで込めて]ファインモーション 素敵な♪レース日和 830010003
            "体力-10、根性+5、賢さ+5、スキルPt+5、「抜け出し準備」のヒントLv +3":
                '体力-10、根性+5、賢さ+5、スキルPt+5、「抜け出し準備」のヒントLv+3',
            # [爽快！ウイニングショット！]メジロライアン 不屈のバーニングハート！！ 830048003
            "パワー+10、根性+5、「勝利への執念」のヒントLv +1": 'パワー+10、根性+5、「勝利への執念」のヒントLv+1',
            # ライスシャワー 何事も前向きに？ 501030520 逆にこの晴れを利用しよう
            "「良バ場◯」のヒントLv  +1": '「良バ場◯」のヒントLv+1',

            # メジロラモーヌ オークスの後に・樫で織る 501086309
            "全ステータス+3、スキルPt+45「自信家」のヒントLv+1、秋川理事長の絆ゲージ+4":
                '全ステータス+3、スキルPt+45、「自信家」のヒントLv+1、秋川理事長の絆ゲージ+4',
            # [愛麗♡キョンシー]アグネスデジタル 哀しき怪物・ヲタキョンシー！ 501019801
            "【大成功】、パワー+20、賢さ+20、「マイル直線◯」のヒントLv+3、"
            "【成功】、パワー+10、賢さ+10、「マイル直線◯」のヒントLv+3":
                '【大成功】パワー+20、賢さ+20、「マイル直線◯」のヒントLv+3' + os.linesep +
                '【成功时】パワー+10、賢さ+10、「マイル直線◯」のヒントLv+3',
            # [Dot-o'-Lantern]メイショウドトウ ドトウのパリピ屋敷！？ 501058801
            "【大成功】、スタミナ+20、根性+20、「中距離コーナー◯」のヒントLv+3、"
            "【成功】、スタミナ+10、根性+10、「中距離コーナー◯」のヒントLv+3":
                '【大成功】スタミナ+20、根性+20、「中距離コーナー◯」のヒントLv+3' + os.linesep +
                '【成功时】スタミナ+10、根性+10、「中距離コーナー◯」のヒントLv+3',
            # ライトハロー 虹の入り江にて 830052001
            "【大成功】、やる気+1、体力+30、スピード+10、根性+10、ライトハローの絆ゲージ+5、レアスキル「お先に失礼っ！」のヒントLv+3、"
            "【成功】、やる気+1、体力+20、スピード+5、根性+5、ライトハローの絆ゲージ+5、レアスキル「お先に失礼っ！」のヒントLv+1":
                '【大成功】やる気+1、体力+30、スピード+10、根性+10、ライトハローの絆ゲージ+5、「お先に失礼っ！」のヒントLv+3、'
                + os.linesep +
                '【成功时】やる気+1、体力+20、スピード+5、根性+5、ライトハローの絆ゲージ+5、「お先に失礼っ！」のヒントLv+1',
            # セイウンスカイ 晴天の攻防 501020524 満足するまで休ませる
            "【大成功】体力+20、「深呼吸」のヒントLv+1、【成功】体力+10":
                '【大成功】体力+20、「深呼吸」のヒントLv+1' + os.linesep +
                '【成功时】体力+10',
            # ネオユニヴァース 星空のコネクト 501105524
            "【確率で分岐】スピード+10、「差し直線◯」のヒントLv+2、"
            "スタミナ+10、「差しコーナー◯」のヒントLv+2、"
            "パワー+5、根性+5、「位置取り押し上げ」のヒントLv+2、"
            "賢さ+10、「静かな呼吸」のヒントLv+2":
                '【可能一】スピード+10、「差し直線◯」のヒントLv+2、' + os.linesep +
                '【可能二】スタミナ+10、「差しコーナー◯」のヒントLv+2、' + os.linesep +
                '【可能三】パワー+5、根性+5、「位置取り押し上げ」のヒントLv+2、' + os.linesep +
                '【可能四】賢さ+10、「静かな呼吸」のヒントLv+2',
            # [Titania]ファインモーション 離れていても 501022802
            "【大成功】スピード+20、スキルPt+15、「切れ者」獲得、【成功】スピード+20、スキルPt+15":
                '【大成功】スピード+20、スキルPt+15、「切れ者」獲得、' + os.linesep +
                '【成功时】スピード+20、スキルPt+15',
            # ライトハロー お疲れ様です……！ 809008003
            "【大成功】、根性+3、やる気+1、ライトハローの絆ゲージ+5、"
            "【成功】、根性+3、ライトハローの絆ゲージ+5":
                '【大成功】根性+3、やる気+1、ライトハローの絆ゲージ+5、' + os.linesep +
                '【成功时】根性+3、ライトハローの絆ゲージ+5',
            # 来源同上 所持数最少目前没留，见得多了再说
            "【大成功】、根性+3、やる気+1、スキルPt+3、ライトハローの絆ゲージ+7、所持数が最少のパフォーマンス+20、"
            "【成功】根性+3、スキルPt+3、ライトハローの絆ゲージ+7、所持数が最少のパフォーマンス+20":
                '【大成功】根性+3、やる気+1、スキルPt+3、ライトハローの絆ゲージ+7、ランダムな1つのステータス+20、' + os.linesep +
                '【成功时】根性+3、スキルPt+3、ライトハローの絆ゲージ+7、ランダムな1つのステータス+20',
            # カワカミプリンセス 完成！究極フォーム！ 501039524
            "【失敗】体力-10、パワー+30、"
            "【大失敗】体力-15、パワー+30、賢さ-10":
                '【失敗时】体力-10、パワー+30' + os.linesep +
                '【大失敗】体力-15、パワー+30、賢さ-10',
            # タマモクロス あきんど根性！ 501021524  @2
            "【大成功】、賢さ+15、「切れ者」獲得"
            "【成功】、スピード+20、賢さ+15":
                '【大成功】賢さ+15、「切れ者」獲得' + os.linesep +
                '【成功时】スピード+20、賢さ+15',
            # ダイワスカーレット 秋華賞の後に・流石で、当然！ 501009316
            "全ステータス+3、スキルPt+45、『秋ウマ娘◯』のヒントLv1（確率）、秋川理事長の絆ゲージ+4":
                '【给技能】全ステータス+3、スキルPt+45、『秋ウマ娘◯』のヒントLv1、秋川理事長の絆ゲージ+4' + os.linesep +
                '【没有给】全ステータス+3、スキルPt+45、秋川理事長の絆ゲージ+4',
            # [大地と我らのアンサンブル]サウンズオブアース 君は、テンポ・ジュストなアンダンテ 830173001 ふ、俺は気まぐれなヴァイオリン……さ @1
            "スタミナ+10，「直線巧者』のヒントLv+2，サウンズオブアースの絆ゲージ+10，连续事件3获得技能为「ハヤテ一文字」":
                'スタミナ+10，『直線巧者』のヒントLv+2，サウンズオブアースの絆ゲージ+10，连续事件3获得技能为「ハヤテ一文字」',
            # [大地と我らのアンサンブル]サウンズオブアース 君は、テンポ・ジュストなアンダンテ 830173001 え、ええっと？ @1
            "根性+10，「直線回復』のヒントLv+2，サウンズオブアースの絆ゲージ+10，连续事件3获得技能为「好転一息」":
                '根性+10，『直線回復』のヒントLv+2，サウンズオブアースの絆ゲージ+10，连续事件3获得技能为「好転一息」',
            # ミホノブルボン 皐月賞の後に・最初の冠 501026306
            "全ステータス+3、スキルPt+51〜57、ランダムで「右回り◯」のヒントLv+1、秋川理事長の絆ゲージ+4":
                '【给技能】全ステータス+3、スキルPt+51〜57、「右回り◯」のヒントLv+1、秋川理事長の絆ゲージ+4' + os.linesep +
                '【没有给】全ステータス+3、スキルPt+51〜57、秋川理事長の絆ゲージ+4',
            # [今ぞ盛りのさくら花]サクラチヨノオー 花咲く、希望！ 830038002
            "やる気+1、スタミナ+30、「中距離直線◯」サクラチヨノオーの絆ゲージ+5":
                'やる気+1、スタミナ+30、「中距離直線◯」+1、サクラチヨノオーの絆ゲージ+5',
            # 桐生院トレーナー トレーナー心得『指導は常に改良せよ』 809004001
            "体力+14、スキルPt19、桐生院の絆ゲージ+5":
                '体力+14、スキルPt+19、桐生院葵の絆ゲージ+5',


            # 一些中文的情况，还原回去
            "直接习得コーナー回復◯、直線回復":
                'スキル「直線回復」習得、スキル「コーナー回復○」習得',
            # [今は瞳を閉じないで]ナイスネイチャ お節介上手なネイチャさん 830138001 君も輝いてると思うけど @1
            "体力+10、やる気+1、ナイスネイチャの絆ゲージ+5，下一事件体力+30":
                '体力+10、やる気+1、ナイスネイチャの絆ゲージ+5',
            # 一些不知所以的情况
            # 青春杯 『アオハル杯』復活！@400002000 你出现的意义是什么
            "-": '',
            # メジロドーベル カラオケチャレンジ 501059524 ライアンの優しさを今は受け取っておこう \u2010
            "‐": '',

            # 樫本理子 意外な一面 809006004
            "『おひとり様◯』的Hint Lv+5，樫本理子绊-10，无法与理事长外出":
                '『おひとり様○』的HintLv+5，樫本理子绊-10，无法与理事长外出',

        }
        effect = rp.get(effect, effect)
        # 然后把个别点去掉，由于有些.被当成、了，只能提前改
        effect = effect.replace('Lv.', 'Lv')
        # 然后把分隔符统一
        for sep in '。.，, ':
            effect = effect.replace(sep, '、')
        # 处理完了 听天由命
        if os.linesep in effect:
            # 这里成功失败没啥特别的说法，反过来也无所谓。为了适配URA忽略前5个字符。
            self._effect[:] = [tuple(filter(self._bool,
                                            (_parse_event(y) for y in x[5:].split('、')))
                                     ) for x in effect.split(os.linesep)]
        else:
            self._effect.append(tuple(filter(self._bool,
                                             map(_parse_event, effect.split('、'))
                                             )))

    def __bool__(self):
        return any(self._bool(effect) for effects in self._effect for effect in effects)

    @staticmethod
    def _bool(effect):
        """判断一个namedtuple是否有意义"""
        if not effect:
            return False
        fields = getattr(effect, '_fields')
        normal = any(getattr(effect, k) for k in fields if k not in ('skill_hint', 'random_attr'))
        return normal or effect.skill_hint[0] or effect.random_attr[0]

    @staticmethod
    def _effect_str(effect):
        d = {'motivation': "やる気%+d", 'vital': "体力%+d", 'max_vital': "体力の最大値%+d",
             'speed_incr': "スピード%+d", 'stamina_incr': "スタミナ%+d", 'power_incr': "パワー%+d",
             'guts_incr': "根性%+d", 'wiz_incr': "賢さ%+d", 'skill_point_incr': "スキルPt%+d",
             'speed_limit_incr': "スピード上限%+d", 'stamina_limit_incr': "スタミナ上限%+d",
             'power_limit_incr': "パワー上限%+d", 'guts_limit_incr': "根性上限%+d",
             'wiz_limit_incr': "賢さ上限%+d", 'all_limit_incr': '全ステータス上限%+d', 'skill': "スキル『%s』習得",
             'condition': "%s獲得", 'condition_clear': "コンディション%sが治った",
             'last_train': "直前のトレーニングに応じたステータス%+d",
             'train_lv': "トレーニングLv%+d", 'fan': "ファン数%+d", 'other': "他:%s"}
        e = {'random_attr': 'ランダムな%dつのステータス%+d',
             'skill_hint': '「%s」のヒントLv%+d'}
        for k in d:
            if v := getattr(effect, k):
                return (d[k] % v).split('_')[-1]
        for k in e:
            if (v := getattr(effect, k))[0]:
                return e[k] % v
        if isinstance(effect.favor, int):
            return "の絆ゲージ%+d" % effect.favor
        elif isinstance(effect.favor, tuple):
            return "%sの絆ゲージ%+d" % effect.favor

        return str(effect)[:20]

    def __str__(self):
        try:
            return os.linesep.join('、'.join(self._effect_str(effect)
                                            for effect in possibility)
                                   for possibility in self._effect)
        except ValueError:
            return self._effect_raw

    __repr__ = __str__

    @property
    def all_effects(self):
        return self._effect.copy()
