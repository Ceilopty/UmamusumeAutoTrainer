from .klass import BaseName, SupportCardName, UmaName


class NameManager:
    _int_min_value = -2147483648
    null_base_name = BaseName(_int_min_value, "未知")
    null_support_name = SupportCardName(_int_min_value, "未知", _int_min_value, _int_min_value)
    null_uma_name = UmaName(_int_min_value, "未知", _int_min_value)

    def __init__(self, data: list[BaseName]):
        self.names = {x.id: x for x in data}
        for i in self.names.values():
            if isinstance(i, SupportCardName):
                i.nick_name = f"{i.type_name}{i.nick_name}"

    def __getitem__(self, item) -> str:
        if isinstance(item, int):
            return self.get_simple_name(item)
        return NotImplemented

    def get_character(self, _id: int) -> BaseName:
        if value := self.names.get(_id):
            return value
        return self.null_base_name

    def get_support_card(self, _id: int) -> SupportCardName:
        if value := self.names.get(_id):
            if isinstance(value, SupportCardName):
                return value
            raise TypeError(f"无法从{type(value)}转换到SupportCardName")
        return self.null_support_name

    def get_umamusume(self, _id: int) -> UmaName:
        if value := self.names.get(_id):
            if isinstance(value, UmaName):
                return value
            raise TypeError(f"无法从{type(value)}转换到UmaName")
        return self.null_uma_name

    def get_simple_name(self, _id: int) -> str:
        if value := self.names.get(_id):
            match value:
                case SupportCardName() as scn:
                    return scn.simple_name
                case UmaName() as un:
                    return un.charater_name
                case _:
                    return value.name
        return "未知"


def name_object_hook(dct: dict):
    cls = dct["$type"]
    if "System.Private.CoreLib" in cls:
        return dct["$values"]
    if "BaseName" in cls:
        return BaseName.object_hook(dct)
    elif "SupportCardName" in cls:
        return SupportCardName.object_hook(dct)
    elif "UmaName" in cls:
        return UmaName.object_hook(dct)
    else:
        raise TypeError
