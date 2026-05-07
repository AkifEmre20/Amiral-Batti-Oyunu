"""
renderer.py - Oyun tahtasını ve UI bileşenlerini ekrana çizen sınıf
"""
import pygame
import math
import os
from src.ui.theme import *
from src.core.board import Board


class GridRenderer:
    """Oyun ızgarasını modern efektlerle çizen sınıf"""

    def __init__(self, origin_x: int, origin_y: int, cell_size: int = CELL_SIZE):
        self._ox = origin_x
        self._oy = origin_y
        self._cs = cell_size
        self._time = 0.0
        # Patlama animasyonları: {(r,c): elapsed}
        self._explosions: dict[tuple[int, int], float] = {}
        # Doku atlası
        self._textures: dict[str, pygame.Surface] = {}
        self._load_textures()

    def _load_textures(self):
        """assets/images/ klasöründen hücre dokularını yükle"""
        inner = self._cs - 4  # padding 2 her tarafta
        base = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "assets", "images")
        )
        names = ["water_cell", "ship_cell", "hit_cell", "miss_cell", "sunk_cell"]
        for name in names:
            path = os.path.join(base, f"{name}.png")
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    self._textures[name] = pygame.transform.smoothscale(img, (inner, inner))
                except pygame.error:
                    pass

    def update(self, dt: float):
        self._time += dt
        to_remove = []
        for key in self._explosions:
            self._explosions[key] += dt
            if self._explosions[key] > 0.8:
                to_remove.append(key)
        for key in to_remove:
            del self._explosions[key]

    def trigger_explosion(self, row: int, col: int):
        self._explosions[(row, col)] = 0.0

    def cell_rect(self, row: int, col: int) -> pygame.Rect:
        x = self._ox + col * self._cs
        y = self._oy + row * self._cs
        return pygame.Rect(x, y, self._cs, self._cs)

    def get_cell_from_mouse(self, mx: int, my: int) -> tuple[int, int] | None:
        col = (mx - self._ox) // self._cs
        row = (my - self._oy) // self._cs
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            return row, col
        return None

    def draw(self, surface: pygame.Surface, board: Board,
             show_ships: bool = True,
             hover_cell: tuple[int, int] | None = None,
             placement_ship=None,
             placement_horizontal: bool = True,
             label: str = ""):
        """Tam ızgarayı çiz"""

        total_w = self._cs * GRID_COLS
        total_h = self._cs * GRID_ROWS

        # Arkaplan
        bg_rect = pygame.Rect(self._ox - 2, self._oy - 2, total_w + 4, total_h + 4)
        pygame.draw.rect(surface, GRID_BG, bg_rect, border_radius=6)

        grid = board.grid

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = self.cell_rect(row, col)
                cell_val = grid[row][col]
                self._draw_cell(surface, rect, row, col, cell_val,
                                show_ships, hover_cell,
                                placement_ship, placement_horizontal, board)

        # Izgara çizgileri
        for i in range(GRID_ROWS + 1):
            y = self._oy + i * self._cs
            pygame.draw.line(surface, GRID_LINE, (self._ox, y), (self._ox + total_w, y))
        for j in range(GRID_COLS + 1):
            x = self._ox + j * self._cs
            pygame.draw.line(surface, GRID_LINE, (x, self._oy), (x, self._oy + total_h))

        # Koordinat etiketleri
        self._draw_labels(surface)

        # Başlık
        if label:
            self._draw_title(surface, label)

        # Patlama animasyonları
        for (r, c), elapsed in list(self._explosions.items()):
            self._draw_explosion(surface, r, c, elapsed)

    def _draw_cell(self, surface, rect, row, col, cell_val,
                   show_ships, hover_cell, placement_ship, placement_horizontal, board=None):
        padding = 2
        inner = pygame.Rect(rect.x + padding, rect.y + padding,
                            rect.w - padding * 2, rect.h - padding * 2)

        # Doku anahtarı seç (gizli SHIP hücreleri su gibi gösterilir)
        tex_key = None
        if cell_val == Board.EMPTY or (cell_val == Board.SHIP and not show_ships):
            tex_key = "water_cell"
        elif cell_val == Board.SHIP and show_ships:
            tex_key = "ship_cell"
        elif cell_val == Board.HIT:
            tex_key = "hit_cell"
        elif cell_val == Board.MISS:
            tex_key = "miss_cell"
        elif cell_val == Board.SUNK:
            tex_key = "sunk_cell"

        if tex_key and tex_key in self._textures:
            # Doku blit — üstüne renk tonu animasyonu ekle (su animasyonu için)
            surface.blit(self._textures[tex_key], inner.topleft)
            if tex_key == "water_cell":
                # Canlı dalga animasyonu: hafif şeffaf overlay
                wave = math.sin(self._time * 1.2 + row * 0.4 + col * 0.3) * 0.5 + 0.5
                pulse_alpha = int(18 * wave)
                pulse_surf = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
                pulse_surf.fill((80, 140, 200, pulse_alpha))
                surface.blit(pulse_surf, inner.topleft)
        else:
            # Fallback: programatik çizim
            wave = math.sin(self._time * 1.2 + row * 0.4 + col * 0.3) * 0.5 + 0.5
            base_blue = int(12 + wave * 6)
            cell_surf = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
            if cell_val == Board.EMPTY or (cell_val == Board.SHIP and not show_ships):
                cell_surf.fill((base_blue, base_blue + 10, base_blue + 30, 200))
            elif cell_val == Board.SHIP and show_ships:
                cell_surf.fill((*SHIP_COLOR, 230))
                highlight = pygame.Surface((inner.w, inner.h // 3), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 40))
                cell_surf.blit(highlight, (0, 0))
            elif cell_val == Board.HIT:
                cell_surf.fill((*HIT_COLOR, 220))
            elif cell_val == Board.MISS:
                cell_surf.fill((base_blue, base_blue + 8, base_blue + 25, 180))
            elif cell_val == Board.SUNK:
                cell_surf.fill((*SUNK_COLOR, 240))
            surface.blit(cell_surf, inner.topleft)

        # Dokusuz marker'lar (doku varsa da üstüne çizilir)
        if cell_val == Board.HIT and "hit_cell" not in self._textures:
            self._draw_x(surface, rect.center, HIT_COLOR)
        elif cell_val == Board.MISS and "miss_cell" not in self._textures:
            pygame.draw.circle(surface, MISS_COLOR, rect.center, self._cs // 5, 2)
        elif cell_val == Board.SUNK and "sunk_cell" not in self._textures:
            self._draw_x(surface, rect.center, (255, 255, 255), width=3)

        # Yerleştirme önizlemesi
        if placement_ship and hover_cell:
            self._draw_placement_preview(surface, row, col, hover_cell,
                                         placement_ship, placement_horizontal, board)

        # Hover efekti (düşman tahtası)
        if hover_cell == (row, col) and cell_val == Board.EMPTY and placement_ship is None:
            hover_surf = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
            hover_surf.fill((*GRID_HOVER, 80))
            surface.blit(hover_surf, inner.topleft)

    def _draw_placement_preview(self, surface, row, col, hover_cell, ship, horizontal, board=None):
        hr, hc = hover_cell
        positions = []
        for i in range(ship.size):
            if horizontal:
                positions.append((hr, hc + i))
            else:
                positions.append((hr + i, hc))

        if (row, col) not in positions:
            return

        # Geçerlilik: sınır + tahta kuralı (bitişiklik, örtüşme)
        bounds_ok = all(0 <= r < GRID_ROWS and 0 <= c < GRID_COLS for r, c in positions)
        if bounds_ok and board is not None:
            all_valid = board.is_valid_placement(hr, hc, ship.size, horizontal)
        else:
            all_valid = bounds_ok
        color = SHIP_HOVER_OK if all_valid else SHIP_HOVER_BAD

        rect = self.cell_rect(row, col)
        padding = 3
        inner = pygame.Rect(rect.x + padding, rect.y + padding,
                            rect.w - padding * 2, rect.h - padding * 2)
        preview_surf = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
        r, g, b = color
        preview_surf.fill((r, g, b, 160))
        surface.blit(preview_surf, inner.topleft)

    def _draw_x(self, surface, center, color, width=2):
        cx, cy = center
        offset = self._cs // 3
        pygame.draw.line(surface, color,
                         (cx - offset, cy - offset), (cx + offset, cy + offset), width)
        pygame.draw.line(surface, color,
                         (cx + offset, cy - offset), (cx - offset, cy + offset), width)

    def _draw_explosion(self, surface, row: int, col: int, elapsed: float):
        """Parlayan patlama efekti"""
        rect = self.cell_rect(row, col)
        progress = min(elapsed / 0.8, 1.0)
        radius = int(self._cs * 0.6 * progress)
        alpha = int(255 * (1 - progress))
        color1 = (*EXPLOSION_1, alpha)
        color2 = (*EXPLOSION_2, alpha // 2)
        expl_surf = pygame.Surface((self._cs * 2, self._cs * 2), pygame.SRCALPHA)
        cx = self._cs
        cy = self._cs
        if radius > 0:
            pygame.draw.circle(expl_surf, color2, (cx, cy), radius + 4)
            pygame.draw.circle(expl_surf, color1, (cx, cy), radius)
        surface.blit(expl_surf, (rect.centerx - self._cs, rect.centery - self._cs))

    def _draw_labels(self, surface: pygame.Surface):
        try:
            font = pygame.font.SysFont("segoeui", 13)
        except Exception:
            font = pygame.font.Font(None, 16)

        letters = "ABCDEFGHIJ"
        for i in range(GRID_COLS):
            # Sütun harfleri (üst)
            txt = font.render(letters[i], True, TEXT_SECONDARY)
            x = self._ox + i * self._cs + self._cs // 2 - txt.get_width() // 2
            surface.blit(txt, (x, self._oy - 22))
            # Satır numaraları (sol)
            txt2 = font.render(str(i + 1), True, TEXT_SECONDARY)
            y = self._oy + i * self._cs + self._cs // 2 - txt2.get_height() // 2
            surface.blit(txt2, (self._ox - 22, y))

    def _draw_title(self, surface: pygame.Surface, label: str):
        try:
            font = pygame.font.SysFont("segoeui", 18, bold=True)
        except Exception:
            font = pygame.font.Font(None, 22)
        txt = font.render(label, True, TEXT_ACCENT)
        x = self._ox + (GRID_COLS * self._cs) // 2 - txt.get_width() // 2
        surface.blit(txt, (x, self._oy - 48))
