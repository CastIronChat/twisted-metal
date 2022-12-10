from __future__ import annotations

from iron_math import rescale_value_between


class Curve:
    """
    Given a set of points on a graph connected by straight lines, you can sample
    the graph at any X value and get the Y value.
    The graph is flat to the left of the first point and to the right of the last point.

    Despite the name "curve", there are no curves here, only straight lines.

    A Curve with a single point is a flat line.  Y is constant for all X values.
    """

    def __init__(self, points: list[tuple[float, float]] = []):
        self.points = points

    def sample(self, sample_x: float):
        if sample_x <= self.points[0][0]:
            return self.points[0][1]
        if sample_x >= self.points[-1][0]:
            return self.points[-1][1]
        for index, point in enumerate(self.points[1:]):
            if sample_x < point[0]:
                return rescale_value_between(
                    sample_x,
                    self.points[index][0],
                    point[0],
                    self.points[index][1],
                    point[1],
                )
