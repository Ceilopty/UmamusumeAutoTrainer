"""处理master.mdb中的资料和URA维护的资料"""
from .database import DataBase
from .filepath import get_info_filepath

__all__ = [
    "get_info_filepath",
    "DataBase",
    ]

DataBase.initialize()
