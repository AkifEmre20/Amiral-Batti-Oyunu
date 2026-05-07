"""
ship.py - Gemi sınıfı ve türevleri
Encapsulation ve Inheritance örneği
"""


class Ship:
    """Temel gemi sınıfı (Base Class)"""

    def __init__(self, name: str, size: int, symbol: str):
        # Encapsulation: özel alanlar
        self._name = name
        self._size = size
        self._symbol = symbol
        self._positions: list[tuple[int, int]] = []
        self._hits: set[tuple[int, int]] = set()
        self._is_horizontal = True

    # --- Property'ler (Encapsulation) ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def positions(self) -> list[tuple[int, int]]:
        return list(self._positions)

    @property
    def is_horizontal(self) -> bool:
        return self._is_horizontal

    @is_horizontal.setter
    def is_horizontal(self, value: bool):
        self._is_horizontal = value

    def place(self, positions: list[tuple[int, int]]):
        """Gemiyi belirtilen pozisyonlara yerleştir"""
        if len(positions) != self._size:
            raise ValueError(f"{self._name} için {self._size} pozisyon gerekli, {len(positions)} verildi.")
        self._positions = list(positions)

    def receive_hit(self, row: int, col: int) -> bool:
        """Gemi bu koordinatta mı? Vuruşu kaydet, True döndür."""
        pos = (row, col)
        if pos in self._positions:
            self._hits.add(pos)
            return True
        return False

    def is_sunk(self) -> bool:
        """Gemi batmış mı?"""
        return len(self._hits) == self._size

    def get_hit_positions(self) -> set[tuple[int, int]]:
        return set(self._hits)

    def __repr__(self):
        status = "BATIK" if self.is_sunk() else f"{len(self._hits)}/{self._size} vuruş"
        return f"{self._name}({self._size}) [{status}]"


# --- Kalıtım (Inheritance) ile gemi türleri ---

class Destroyer(Ship):
    """Muhrip - 2 kare"""
    def __init__(self):
        super().__init__(name="Muhrip", size=2, symbol="M")

    def get_description(self) -> str:
        return "Hızlı ve çevik, 2 karelik küçük gemi."


class Submarine(Ship):
    """Denizaltı - 3 kare"""
    def __init__(self):
        super().__init__(name="Denizaltı", size=3, symbol="D")

    def get_description(self) -> str:
        return "Su altında gizlenen, 3 karelik gemi."


class Battleship(Ship):
    """Savaş gemisi - 4 kare"""
    def __init__(self):
        super().__init__(name="Savaş Gemisi", size=4, symbol="S")

    def get_description(self) -> str:
        return "Güçlü ve dayanıklı, 4 karelik gemi."


class Carrier(Ship):
    """Uçak gemisi - 5 kare"""
    def __init__(self):
        super().__init__(name="Uçak Gemisi", size=5, symbol="U")

    def get_description(self) -> str:
        return "En büyük gemi, 5 kare kaplar."


# Polymorphism: tüm gemileri aynı arayüzle kullanabiliriz
SHIP_CLASSES = [Carrier, Battleship, Submarine, Submarine, Destroyer]
