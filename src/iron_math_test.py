from __future__ import annotations

import unittest

import iron_math as iron_math


class RescaleValueBetween(unittest.TestCase):
    def test_rescale_value_between(self):
        v = iron_math.rescale_value_between(0, 5, 10)
        self.assertEqual(v, -1)

        v = iron_math.rescale_value_between(5, 5, 10)
        self.assertEqual(v, 0)

        v = iron_math.rescale_value_between(10, 5, 10)
        self.assertEqual(v, 1)

        v = iron_math.rescale_value_between(10, 5, 10)
        self.assertEqual(v, 1)

        v = iron_math.rescale_value_between(10, 5, 10, -100, 100)
        self.assertEqual(v, 100)

        v = iron_math.rescale_value_between(20, 5, 10, -100, 100)
        self.assertEqual(v, 500)
