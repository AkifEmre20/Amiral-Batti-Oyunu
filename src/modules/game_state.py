"""
game_state.py - Oyun durumu yönetimi (State Pattern)
"""
from enum import Enum, auto


class GamePhase(Enum):
    MAIN_MENU = auto()        # Ana menü
    SHIP_PLACEMENT = auto()   # Gemi yerleştirme aşaması
    PLAYER_TURN = auto()      # Oyuncu sırası
    AI_TURN = auto()          # AI sırası
    GAME_OVER = auto()        # Oyun bitti


class AttackResult:
    """Saldırı sonucunu taşıyan veri sınıfı"""

    def __init__(self, row: int, col: int, result_code: int,
                 ship_name: str | None = None, is_player_attack: bool = True):
        self.row = row
        self.col = col
        self.result_code = result_code  # Board.HIT / MISS / SUNK
        self.ship_name = ship_name
        self.is_player_attack = is_player_attack

    @property
    def is_hit(self) -> bool:
        from src.core.board import Board
        return self.result_code in (Board.HIT, Board.SUNK)

    @property
    def is_sunk(self) -> bool:
        from src.core.board import Board
        return self.result_code == Board.SUNK

    def __repr__(self):
        tag = "VURUŞ" if self.is_hit else "ISKALADI"
        sunk = f" ({self.ship_name} BATTI!)" if self.is_sunk else ""
        actor = "Oyuncu" if self.is_player_attack else "Bilgisayar"
        return f"{actor} ({self.row},{self.col}) → {tag}{sunk}"


class GameState:
    """Anlık oyun durumu"""

    def __init__(self):
        self.phase = GamePhase.MAIN_MENU
        self.round_number = 0
        self.attack_log: list[AttackResult] = []
        self.winner: str | None = None
        self.placement_ship_index = 0   # Şu an yerleştirilen gemi indeksi
        self.placement_horizontal = True

    def next_phase(self, phase: GamePhase):
        self.phase = phase

    def add_attack_log(self, result: AttackResult):
        self.attack_log.append(result)
        if result.is_player_attack:
            self.round_number += 1

    def set_winner(self, winner_name: str):
        self.winner = winner_name
        self.phase = GamePhase.GAME_OVER

    @property
    def last_attack(self) -> AttackResult | None:
        return self.attack_log[-1] if self.attack_log else None
