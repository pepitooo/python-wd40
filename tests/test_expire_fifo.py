from unittest import TestCase

import arrow
import time

from wd40.expire_fifo import ExpireArrow, ExpireDict, ExpireFifo


class TestDeadManAlarm(TestCase):

    def test_not_yet_expire(self):
        factory = arrow.ArrowFactory(ExpireArrow)
        future = factory.utcnow().replace(seconds=1)
        assert(not future.is_expired())

    def test_expire(self):
        factory = arrow.ArrowFactory(ExpireArrow)
        # replace seconds=xxx is used to go forward or backward on time
        past = factory.utcnow().replace(seconds=-1)
        assert(past.is_expired())

    def test_expire_with_sleep(self):
        factory = arrow.ArrowFactory(ExpireArrow)
        utc = factory.utcnow().expiration(seconds=0.1)
        time.sleep(0.2)
        assert(utc.is_expired())

    def test_not_yet_expire_with_sleep(self):
        factory = arrow.ArrowFactory(ExpireArrow)
        utc = factory.utcnow().expiration(seconds=0.2)
        time.sleep(0.1)
        assert(not utc.is_expired())

    def test_expiration(self):
        factory = arrow.ArrowFactory(ExpireArrow)
        expiration_date = factory.utcnow().expiration(seconds=0.1)
        assert(arrow.utcnow() < expiration_date)
        time.sleep(0.2)
        assert(arrow.utcnow() > expiration_date)

    def test_expire_list_as_normal_list(self):
        expire_list = ExpireFifo(expire_s=10)
        expire_list.append(1)
        expire_list.append(2)
        expire_list.append(3)
        assert 1 == expire_list.pop()
        assert 2 == expire_list.pop()
        assert 3 == expire_list.pop()
        assert expire_list.is_empty()

    def test_expire_list_with_expired_data(self):
        expire_list = ExpireFifo(expire_s=0.1)
        expire_list.append(1)
        expire_list.append(2, expire_s=0.3)
        time.sleep(0.2)
        expire_list.append(3)
        assert 2 == expire_list.pop()
        assert 3 == expire_list.pop()
        assert expire_list.is_empty()

    def test_expire_dict_as_normal_dict(self):
        expire_dict = ExpireDict(expire_s=10)
        expire_dict.add('1', 1)
        expire_dict.add('2', 2)
        expire_dict.add('3', 3)
        assert 1 == expire_dict.pop('1')
        assert 2 == expire_dict.pop('2')
        assert 3 == expire_dict.pop('3')
        assert 0 == len(expire_dict)

    def test_expire_dict_with_expired_data(self):
        expire_dict = ExpireDict(expire_s=0.1)
        expire_dict.add('1', 1)
        expire_dict.add('2', 2, expire_s=0.3)
        time.sleep(0.2)
        expire_dict.add('3', 3)
        assert 2 == expire_dict.pop('2')
        assert 3 == expire_dict.pop('3')
        assert 0 == len(expire_dict)

    def test_expire_dict_in_not_in(self):
        expire_dict = ExpireDict(expire_s=0.1)
        expire_dict.add('1', 1, expire_s=10)
        expire_dict.add('2', 2, expire_s=10)
        expire_dict.add('3', 3)
        time.sleep(0.2)
        assert '1' in expire_dict
        assert '2' in expire_dict
        assert '3' not in expire_dict
