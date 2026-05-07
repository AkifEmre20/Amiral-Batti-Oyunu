"""
player.py - Oyuncu sınıfları (İnsan ve AI)
Polymorphism örneği: choose_attack() metodu her alt sınıfta farklı davranır
"""
import random
from abc import ABC, abstractmethod
from src.core.board import Board
from src.core.ship import SHIP_CLASSES


class Player(ABC):
    """Soyut temel oyuncu sınıfı"""

    def __init__(self, name: str):
        self._name = name
        self._board = Board(name)
        self._attack_history: set[tuple[int, int]] = set()
        self._score = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def board(self) -> Board:
        return self._board

    @property
    def score(self) -> int:
        return self._score

    def add_score(self, points: int):
        self._score += points

    def has_attacked(self, row: int, col: int) -> bool:
        return (row, col) in self._attack_history

    def record_attack(self, row: int, col: int):
        self._attack_history.add((row, col))

    def get_attack_history(self) -> set[tuple[int, int]]:
        return set(self._attack_history)

    @abstractmethod
    def choose_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Saldırı koordinatını seç (Polymorphism)"""
        pass

    def setup_ships(self):
        """Gemileri tahtaya yerleştir"""
        for ShipClass in SHIP_CLASSES:
            ship = ShipClass()
            self._place_ship_randomly(ship)

    def _place_ship_randomly(self, ship):
        """Gemiyi rastgele konuma yerleştir"""
        placed = False
        while not placed:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            horizontal = random.choice([True, False])
            placed = self._board.place_ship(ship, row, col, horizontal)


class HumanPlayer(Player):
    """İnsan oyuncusu - saldırı UI'dan gelir"""

    def __init__(self, name: str):
        super().__init__(name)

    def choose_attack(self, enemy_board: Board) -> tuple[int, int]:
        """
        İnsan oyuncusu için bu metot UI tarafından dışarıdan çağrılır.
        GameService üzerinden koordinat iletilir.
        """
        raise NotImplementedError("İnsan oyuncusunun saldırısı UI üzerinden yapılır.")


class AIPlayer(Player):
    """Yapay zeka oyuncusu"""

    # AI zorluk seviyeleri
    EASY = "kolay"
    MEDIUM = "orta"
    HARD = "zor"

    def __init__(self, difficulty: str = MEDIUM):
        super().__init__("Bilgisayar")
        self._difficulty = difficulty
        self._hunt_targets: list[tuple[int, int]] = []  # Hedef listesi (hit sonrası)
        self._last_hit: tuple[int, int] | None = None
        self._hunt_direction: str | None = None  # "H" veya "V"

    @property
    def difficulty(self) -> str:
        return self._difficulty

    def choose_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Zorluk seviyesine göre saldırı seç (Polymorphism)"""
        if self._difficulty == self.EASY:
            return self._random_attack(enemy_board)
        elif self._difficulty == self.MEDIUM:
            return self._smart_attack(enemy_board)
        else:
            return self._hard_attack(enemy_board)

    def notify_hit_result(self, row: int, col: int, result: int):
        """Saldırı sonucunu AI'ya bildir (hedef güncelleme için)"""
        from src.core.board import Board as B
        if result == B.HIT:
            self._last_hit = (row, col)
            self._add_adjacent_targets(row, col)
        elif result == B.SUNK:
            self._hunt_targets.clear()
            self._last_hit = None
            self._hunt_direction = None

    def _random_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Rastgele saldırı (Kolay mod)"""
        available = [
            (r, c)
            for r in range(10) for c in range(10)
            if not self.has_attacked(r, c)
        ]
        return random.choice(available)

    def _smart_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Hunt & Target algoritması (Orta mod)"""
        if self._hunt_targets:
            target = self._hunt_targets.pop(0)
            while self.has_attacked(*target) and self._hunt_targets:
                target = self._hunt_targets.pop(0)
            if not self.has_attacked(*target):
                return target

        # Checkerboard pattern ile arama
        available = [
            (r, c)
            for r in range(10) for c in range(10)
            if not self.has_attacked(r, c) and (r + c) % 2 == 0
        ]
        if not available:
            available = [
                (r, c)
                for r in range(10) for c in range(10)
                if not self.has_attacked(r, c)
            ]
        return random.choice(available)

    def _hard_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Gelişmiş Hunt & Target (Zor mod)"""
        if self._hunt_targets:
            target = self._hunt_targets.pop(0)
            while self.has_attacked(*target) and self._hunt_targets:
                target = self._hunt_targets.pop(0)
            if not self.has_attacked(*target):
                return target

        # Olasılık haritası hesapla
        return self._probability_attack(enemy_board)

    def _probability_attack(self, enemy_board: Board) -> tuple[int, int]:
        """Olasılık yoğunluk haritasına göre en iyi hücreyi seç"""
        prob_map = [[0] * 10 for _ in range(10)]
        # En küçük batmamış gemi boyutuna göre olasılık hesapla
        min_size = 2
        for r in range(10):
            for c in range(10):
                if not self.has_attacked(r, c):
                    # Yatay
                    for sz in range(min_size, 6):
                        if all(
                            0 <= c + i < 10 and not self.has_attacked(r, c + i)
                            for i in range(sz)
                        ):
                            for i in range(sz):
                                prob_map[r][c + i] += 1
                    # Dikey
                    for sz in range(min_size, 6):
                        if all(
                            0 <= r + i < 10 and not self.has_attacked(r + i, c)
                            for i in range(sz)
                        ):
                            for i in range(sz):
                                prob_map[r + i][c] += 1

        best_val = -1
        best_pos = (0, 0)
        for r in range(10):
            for c in range(10):
                if not self.has_attacked(r, c) and prob_map[r][c] > best_val:
                    best_val = prob_map[r][c]
                    best_pos = (r, c)
        return best_pos

    def _add_adjacent_targets(self, row: int, col: int):
        """Vurulan hücrenin komşularını hedef listesine ekle"""
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and not self.has_attacked(nr, nc):
                if (nr, nc) not in self._hunt_targets:
                    self._hunt_targets.append((nr, nc))
