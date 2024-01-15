from .. import Data, Array
from .Chara import SingleModeChara
from ..ResponseCommon import ResponseCommon
from ..NotUpDownParameterInfo import (
                        NotDownParameterInfo,
                        NotUpParameterInfo)
from .HomeInfo import SingleModeHomeInfo
from .EventInfo import SingleModeEventInfo
from .SuccessionEffectedFactor import SuccessionEffectedFactor
from .Race import SingleModeRaceCondition, SingleModeRaceStartInfo
from .Scenario import *


class SingleModeCommandResult(Data):
    command_id: int
    sub_id: int
    result_state: int


class CommonResponse(Data):
    chara_info: SingleModeChara
    not_up_parameter_info: NotUpParameterInfo
    not_down_parameter_info: NotDownParameterInfo
    home_info: SingleModeHomeInfo
    command_result: SingleModeCommandResult
    unchecked_event_array: Array[SingleModeEventInfo]
    event_effected_factor_array: Array[SuccessionEffectedFactor]
    race_condition_array: Array[SingleModeRaceCondition]
    race_start_info: SingleModeRaceStartInfo
    team_data_set: TeamDataSet
    free_data_set: FreeDataSet
    live_data_set: LiveDataSet
    venus_data_set: VenusDataSet
    arc_data_set: ArcDataSet


class SingleModeCheckEventResponse(ResponseCommon):
    data: CommonResponse
