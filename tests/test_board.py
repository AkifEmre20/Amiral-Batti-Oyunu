"""
test_board.py - Board sınıfı birim testleri
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from src.core.board import Board
from src.core.ship import Destroyer, Submarine, Battleship


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board("Test")
        self.destroyer = Destroyer()

    def test_place_ship_valid(self):
        success = self.board.place_ship(self.destroyer, 0, 0, True)
        self.assertTrue(success)

    def test_place_ship_out_of_bounds(self):
        success = self.board.place_ship(self.destroyer, 0, 9, True)  # 2 kare sığmaz
        self.assertFalse(success)

    def test_place_ship_overlap(self):
        sub = Submarine()
        self.board.place_ship(self.destroyer, 0, 0, True)
        success = self.board.place_ship(sub, 0, 0, True)
        self.assertFalse(success)

    def test_attack_hit(self):
        self.board.place_ship(self.destroyer, 3, 3, True)
        result = self.board.receive_attack(3, 3)
        self.assertEqual(result, Board.HIT)

    def test_attack_miss(self):
        result = self.board.receive_attack(5, 5)
        self.assertEqual(result, Board.MISS)

    def test_attack_sunk(self):
        self.board.place_ship(self.destroyer, 2, 2, True)
        self.board.receive_attack(2, 2)
        result = self.board.receive_attack(2, 3)
        self.assertEqual(result, Board.SUNK)

    def test_duplicate_attack(self):
        self.board.receive_attack(0, 0)
        result = self.board.receive_attack(0, 0)
        self.assertEqual(result, -1)

    def test_all_ships_sunk(self):
        self.board.place_ship(self.destroyer, 0, 0, True)
        self.board.receive_attack(0, 0)
        self.board.receive_attack(0, 1)
        self.assertTrue(self.board.all_ships_sunk())


class TestShip(unittest.TestCase):

    def test_ship_properties(self):
        d = Destroyer()
        self.assertEqual(d.size, 2)
        self.assertEqual(d.name, "Muhrip")

    def test_ship_not_sunk_initially(self):
        d = Destroyer()
        d.place([(0, 0), (0, 1)])
        self.assertFalse(d.is_sunk())

    def test_ship_sunk_after_all_hits(self):
        d = Destroyer()
        d.place([(0, 0), (0, 1)])
        d.receive_hit(0, 0)
        d.receive_hit(0, 1)
        self.assertTrue(d.is_sunk())

    def test_polymorphism(self):
        """Polymorphism: tüm gemi türleri aynı arayüzü destekler"""
        from src.core.ship import SHIP_CLASSES
        for ShipClass in SHIP_CLASSES:
            ship = ShipClass()
            self.assertTrue(hasattr(ship, "name"))
            self.assertTrue(hasattr(ship, "size"))
            self.assertTrue(hasattr(ship, "is_sunk"))
            self.assertTrue(hasattr(ship, "receive_hit"))


if __name__ == "__main__":
    unittest.main()
