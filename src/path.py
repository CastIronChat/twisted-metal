from __future__ import annotations

from curve import Curve


class Path:
    """
    Hacky combination of two Curves to produce a timeline of 2d vectors.
    """

    def __init__(self, points: list[tuple[float, float, float]] = []):
        x_points = [(t[0], t[1]) for t in points]
        y_points = [(t[0], t[2]) for t in points]
        self._x_curve = Curve(x_points)
        self._y_curve = Curve(y_points)

    @property
    def min_time(self):
        return self._x_curve.points[0][0]

    @property
    def max_time(self):
        return self._x_curve.points[-1][0]

    def sample(self, sample_time: float):
        return (self._x_curve.sample(sample_time), self._y_curve.sample(sample_time))
