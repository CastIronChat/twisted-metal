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


class AddVec(unittest.TestCase):
    def test_adding_many_vecs(self):
        x, y = iron_math.add_vec((0.0, 1.0), (0.0, 2.0), (1.0, 0.0))
        self.assertEqual(x, 1)
        self.assertEqual(y, 3)

        x, y = iron_math.add_vec((0.0, 1.0))
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

        x, y = iron_math.add_vec()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
