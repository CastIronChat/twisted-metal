from __future__ import annotations

from unittest import TestCase

from rounds.game_modes.stock import StockGameMode


class TestStock(TestCase):
    def test_stock(self):
        mode = StockGameMode()
