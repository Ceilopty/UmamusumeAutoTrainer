from .. import Data, Array


class FactorInfo(Data):
    factor_id: int
    level: int


class SuccessionEffectedFactor(Data):
    position: int
    factor_id_array: Array[int]
    factor_info_array: Array[FactorInfo]
