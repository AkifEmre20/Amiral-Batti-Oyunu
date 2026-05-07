"""
create_assets.py - Tüm oyun grafik varlıklarını programatik olarak oluşturur.
Çalıştırmak için: python assets/create_assets.py
"""
import pygame
import math
import os


# ── Yardımcı ─────────────────────────────────────────────────────────────────
def _save(surf: pygame.Surface, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pygame.image.save(surf, path)
    print(f"  [OK] {os.path.relpath(path)}")


# ── Pencere İkonu (64x64) ─────────────────────────────────────────────────────
def make_icon(size: int = 64) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2

    # Arka plan çemberi
    pygame.draw.circle(s, (16, 28, 52, 255), (cx, cy), cx - 1)
    pygame.draw.circle(s, (52, 152, 219, 200), (cx, cy), cx - 1, 2)

    blue = (52, 152, 219, 255)
    light = (140, 210, 255, 255)
    tk = max(2, size // 18)  # çizgi kalınlığı

    top = cy - size * 3 // 8
    bot = cy + size * 3 // 8
    bar_y = cy - size // 10

    # Dikey mil
    pygame.draw.line(s, blue, (cx, top), (cx, bot), tk)
    # Üst halka
    ring_r = size // 9
    pygame.draw.circle(s, blue, (cx, top), ring_r, tk)
    pygame.draw.circle(s, light, (cx - 1, top - 1), max(1, ring_r // 2), 1)
    # Yatay çubuk
    pygame.draw.line(s, blue, (cx - size // 4, bar_y), (cx + size // 4, bar_y), tk)
    # Sol kol
    arm_y = cy + size // 8
    pygame.draw.line(s, blue, (cx, bot), (cx - size // 3, arm_y), tk)
    pygame.draw.circle(s, blue,  (cx - size // 3, arm_y), tk + 1)
    pygame.draw.circle(s, light, (cx - size // 3 - 1, arm_y - 1), 1)
    # Sağ kol
    pygame.draw.line(s, blue, (cx, bot), (cx + size // 3, arm_y), tk)
    pygame.draw.circle(s, blue,  (cx + size // 3, arm_y), tk + 1)
    pygame.draw.circle(s, light, (cx + size // 3 - 1, arm_y - 1), 1)
    return s


# ── Su Hücresi (boş kare) ─────────────────────────────────────────────────────
def make_water_cell(size: int) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill((10, 20, 38, 255))

    # Üstten alta renk geçişi (hafif açık → koyu)
    for y in range(size):
        t = y / size
        alpha = int(30 * (1 - t))
        line = pygame.Surface((size, 1), pygame.SRCALPHA)
        line.fill((80, 140, 200, alpha))
        s.blit(line, (0, y))

    # 2 dalga çizgisi
    for wave_y_base in [size // 3, size * 2 // 3]:
        pts = [(x, wave_y_base + int(2 * math.sin(x * 0.45)))
               for x in range(size + 1)]
        for i in range(len(pts) - 1):
            pygame.draw.line(s, (40, 90, 160, 55), pts[i], pts[i + 1], 1)

    # Üst sol köşe parlaması
    shimmer = pygame.Surface((size // 2, size // 3), pygame.SRCALPHA)
    shimmer.fill((150, 200, 255, 12))
    s.blit(shimmer, (1, 1))
    return s


# ── Gemi Hücresi ──────────────────────────────────────────────────────────────
def make_ship_cell(size: int) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)

    # Çelik mavi degrade (üstten alta açık → koyu)
    for y in range(size):
        t = y / size
        r = int(38 + (1 - t) * 24)
        g = int(98 + (1 - t) * 28)
        b = int(168 + (1 - t) * 22)
        pygame.draw.line(s, (r, g, b, 245), (0, y), (size, y))

    # Üst parlaklık şeridi
    for y in range(4):
        alpha = 90 - y * 20
        hi = pygame.Surface((size, 1), pygame.SRCALPHA)
        hi.fill((200, 230, 255, alpha))
        s.blit(hi, (0, y))

    # Sol kenar parlaması
    for x in range(3):
        alpha = 60 - x * 18
        vi = pygame.Surface((1, size), pygame.SRCALPHA)
        vi.fill((200, 230, 255, alpha))
        s.blit(vi, (x, 0))

    # İç panel çerçevesi
    mg = 4
    pygame.draw.rect(s, (65, 130, 200, 160),
                     (mg, mg, size - mg * 2, size - mg * 2), 1)

    # Rivet noktaları (köşeler)
    for rx, ry in [(7, 7), (size - 7, 7), (7, size - 7), (size - 7, size - 7)]:
        pygame.draw.circle(s, (85, 155, 215, 220), (rx, ry), 2)
        pygame.draw.circle(s, (170, 220, 255, 120), (rx - 1, ry - 1), 1)

    return s


# ── İsabet Hücresi ────────────────────────────────────────────────────────────
def make_hit_cell(size: int) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill((75, 10, 10, 255))
    cx = cy = size // 2

    # Patlama ışıkları: 8 kollu
    for i in range(8):
        angle = i * (math.pi / 4)
        x2 = cx + int(math.cos(angle) * (size // 2 - 3))
        y2 = cy + int(math.sin(angle) * (size // 2 - 3))
        pygame.draw.line(s, (255, 110, 20, 210), (cx, cy), (x2, y2), 2)

    # Ara kısa kollar (45° arayla, daha kısa)
    for i in range(8):
        angle = i * (math.pi / 4) + math.pi / 8
        x2 = cx + int(math.cos(angle) * (size // 3))
        y2 = cy + int(math.sin(angle) * (size // 3))
        pygame.draw.line(s, (255, 160, 40, 140), (cx, cy), (x2, y2), 1)

    # Dış ve iç ateş halkaları
    pygame.draw.circle(s, (255, 80, 15, 70),  (cx, cy), size // 3, 3)
    pygame.draw.circle(s, (255, 140, 30, 110), (cx, cy), size // 5, 2)

    # Merkez nokta
    pygame.draw.circle(s, (255, 220, 70, 255), (cx, cy), size // 8)
    pygame.draw.circle(s, (255, 255, 200, 200), (cx - 1, cy - 1), size // 16)

    return s


# ── Iskalama Hücresi ──────────────────────────────────────────────────────────
def make_miss_cell(size: int) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill((8, 16, 32, 255))
    cx = cy = size // 2

    # Su halkası (dalgalanma efekti)
    for i, rad in enumerate([size // 5, size // 3, size // 2 - 4]):
        alpha = 130 - i * 32
        pygame.draw.circle(s, (110, 155, 200, alpha), (cx, cy), rad, 1)

    # Merkez küçük haç
    cl = 4
    pygame.draw.line(s, (140, 175, 215, 200), (cx - cl, cy), (cx + cl, cy), 2)
    pygame.draw.line(s, (140, 175, 215, 200), (cx, cy - cl), (cx, cy + cl), 2)
    pygame.draw.circle(s, (140, 175, 215, 160), (cx, cy), 2)

    return s


# ── Batık Hücresi ─────────────────────────────────────────────────────────────
def make_sunk_cell(size: int) -> pygame.Surface:
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill((45, 5, 5, 255))
    cx = cy = size // 2
    off = size // 2 - 5

    # Kalın X
    pygame.draw.line(s, (210, 35, 35, 255),
                     (cx - off, cy - off), (cx + off, cy + off), 3)
    pygame.draw.line(s, (210, 35, 35, 255),
                     (cx + off, cy - off), (cx - off, cy + off), 3)

    # X parlaklık (ince beyaz üst katman)
    pygame.draw.line(s, (255, 100, 100, 110),
                     (cx - off + 1, cy - off), (cx + off, cy + off - 1), 1)
    pygame.draw.line(s, (255, 100, 100, 110),
                     (cx + off - 1, cy - off), (cx - off, cy + off - 1), 1)

    # Köşe hasar noktaları
    for dx, dy in [(3, 3), (size - 3, 3), (3, size - 3), (size - 3, size - 3)]:
        pygame.draw.circle(s, (190, 70, 20, 210), (dx, dy), 2)

    return s


# ── Ana ───────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    pygame.display.set_mode((1, 1))  # Save için minimal ekran

    base = os.path.dirname(os.path.abspath(__file__))
    icons_dir  = os.path.join(base, "icons")
    images_dir = os.path.join(base, "images")
    cs = 46  # CELL_SIZE ile eşleşmeli

    print("Varlıklar oluşturuluyor...")
    _save(make_icon(64),        os.path.join(icons_dir,  "icon.png"))
    _save(make_water_cell(cs),  os.path.join(images_dir, "water_cell.png"))
    _save(make_ship_cell(cs),   os.path.join(images_dir, "ship_cell.png"))
    _save(make_hit_cell(cs),    os.path.join(images_dir, "hit_cell.png"))
    _save(make_miss_cell(cs),   os.path.join(images_dir, "miss_cell.png"))
    _save(make_sunk_cell(cs),   os.path.join(images_dir, "sunk_cell.png"))
    print("Tamamlandi!")

    pygame.quit()


if __name__ == "__main__":
    main()
