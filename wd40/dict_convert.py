class DictToObj(object):
    """
    transform a dict to a object
    """
    def __init__(self, d):
        for a, b in d.items():
            if type(a) is bytes:
                attr = a.decode()
            else:
                attr = a
            if isinstance(b, (list, tuple)):
                setattr(self, attr, [DictToObj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, attr, DictToObj(b) if isinstance(b, dict) else b)


class DictToObjJson(object):
    """
    transform a dict to a object
    """
    def __init__(self, d):
        for a, b in d.items():
            if type(a) is bytes:
                attr = a.decode()
            else:
                attr = a
            if type(b) is bytes:
                b = b.decode()
            if isinstance(b, (list, tuple)):
                setattr(self, attr, [DictToObj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, attr, DictToObj(b) if isinstance(b, dict) else b)