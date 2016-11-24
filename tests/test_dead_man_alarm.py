import queue
from unittest import TestCase

import time

from wd40.dead_man_alarm import DeadManAlarm

stack_msg = queue.Queue()
action_counter = 0


def action():
    global action_counter
    action_counter += 1
    stack_msg.put(action_counter)


class TestDeadManAlarm(TestCase):

    def test_man_is_not_dead(self):
        assert stack_msg.empty()
        dma = DeadManAlarm(0.5, lambda: action())
        with dma:
            dma.i_m_alive()
            assert stack_msg.empty()

    def test_man_is_dead(self):
        assert stack_msg.empty()
        dma = DeadManAlarm(0.5, lambda: action())
        with dma:
            # dma.i_m_alive()
            time.sleep(0.6)
            assert not stack_msg.empty()
            assert stack_msg.get_nowait()

    def test_no_false_alarm_on_stop(self):
        assert stack_msg.empty()
        dma = DeadManAlarm(0.5, lambda: action())
        with dma:
            pass
        assert stack_msg.empty()

    def test_man_will_die(self):
        assert stack_msg.empty()
        dma = DeadManAlarm(0.5, lambda: action())
        with dma:
            dma.i_m_alive()
            time.sleep(0.4)
            dma.i_m_alive()
            assert stack_msg.empty()
            time.sleep(0.4)
            dma.i_m_alive()
            assert stack_msg.empty()
            time.sleep(0.6)
            assert not stack_msg.empty()
            assert stack_msg.get_nowait()
