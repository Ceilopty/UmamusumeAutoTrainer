if __name__ == '__main__':
    import database
    import gallop
else:
    from . import database
    from . import parse
    from . import gallop


def json2br():
    import brotli, os
    for x in os.listdir():
        if '.json' in x:
            with open(x, 'rb') as f, open(x[:-4] + 'br', 'wb') as g:
                g.write(brotli.compress(f.read()))


def msgpack2json():
    import msgpack, json, os
    for x in os.listdir():
        if '.msgpack' in x:
            if (j := x[:-7] + 'json') in os.listdir():
                continue
            with open(x, 'rb') as f, open(j, 'w') as g:
                json.dump(msgpack.load(f, strict_map_key=False), g)


def br2json():
    import os, brotli
    for x in os.listdir():
        if '.br' in x:
            if (j := x[:-2] + 'json') in os.listdir():
                continue
            with open(x, 'rb') as f, open(j, 'wb') as g:
                g.write(brotli.decompress(f.read()))


if __name__ == '__main__':
    json2br()
    # msgpack2json()
    # br2json()
    pass
# a = gallop.Event(foo)
