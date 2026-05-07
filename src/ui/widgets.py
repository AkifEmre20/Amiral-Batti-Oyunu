"""
widgets.py - Tekrar kullanılabilir UI bileşenleri (Button, Label, AnimatedText)
"""
import pygame
import math
from src.ui.theme import *


class Button:
    """Modern köşe-yuvarlak buton bileşeni"""

    def __init__(self, x: int, y: int, w: int, h: int,
                 text: str,
                 color=BTN_PRIMARY, hover_color=BTN_PRIMARY_H,
                 text_color=TEXT_PRIMARY,
                 font_size: int = 20,
                 radius: int = 10):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.radius = radius
        self._font = None
        self._font_size = font_size
        self._hovered = False
        self._scale = 1.0
        self._target_scale = 1.0
        self.enabled = True

    def _get_font(self) -> pygame.font.Font:
        if self._font is None:
            try:
                self._font = pygame.font.SysFont("segoeui", self._font_size, bold=True)
            except Exception:
                self._font = pygame.font.Font(None, self._font_size + 4)
        return self._font

    def update(self, mouse_pos: tuple[int, int]):
        if not self.enabled:
            self._hovered = False
            return
        self._hovered = self.rect.collidepoint(mouse_pos)
        self._target_scale = 1.04 if self._hovered else 1.0
        # Smooth scale
        self._scale += (self._target_scale - self._scale) * 0.25

    def is_clicked(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self._hovered else self.color
        if not self.enabled:
            color = BTN_NEUTRAL

        # Scale effect
        sw = int(self.rect.w * self._scale)
        sh = int(self.rect.h * self._scale)
        sx = self.rect.centerx - sw // 2
        sy = self.rect.centery - sh // 2
        scaled_rect = pygame.Rect(sx, sy, sw, sh)

        # Gölge
        shadow_rect = scaled_rect.move(0, 3)
        shadow_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 80), shadow_surf.get_rect(), border_radius=self.radius)
        surface.blit(shadow_surf, shadow_rect.topleft)

        # Buton arkaplanı
        pygame.draw.rect(surface, color, scaled_rect, border_radius=self.radius)

        # Üst kenar parlaması
        highlight_rect = pygame.Rect(scaled_rect.x + 2, scaled_rect.y + 2, scaled_rect.w - 4, 2)
        highlight_surf = pygame.Surface((highlight_rect.w, 2), pygame.SRCALPHA)
        highlight_surf.fill((255, 255, 255, 40))
        surface.blit(highlight_surf, highlight_rect.topleft)

        # Metin
        font = self._get_font()
        text_surf = font.render(self.text, True, self.text_color if self.enabled else TEXT_SECONDARY)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        surface.blit(text_surf, text_rect)


class Panel:
    """Yarı saydam panel bileşeni"""

    def __init__(self, x: int, y: int, w: int, h: int,
                 color=PANEL_BG, alpha: int = 230, radius: int = 12):
        self.rect = pygame.Rect(x, y, w, h)
        self._color = color
        self._alpha = alpha
        self._radius = radius

    def draw(self, surface: pygame.Surface):
        surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        r, g, b = self._color
        pygame.draw.rect(surf, (r, g, b, self._alpha),
                         surf.get_rect(), border_radius=self._radius)
        # İnce kenarlık
        pygame.draw.rect(surf, (*GRID_LINE, 180),
                         surf.get_rect(), width=1, border_radius=self._radius)
        surface.blit(surf, self.rect.topleft)


class AnimatedText:
    """Yukarı kayarak kaybolan animasyonlu metin"""

    def __init__(self, text: str, x: int, y: int, color=TEXT_PRIMARY,
                 font_size: int = 22, duration: float = 2.0):
        self.text = text
        self.x = x
        self.y = float(y)
        self.color = color
        self.font_size = font_size
        self.duration = duration
        self._elapsed = 0.0
        self._alive = True
        try:
            self._font = pygame.font.SysFont("segoeui", font_size, bold=True)
        except Exception:
            self._font = pygame.font.Font(None, font_size + 4)

    @property
    def is_alive(self) -> bool:
        return self._alive

    def update(self, dt: float):
        self._elapsed += dt
        self.y -= 40 * dt
        if self._elapsed >= self.duration:
            self._alive = False

    def draw(self, surface: pygame.Surface):
        if not self._alive:
            return
        alpha = max(0, int(255 * (1 - self._elapsed / self.duration)))
        text_surf = self._font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        rect = text_surf.get_rect(center=(self.x, int(self.y)))
        surface.blit(text_surf, rect)


class WaterEffect:
    """Arkaplan dalgalanma efekti"""

    def __init__(self, w: int, h: int):
        self._w = w
        self._h = h
        self._time = 0.0

    def update(self, dt: float):
        self._time += dt

    def draw(self, surface: pygame.Surface):
        # Hafif dalga çizgileri
        for i in range(0, self._h, 40):
            offset = int(4 * math.sin(self._time * 0.8 + i * 0.05))
            alpha = 15 + int(5 * math.sin(self._time + i * 0.1))
            line_surf = pygame.Surface((self._w, 1), pygame.SRCALPHA)
            line_surf.fill((52, 152, 219, max(0, min(255, alpha))))
            surface.blit(line_surf, (0, i + offset))
