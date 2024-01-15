from .. import Data, Array
from .CommandInfo import SingleModeCommandInfo


class SingleModeHomeInfo(Data):
    command_info_array: Array[SingleModeCommandInfo]
    race_entry_restriction: int
    disable_command_id_array: Array[int]
    available_continue_num: int
    free_continue_time: int
    shortened_race_state: int
