if __name__ == "__main__":
    from filepath import *
    from klass import *
else:
    from .filepath import *
    from .klass import *

NAME_MANAGER = None


def deserialize(file_path: str) -> list | dict:
    import json
    import brotli
    with open(file_path, 'rb') as file:
        js = brotli.decompress(file.read())
    return json.loads(js)


def get_name_manager():
    global NAME_MANAGER
    if NAME_MANAGER is None:
        NAME_MANAGER = NameManager(IdList(map(Name, deserialize(NAMES_FILEPATH)['$values'])))
    return NAME_MANAGER


def load():
    events = deserialize(EVENT_NAME_FILEPATH)
    success_events = deserialize(SUCCESS_EVENT_FILEPATH)
    names = deserialize(NAMES_FILEPATH)
    skills = deserialize(SKILLS_FILEPATH)
    talent_skill_sets = deserialize(TALENT_SKILL_FILEPATH)
    factor_ids = deserialize(FACTOR_IDS_FILEPATH)
    support_card_data = deserialize(SUPPORT_CARD_DATA_FILEPATH)
    support_card_effect = deserialize(SUPPORT_CARD_EFFECT_TABLE_FILEPATH)
    support_card_unique_effect = deserialize(SUPPORT_CARD_UNIQUE_EFFECT_FILEPATH)
    chara_data = deserialize(CHARA_DATA_FILEPATH)
    card_data = deserialize(CARD_DATA_FILEPATH)
    text = deserialize(TEXT_DATA_FILEPATH)

    parsed_events = IdList(map(Event, events))
    parsed_success_events = IdList(map(SuccessEvent, success_events))
    parsed_names = IdList(map(Name, names['$values']))
    parsed_skills = IdList(map(Skill, skills))
    parsed_talent_skill_sets = dict((k, IdList(map(TalentSkill(skills=parsed_skills), v), 'skill_id'))
                                    for k, v in talent_skill_sets.items())
    parsed_factor_ids = factor_ids.copy()
    parsed_chara = IdList(map(Chara, chara_data))
    parsed_card = IdList(map(Card, card_data))
    parsed_support = IdList(map(SupportCard, support_card_data))
    text = TextData(text)

    Chara.set_text(text)
    Card.set_chara(parsed_chara)

    from collections import namedtuple
    R = namedtuple('Res', (
        'events', 'success_events', 'names', 'skills', 'talent_skill_sets',
        'factor_ids', 'support', 'support_card_effect',
        'support_card_unique_effect', 'chara', 'card', 'text'
    ))
    return R(
        events=parsed_events,
        success_events=parsed_success_events,
        names=parsed_names,
        skills=parsed_skills,
        talent_skill_sets=parsed_talent_skill_sets,
        factor_ids=parsed_factor_ids,
        support=parsed_support,
        support_card_effect=support_card_effect,
        support_card_unique_effect=support_card_unique_effect,
        chara=parsed_chara,
        card=parsed_card,
        text=text
    )


def get_info_filepath(t: str = 'T', turn: int = 0, event: int = 1) -> str:
    if not len(t) == 1 and t in 'ET':
        return ''
    match t:
        case 'E':
            file = f'turn{turn}Event{event}.json' if turn else 'thisTurnThisEvent.json'
            folder = EVENT_INFO_FOLDER
        case 'T':
            file = f'turn{turn}.json' if turn else 'thisTurn.json'
            folder = TURN_INFO_FOLDER
        case _:
            return ''
    return os.path.join(folder, file)


class NameManager:
    def __init__(self, names):
        self.names = names

    def get_support(self, _id: int):
        return self.names[_id]
