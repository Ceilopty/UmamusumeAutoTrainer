"""青春杯"""
from ... import Data, Array
from ..CommandInfo import CommandInfoBasic


class TeamDataSet(Data):
    command_info_array: Array[CommandInfoBasic]
