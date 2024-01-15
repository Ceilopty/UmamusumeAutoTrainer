"""偶像杯"""
from ... import Data, Array
from ..CommandInfo import CommandInfoBasic


class LiveDataSet(Data):
    command_info_array: Array[CommandInfoBasic]
