import time
import threading


class Analytics:
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.model_usage = {}  # model -> count
        self.language_usage = {}  # language -> count
        self.response_times = []
        self._lock = threading.Lock()
        self._request_starts = {}

    def on_request(self, model, language):
        with self._lock:
            self.total_requests += 1
            self.model_usage[model] = self.model_usage.get(model, 0) + 1
            self.language_usage[language] = self.language_usage.get(language, 0) + 1
            self._request_starts[threading.get_ident()] = time.time()

    def on_success(self, model=None):
        with self._lock:
            start = self._request_starts.pop(threading.get_ident(), None)
            if start:
                self.response_times.append(time.time() - start)

    def on_error(self, model=None):
        with self._lock:
            self.total_errors += 1
            self._request_starts.pop(threading.get_ident(), None)

    def get_avg_response_time(self):
        with self._lock:
            if not self.response_times:
                return 0.0
            return sum(self.response_times) / len(self.response_times)

    def get_error_rate(self):
        with self._lock:
            if self.total_requests == 0:
                return 0.0
            return self.total_errors / self.total_requests

    def get_summary(self):
        with self._lock:
            return {
                "total_requests": self.total_requests,
                "total_errors": self.total_errors,
                "error_rate": self.total_errors / self.total_requests if self.total_requests > 0 else 0.0,
                "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0.0,
                "model_usage": dict(self.model_usage),
                "language_usage": dict(self.language_usage),
            }


# singleton
analytics = Analytics()
