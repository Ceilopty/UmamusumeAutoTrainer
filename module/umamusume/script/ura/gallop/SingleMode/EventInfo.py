from .. import Data, Array


class ChoiceArray:
    select_index: int
    receive_item_id: int
    target_race_id: int


class EventContentsInfo(Data):
    support_card_id: int
    show_clear: int
    show_clear_sort_id: int
    choice_array: Array[ChoiceArray]
    is_effected_multi_chara: bool


class SingleModeSuccessionEventInfo(Data):
    effect_type: int


class MinigameResultDetail(Data):
    get_id: int
    chara_id: int
    dress_id: int
    motion: str
    face: str


class MinigameResult(Data):
    result_state: int
    result_value: int
    result_detail_array: Array[MinigameResultDetail]


class SingleModeEventInfo(Data):
    event_id: int
    chara_id: int
    story_id: int
    playing_time: int
    event_contents_info: EventContentsInfo
    succession_event_info: SingleModeSuccessionEventInfo
    minigame_result: MinigameResult
