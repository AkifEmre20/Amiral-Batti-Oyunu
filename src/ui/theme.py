"""
theme.py - Renk paleti, font ve stil sabitleri
"""

# ── Renk Paleti ──────────────────────────────────────────────────────────────
DARK_BG        = (10,  18,  35)   # Koyu lacivert arkaplan
PANEL_BG       = (16,  28,  52)   # Panel arka planı
GRID_BG        = (12,  22,  42)   # Izgara arka planı
GRID_LINE      = (30,  55,  90)   # Izgara çizgileri
GRID_HOVER     = (40,  80, 140)   # Hover hücresi
GRID_HOVER_INVALID = (140, 40, 40)

# Gemi renkleri
SHIP_COLOR     = (52,  152, 219)  # Mavi
SHIP_SHADOW    = (30,  100, 170)
SHIP_HOVER_OK  = (46,  204, 113)  # Yeşil (geçerli yerleşim)
SHIP_HOVER_BAD = (231, 76,  60)   # Kırmızı (geçersiz)

# Saldırı sonucu renkleri
HIT_COLOR      = (231, 76,  60)   # Kırmızı - isabet
MISS_COLOR     = (149, 165, 166)  # Gri - ıskala
SUNK_COLOR     = (255, 50,  50)   # Parlak kırmızı - batık
SUNK_OVERLAY   = (180, 30,  30, 180)

# Metin renkleri
TEXT_PRIMARY   = (236, 240, 241)  # Neredeyse beyaz
TEXT_SECONDARY = (127, 140, 141)  # Gri
TEXT_ACCENT    = (52,  152, 219)  # Mavi vurgu
TEXT_WARNING   = (241, 196, 15)   # Sarı
TEXT_SUCCESS   = (46,  204, 113)  # Yeşil
TEXT_DANGER    = (231, 76,  60)   # Kırmızı

# Buton renkleri
BTN_PRIMARY    = (41,  128, 185)
BTN_PRIMARY_H  = (52,  152, 219)
BTN_DANGER     = (192, 57,  43)
BTN_DANGER_H   = (231, 76,  60)
BTN_SUCCESS    = (39,  174, 96)
BTN_SUCCESS_H  = (46,  204, 113)
BTN_NEUTRAL    = (44,  62,  80)
BTN_NEUTRAL_H  = (52,  73,  94)

# Özel efekt renkleri
EXPLOSION_1    = (255, 165,  0)   # Turuncu
EXPLOSION_2    = (255, 69,   0)   # Ateş kırmızısı
WATER_1        = (52,  152, 219)
WATER_2        = (41,  128, 185)
GOLD           = (241, 196,  15)
SILVER         = (189, 195, 199)

# ── Boyutlar ─────────────────────────────────────────────────────────────────
WINDOW_W       = 1280
WINDOW_H       = 760
CELL_SIZE      = 46
GRID_COLS      = 10
GRID_ROWS      = 10
GRID_W         = CELL_SIZE * GRID_COLS
GRID_H         = CELL_SIZE * GRID_ROWS

# Sol tahta pozisyonu (oyuncu)
LEFT_GRID_X    = 60
LEFT_GRID_Y    = 165

# Sağ tahta pozisyonu (düşman)
RIGHT_GRID_X   = 630
RIGHT_GRID_Y   = 165

# FPS
FPS            = 60
