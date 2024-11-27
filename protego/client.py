import time
from threading import Lock


class ProtegoClientState:
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class ProtegoClient:
    def __init__(self):
        self.state = ProtegoClientState.CLOSED
        self.failures = 0
        self.last_failure_time = 0
        self.half_open_attempts = 0
        self.lock = Lock()

    def call(self, func, *args, **kwargs):
        failure_threshold = kwargs.pop("failure_threshold", self.default_failure_threshold)
        reset_timeout = kwargs.pop("reset_timeout", self.default_reset_timeout)
        half_open_retries = kwargs.pop("half_open_retries", self.default_half_open_retries)

        with self.lock:
            if self.state == ProtegoClientState.OPEN:
                if time.time() - self.last_failure_time > reset_timeout:
                    self.state = ProtegoClientState.HALF_OPEN
                    self.half_open_attempts = 0
                else:
                    raise Exception("Circuit is open. Request blocked.")

            if self.state == ProtegoClientState.HALF_OPEN and self.half_open_attempts >= half_open_retries:
                raise Exception("Circuit is half-open. Retry limit reached.")

        try:
            result = func(*args, **kwargs)
            self._reset()
            return result
        except Exception as e:
            self._record_failure(failure_threshold)
            raise e

    def _reset(self):
        with self.lock:
            self.state = ProtegoClientState.CLOSED
            self.failures = 0
            self.last_failure_time = 0
            self.half_open_attempts = 0

    def _record_failure(self, failure_threshold):
        with self.lock:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= failure_threshold:
                self.state = ProtegoClientState.OPEN
