"""
game_service.py - Oyun iş mantığı katmanı
UI ile core arasındaki köprü
"""
import time
from src.core.board import Board
from src.core.player import HumanPlayer, AIPlayer
from src.core.ship import SHIP_CLASSES
from src.modules.game_state import GameState, GamePhase, AttackResult
from src.services.score_service import ScoreService


class GameService:
    """Oyun akışını yöneten servis sınıfı"""

    HIT_SCORE = 10
    SUNK_BONUS = 50
    WIN_BONUS = 200

    def __init__(self, player_name: str = "Oyuncu", ai_difficulty: str = AIPlayer.MEDIUM):
        self._human = HumanPlayer(player_name)
        self._ai = AIPlayer(ai_difficulty)
        self._state = GameState()
        self._score_service = ScoreService()
        self._placement_ships = [ShipClass() for ShipClass in SHIP_CLASSES]

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def human(self) -> HumanPlayer:
        return self._human

    @property
    def ai(self) -> AIPlayer:
        return self._ai

    @property
    def current_placement_ship(self):
        """Şu an yerleştirilen gemi"""
        idx = self._state.placement_ship_index
        if idx < len(self._placement_ships):
            return self._placement_ships[idx]
        return None

    def start_placement_phase(self):
        """Gemi yerleştirme aşamasını başlat"""
        self._state.next_phase(GamePhase.SHIP_PLACEMENT)
        self._state.placement_ship_index = 0

    def try_place_ship(self, row: int, col: int) -> bool:
        """
        Mevcut gemiyi (row, col) konumuna yerleştirmeyi dene.
        Başarılıysa True döndür ve bir sonraki gemiye geç.
        """
        ship = self.current_placement_ship
        if ship is None:
            return False

        horizontal = self._state.placement_horizontal
        success = self._human.board.place_ship(ship, row, col, horizontal)
        if success:
            self._state.placement_ship_index += 1
            # Tüm gemiler yerleştirildiyse oyunu başlat
            if self._state.placement_ship_index >= len(self._placement_ships):
                self._ai.setup_ships()
                self._state.next_phase(GamePhase.PLAYER_TURN)
        return success

    def toggle_placement_orientation(self):
        self._state.placement_horizontal = not self._state.placement_horizontal

    def player_attack(self, row: int, col: int) -> AttackResult | None:
        """
        Oyuncu saldırısını işle.
        Faz PLAYER_TURN değilse veya hücre daha önce vurulduysa None döndür.
        """
        if self._state.phase != GamePhase.PLAYER_TURN:
            return None
        if self._human.has_attacked(row, col):
            return None

        self._human.record_attack(row, col)
        result_code = self._ai.board.receive_attack(row, col)

        if result_code == -1:
            return None

        ship_name = None
        if result_code in (Board.HIT, Board.SUNK):
            self._human.add_score(self.HIT_SCORE)
            ship = self._ai.board.get_ship_at(row, col)
            if result_code == Board.SUNK and ship:
                ship_name = ship.name
                self._human.add_score(self.SUNK_BONUS)

        attack = AttackResult(row, col, result_code, ship_name, is_player_attack=True)
        self._state.add_attack_log(attack)

        # Oyun bitti mi?
        if self._ai.board.all_ships_sunk():
            self._human.add_score(self.WIN_BONUS)
            self._score_service.save_score(self._human.name, self._human.score)
            self._state.set_winner(self._human.name)
        else:
            self._state.next_phase(GamePhase.AI_TURN)

        return attack

    def ai_attack(self) -> AttackResult:
        """AI saldırısını işle ve sonucu döndür"""
        row, col = self._ai.choose_attack(self._human.board)
        self._ai.record_attack(row, col)
        result_code = self._human.board.receive_attack(row, col)

        ship_name = None
        if result_code in (Board.HIT, Board.SUNK):
            ship = self._human.board.get_ship_at(row, col)
            if result_code == Board.SUNK and ship:
                ship_name = ship.name

        self._ai.notify_hit_result(row, col, result_code)

        attack = AttackResult(row, col, result_code, ship_name, is_player_attack=False)
        self._state.add_attack_log(attack)

        if self._human.board.all_ships_sunk():
            self._score_service.save_score(self._human.name, self._human.score)
            self._state.set_winner(self._ai.name)
        else:
            self._state.next_phase(GamePhase.PLAYER_TURN)

        return attack

    def reset(self, player_name: str = None, ai_difficulty: str = None):
        """Oyunu sıfırla"""
        name = player_name or self._human.name
        diff = ai_difficulty or self._ai.difficulty
        self.__init__(name, diff)

    def get_scores(self) -> list[dict]:
        return self._score_service.get_top_scores()
