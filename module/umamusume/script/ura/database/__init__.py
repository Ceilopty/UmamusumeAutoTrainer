"""master.mdb中的资料"""
from .name_manager import (get_info_filepath,
                           get_name_manager,
                           load)

__all__ = [
    "get_info_filepath",
    "NameManager",
    ]

try:
    NameManager = get_name_manager()
except FileNotFoundError:
    NameManager = None

if __name__ == "__main__":
    a, b, c, d, e = load()[:5]
    for i in range(2):
        print(i, a[b[i]])
        print(i, b[i])
        print(i, c[i])
        print(i, d[i])
        print(i, e[list(e.keys())[i]])
