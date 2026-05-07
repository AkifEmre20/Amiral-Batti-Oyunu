"""
board.py - Oyun tahtası sınıfı
"""
from src.core.ship import Ship

GRID_SIZE = 10


class Board:
    """10x10 oyun tahtasını temsil eder"""

    # Hücre durumları
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3
    SUNK = 4

    def __init__(self, owner: str):
        self._owner = owner
        # 2D grid: her hücre EMPTY/SHIP/HIT/MISS/SUNK
        self._grid: list[list[int]] = [[self.EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
        self._ships: list[Ship] = []

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def grid(self) -> list[list[int]]:
        return [row[:] for row in self._grid]

    @property
    def ships(self) -> list[Ship]:
        return list(self._ships)

    def is_valid_placement(self, row: int, col: int, size: int, horizontal: bool) -> bool:
        """Gemi yerleşimi geçerli mi?"""
        try:
            positions = self._calculate_positions(row, col, size, horizontal)
        except ValueError:
            return False

        for r, c in positions:
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                return False
            if self._grid[r][c] != self.EMPTY:
                return False
            # Komşu hücre kontrolü (gemiler birbirine değemez)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if self._grid[nr][nc] == self.SHIP and (nr, nc) not in positions:
                            return False
        return True

    def place_ship(self, ship: Ship, row: int, col: int, horizontal: bool) -> bool:
        """Gemiyi tahtaya yerleştir. Başarılı ise True döndür."""
        if not self.is_valid_placement(row, col, ship.size, horizontal):
            return False

        positions = self._calculate_positions(row, col, ship.size, horizontal)
        ship.is_horizontal = horizontal
        ship.place(positions)

        for r, c in positions:
            self._grid[r][c] = self.SHIP

        self._ships.append(ship)
        return True

    def receive_attack(self, row: int, col: int) -> int:
        """
        Koordinata saldır.
        Döndür: HIT, MISS, SUNK veya -1 (daha önce vurulmuş)
        """
        if self._grid[row][col] in (self.HIT, self.MISS, self.SUNK):
            return -1  # Zaten vurulmuş

        for ship in self._ships:
            if ship.receive_hit(row, col):
                if ship.is_sunk():
                    # Batan geminin tüm pozisyonlarını SUNK yap
                    for r, c in ship.positions:
                        self._grid[r][c] = self.SUNK
                    return self.SUNK
                else:
                    self._grid[row][col] = self.HIT
                    return self.HIT

        self._grid[row][col] = self.MISS
        return self.MISS

    def all_ships_sunk(self) -> bool:
        """Tüm gemiler battı mı?"""
        return all(ship.is_sunk() for ship in self._ships)

    def get_ship_at(self, row: int, col: int) -> Ship | None:
        """Belirtilen koordinattaki gemi"""
        for ship in self._ships:
            if (row, col) in ship.positions:
                return ship
        return None

    def _calculate_positions(self, row: int, col: int, size: int, horizontal: bool) -> list[tuple[int, int]]:
        positions = []
        for i in range(size):
            if horizontal:
                positions.append((row, col + i))
            else:
                positions.append((row + i, col))
        return positions

    def __repr__(self):
        lines = [f"Tahta ({self._owner}):"]
        header = "   " + " ".join(str(i) for i in range(GRID_SIZE))
        lines.append(header)
        symbols = {self.EMPTY: ".", self.SHIP: "S", self.HIT: "X", self.MISS: "O", self.SUNK: "#"}
        for i, row in enumerate(self._grid):
            row_str = f"{i:2} " + " ".join(symbols.get(c, "?") for c in row)
            lines.append(row_str)
        return "\n".join(lines)
