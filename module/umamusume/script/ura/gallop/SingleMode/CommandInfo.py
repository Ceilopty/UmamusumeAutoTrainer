from .. import Data, Array


class ParamsIncDecInfo(Data):
    target_type: int
    value: int


class CommandInfoBasic(Data):
    command_type: int
    command_id: int
    params_inf_dec_info_array: Array[ParamsIncDecInfo]


class SingleModeCommandInfo(CommandInfoBasic):
    is_enable: int
    training_partner_array: Array[int]
    tips_event_partner_array: Array[int]
    failure_rate: int
