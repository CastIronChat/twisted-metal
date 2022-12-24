from __future__ import annotations

ns_per_ms = 1e6


class PingAverage:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.window = []
        self.average_ms = 0

    def log_data_point(self, ping_ns: int):
        self.window.insert(0, ping_ns)
        if len(self.window) > self.window_size:
            self.window.pop()
        self.average_ms = int(sum(self.window) / len(self.window) / ns_per_ms)
