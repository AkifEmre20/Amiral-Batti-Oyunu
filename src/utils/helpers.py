"""
helpers.py - Yardımcı fonksiyonlar
"""
import pygame
import os
from src.ui.theme import WINDOW_W, WINDOW_H


def clamp(value: int | float, min_val: int | float, max_val: int | float):
    """Değeri [min, max] aralığında tut"""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Lineer interpolasyon"""
    return a + (b - a) * clamp(t, 0.0, 1.0)


def load_image_safe(path: str, size: tuple[int, int] | None = None) -> pygame.Surface | None:
    """
    Resmi yükler. Bulunamazsa None döndürür.
    """
    if not os.path.exists(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except pygame.error:
        return None


def load_sound_safe(path: str) -> pygame.mixer.Sound | None:
    """
    Ses dosyasını yükler. Bulunamazsa None döndürür.
    """
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None


def center_rect(w: int, h: int) -> pygame.Rect:
    """Pencere ortasında belirtilen boyutta dikdörtgen"""
    x = (WINDOW_W - w) // 2
    y = (WINDOW_H - h) // 2
    return pygame.Rect(x, y, w, h)
