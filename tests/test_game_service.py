"""
test_game_service.py - GameService birim testleri
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from src.services.game_service import GameService
from src.modules.game_state import GamePhase
from src.core.board import Board


class TestGameService(unittest.TestCase):

    def setUp(self):
        self.svc = GameService("TestOyuncu", "kolay")

    def test_initial_phase_menu(self):
        from src.modules.game_state import GamePhase
        self.assertEqual(self.svc.state.phase, GamePhase.MAIN_MENU)

    def test_placement_phase_starts(self):
        self.svc.start_placement_phase()
        self.assertEqual(self.svc.state.phase, GamePhase.SHIP_PLACEMENT)

    def test_placement_advances_ship_index(self):
        self.svc.start_placement_phase()
        initial_idx = self.svc.state.placement_ship_index
        # İlk gemi 5 kare, 0,0 konumuna yatay sığar
        result = self.svc.try_place_ship(0, 0)
        self.assertTrue(result)
        self.assertEqual(self.svc.state.placement_ship_index, initial_idx + 1)

    def test_toggle_orientation(self):
        self.svc.start_placement_phase()
        initial = self.svc.state.placement_horizontal
        self.svc.toggle_placement_orientation()
        self.assertNotEqual(self.svc.state.placement_horizontal, initial)

    def test_player_attack_before_game_returns_none(self):
        result = self.svc.player_attack(0, 0)
        self.assertIsNone(result)

    def test_reset(self):
        self.svc.start_placement_phase()
        self.svc.reset()
        self.assertEqual(self.svc.state.phase, GamePhase.MAIN_MENU)


if __name__ == "__main__":
    unittest.main()
