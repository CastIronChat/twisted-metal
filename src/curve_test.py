from __future__ import annotations

from unittest import TestCase

import curve


class TestCurve(TestCase):
    def test_sample(self):
        c = curve.Curve([(0.1, 20), (0.8, 500)])

        v = c.sample(-10)
        self.assertEqual(v, 20)

        v = c.sample(600)
        self.assertEqual(v, 500)

        v = c.sample(0.1)
        self.assertEqual(v, 20)

        v = c.sample(0.8)
        self.assertEqual(v, 500)

        v = c.sample(0.2)
        # 1/7 of the way between 20 and 500
        # = 20 + (480/7) =
        self.assertAlmostEqual(v, 88, delta=1)
