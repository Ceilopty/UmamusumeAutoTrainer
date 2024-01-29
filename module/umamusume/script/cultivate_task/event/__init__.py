from typing import Union

from bot.recog.ocr import find_similar_text
import bot.base.log as logger
from module.umamusume.context import UmamusumeContext
from .parse import parse_event

log = logger.get_logger(__name__)

USE_DEFAULT = True  # 使用默认选项 或者参考Context


class Event:
    instances = {}

    def __new__(cls, event_name: str, *args):
        if not args:  # Runtime
            event_name_normalized = find_similar_text(event_name, cls.event_map, 0.8)
            if event_name_normalized != "":
                if event_name_normalized not in cls.instances:
                    if event_name_normalized in cls.event_map:
                        handler = cls.event_map[event_name_normalized]
                        if callable(handler):
                            return handler
                        elif isinstance(handler, int):
                            return lambda x: handler
                return cls.instances[event_name_normalized]
            log.debug("未知事件[%s]，使用默认选项1", event_name)
            return lambda x: 1
        else:  # Initialize
            if event_name not in cls.instances:
                self = super().__new__(cls)
                cls.instances[event_name] = self
                if event_name in cls.event_map:
                    self.handler = cls.event_map[event_name]
            return cls.instances[event_name]

    def __init__(self, event_name: str, event: tuple = None, default: Union[int, None] = None):
        if not event:
            return
        self.event_name = event_name
        self.event = parse_event(event)
        if not default:
            default = 1
        if USE_DEFAULT:
            self.handler = default
        self.register(self.event_name, self.handler)

    def __call__(self, ctx: UmamusumeContext):
        if type(self.handler) is int:
            return self.handler
        if callable(self.handler):
            return self.handler(ctx)
        log.warning("事件[%s]未提供处理逻辑", self.event_name)
        return 1

    def handler(self, ctx: UmamusumeContext) -> int:
        pass

    event_map: dict[str, Union[callable, int]] = {}

    @classmethod
    def register(cls, event_name: str, handler: Union[callable, int]) -> None:
        cls.event_map[event_name] = handler


class EventHolder:
    def __init__(self, module):
        self.name = module.__name__
        for event_name in dir(module):
            if event_name.startswith('__'):
                continue
            setattr(self, event_name, Event(*getattr(module, event_name)))
            
    @classmethod
    def load(cls, module_name):
        import sys
        module = getattr(sys.modules[cls.__module__], module_name)
        setattr(module, module_name, cls(module))

    @staticmethod
    def get_all(name):
        import sys
        import os
        path = os.path.split(sys.modules[name].__file__)[0]
        return [os.path.splitext(file)[0]
                for file in os.listdir(path)
                if os.path.isfile(os.path.join(path, file)) and
                not file.startswith('_')]


"""
from . import scenario
from . import chara
from . import support
"""
