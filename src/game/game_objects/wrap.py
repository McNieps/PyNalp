import math


class Wrap:
    def __init__(self, d_max: int, t_max: float, severity: float = 8):
        """
        severity ]1, +inf[
        """

        self.severity = severity
        self.speed = d_max / (severity - 1)

        self.current_duration = 0
        self.max_duration = t_max

        self.current_distance = 0
        self.max_distance = d_max

        self.over = True

        self.offset = 0

    def init_wrap(self):
        self.over = False

    def compute(self, delta: float):
        if self.over:
            return

        self.current_duration += delta

        if self.current_duration > self.max_duration:
            self.over = True

            self.current_duration = 0
            self.current_distance = 0

            self.offset += self.max_distance
            return

        time_ratio = self.current_duration / self.max_duration * self.severity

        self.current_distance = self.speed * (time_ratio - math.exp(time_ratio-self.severity))

        # return wrap_speed * (wrap_duration * 5 - math.exp(wrap_duration * 5 - 10))

    @property
    def distance(self):
        return self.offset + self.current_distance
