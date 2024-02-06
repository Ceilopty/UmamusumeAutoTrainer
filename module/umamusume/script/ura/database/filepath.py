import os
import sys

_CURRENT = os.path.split(sys.modules[__name__].__file__)[0]
_CURRENT = os.path.join(_CURRENT, '.br')
_CURRENT_CHN = os.path.join(_CURRENT, 'com.bilibili.umamusu')
_CURRENT_JPN = os.path.join(_CURRENT, 'jp.co.cygames.umamusume')
_LOCALAPPDATA = os.environ.get('LOCALAPPDATA')
EVENT_NAME_FILEPATH = os.path.join(_LOCALAPPDATA,
                                   "UmamusumeResponseAnalyzer",
                                   "events.br")
SUCCESS_EVENT_FILEPATH = os.path.join(_LOCALAPPDATA,
                                      "UmamusumeResponseAnalyzer",
                                      "success_events.br")
NAMES_FILEPATH = os.path.join(_LOCALAPPDATA,
                              "UmamusumeResponseAnalyzer",
                              "names.br")
SKILLS_FILEPATH = os.path.join(_LOCALAPPDATA,
                               "UmamusumeResponseAnalyzer",
                               "skill_data.br")
TALENT_SKILL_FILEPATH = os.path.join(_LOCALAPPDATA,
                                     "UmamusumeResponseAnalyzer",
                                     "talent_skill_sets.br")
FACTOR_IDS_FILEPATH = os.path.join(_LOCALAPPDATA,
                                   "UmamusumeResponseAnalyzer",
                                   "factor_ids.br")
SUPPORT_CARD_DATA_FILEPATH = os.path.join(_CURRENT_JPN,
                                          "support_card_data.br")
SUPPORT_CARD_EFFECT_TABLE_FILEPATH = os.path.join(_CURRENT_JPN,
                                                  "support_card_effect_table.br")
SUPPORT_CARD_UNIQUE_EFFECT_FILEPATH = os.path.join(_CURRENT_JPN,
                                                   "support_card_unique_effect.br")
CHARA_DATA_FILEPATH = os.path.join(_CURRENT_JPN,
                                   "chara_data.br")
CARD_DATA_FILEPATH = os.path.join(_CURRENT_JPN,
                                  "card_data.br")
TEXT_DATA_FILEPATH = os.path.join(_CURRENT_CHN, "text_data.br")
TEXT_J_DATA_FILEPATH = os.path.join(_CURRENT_JPN, "text_data.br")
_GAME_DATA_FOLDER = os.path.join(_LOCALAPPDATA,
                                 "UmamusumeResponseAnalyzer",
                                 "GameData")
TURN_INFO_FOLDER = os.path.join(_GAME_DATA_FOLDER,
                                "Turn")
EVENT_INFO_FOLDER = os.path.join(_GAME_DATA_FOLDER,
                                 "Event")


def get_info_filepath(t: str = 'T', turn: int = 0, event: int = 1) -> str:
    if not len(t) == 1 and t in 'ETS':
        return ''
    match t:
        case 'E':
            file = f'turn{turn}Event{event}.json' if turn else 'thisTurnThisEvent.json'
            folder = EVENT_INFO_FOLDER
        case 'T':
            file = f'turn{turn}.json' if turn else 'thisTurn.json'
            folder = TURN_INFO_FOLDER
        case 'S':
            file = "TeamStadium.json"
            folder = _GAME_DATA_FOLDER
        case _:
            return ''
    return os.path.join(folder, file)
