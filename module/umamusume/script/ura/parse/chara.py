class CharaNotFoundError(Exception):
    pass


class SupportCardCharaNotFoundError(Exception):
    pass


class Chara:
    """角色规范化
    先放个架子，细节有空再说"""
    def __init__(self, chara: str):
        from ..database import DataBase
        self._name_raw = chara
        self.chara = DataBase.get_chara_by_name(chara)
        if not self.chara:
            raise CharaNotFoundError(chara)
        self.name = self.chara.name
        self.id = self.chara.id

    def __str__(self):
        return self.name or self._name_raw or ''

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Chara):
            return NotImplemented
        return self.id == other.id


class SupportCardChara(Chara):
    """团队卡需要用支援卡角色名（77）找到支援卡，
    再根据支援卡的角色找到支援卡角色。我已经晕了"""
    def __init__(self, chara: str):
        from ..database import DataBase
        self._name_raw_ = chara
        _chara = DataBase.get_support_card_chara_by_name(chara)
        if not _chara:
            raise SupportCardCharaNotFoundError(chara)
        _chara = DataBase.get_chara_by_id(_chara.chara_id)
        super().__init__(_chara.name_alter)
