from .. import EventHolder

__all__ = EventHolder.get_all(__name__)

from . import *


class Support(EventHolder):
    pass


for support in __all__:
    Support.load(support)

