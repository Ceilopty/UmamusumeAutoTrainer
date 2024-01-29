DEBUG = True


class _DataMeta(type):
    def __new__(cls, name, bases: tuple, attrs: dict, **kw):
        annotation = {}
        for base in bases:
            annotation.update(getattr(base, '__annotations__', {}))
        annotation.update(attrs.get('__annotations__', {}))
        attrs['__annotations__'] = annotation
        return super().__new__(cls, name, bases, attrs, **kw)


class Data(metaclass=_DataMeta):
    """
    初始化时自动匹配声明的属性
    包含基类的声明
    """
    def __init__(self, data):
        if data is None:
            return
        # 保留原始数据
        datacopy = data.copy() if hasattr(data, 'copy') else data
        setattr(self, self.__class__.__name__ + '_raw', datacopy)
        not_found = []
        empty_value = []
        for key, cls in self.__annotations__.items():
            if key in data:
                if (value := data.pop(key)) is None:
                    empty_value.append(key)
                else:
                    from enum import Enum
                    if isinstance(value, Enum):
                        value = value.value
                    setattr(self, key, cls(value))
            else:
                not_found.append(key)
        else:
            if DEBUG:
                if not_found:
                    print('%s not found in %s' % (not_found, self))
                if data:
                    print('Found %s in %s' % (data.keys(), self))
                if empty_value:
                    print('%s in %s has NULL value' % (empty_value, self))

    def __iter__(self):
        return iter(getattr(self, self.__class__.__name__ + '_raw'))


class _ListMeta(type):
    def __getitem__(cls, item):
        attrs = {
            "__init__": Array.__init__,
            "append": Array.append,
            "extend": Array.extend,
            "data": item
        }
        return _ListMeta('Array', (list,), attrs)


class Array(list, metaclass=_ListMeta):
    """
    初始化时对data中每项匹配声明的属性
    属性的类型由data声明
    """
    data: type

    def __init__(self, iterable):
        list.__init__(self, map(self.data, iterable))

    def append(self, __object):
        list.append(self, self.data(__object))
        
    def extend(self, __iterable):
        list.extend(self, map(self.data, __iterable))
