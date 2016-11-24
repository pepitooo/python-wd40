import arrow


class ExpireArrow(arrow.Arrow):
    def is_expired(self) -> bool:
        return self < arrow.utcnow()

    def expiration(self, seconds):
        return self.replace(seconds=seconds)


class ExpireFifo:
    def __init__(self, expire_s=None):
        """
        :param expire_s: expiration date delta en seconds
                         all objects inserted will use this delta to set their own expiration date
        :return:
        """
        self._list = []
        self.expire_s = expire_s
        self.arrow_factory = arrow.ArrowFactory(ExpireArrow)

    def append(self, p_object, expire_s=None) -> None:
        """
        Append new object in the list
        :param p_object: object to add to the list
        :param expire_s: (optional) if you want to use a different expiration date in seconds
        """
        if expire_s is None:
            expire_s = self.expire_s
        expiration_date = self.arrow_factory.now().expiration(seconds=expire_s)
        self._list.append((expiration_date, p_object))

    def pop(self) -> object:
        """
        :return: first element stored in the list (FIFO)
        :raise: ExpireFifo.ExpiredValueError if the data is expired
        """
        # list.pop(0) = take first element stored
        while not self.is_empty():
            expiration_date, p_object = self._list.pop(0)
            if not expiration_date.is_expired():
                return p_object

            del expiration_date
            del p_object

        raise KeyError

    def is_empty(self):
        """
        :return: true is the ExpireFifo is empty
        """
        return 0 == len(self._list)

    class ExpiredValueError(TimeoutError):
        """
        raise this when data is expired on pop()
        """
        pass


class ExpireDict(dict):
    def __init__(self, expire_s=None):
        """
        :param expire_s: expiration date delta en seconds
                         all objects inserted will use this delta to set their own expiration date
        :return:
        """
        super().__init__()
        self.expire_s = expire_s
        self.arrow_factory = arrow.ArrowFactory(ExpireArrow)

    def add(self, key, value, expire_s=None):
        if not expire_s:
            expire_s = self.expire_s
        expiration_date = self.arrow_factory.now().expiration(seconds=expire_s)
        super().__setitem__(key, (value, expiration_date))

    def __setitem__(self, key, value):
        self.add(key, value)

    def get(self, k, d=None):
        self.clean_up()
        p_object, expiration_date = super().get(k, d)
        return p_object

    def pop(self, k, d=None):
        self.clean_up()
        p_object, expiration_date = super().pop(k, d)
        return p_object

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, item):
        self.clean_up()
        return super().__contains__(item)

    def clean_up(self):
        for key in list(super().keys()):
            val = super().get(key)
            p_object, expiration_date = val
            if expiration_date.is_expired():
                super().__delitem__(key)

