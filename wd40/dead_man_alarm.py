import threading


class DeadManAlarm(threading.Thread):
    def __init__(self, seconds_before_action, action):
        super().__init__(name='DeadManAlarm')
        self.seconds_before_action = seconds_before_action
        self.action = action
        self._is_running = False
        self.lock = threading.Event()

    def run(self):
        self._is_running = True
        while self._is_running:
            if not self.lock.wait(self.seconds_before_action):
                if self._is_running:
                    self.action()
            else:
                self.lock.clear()

    def stop(self):
        self._is_running = False
        self.lock.set()

    def i_m_alive(self):
        self.lock.set()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

