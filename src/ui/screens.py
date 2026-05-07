"""
screens.py - Ana Menü, Oyun, Game Over ekranları
"""
import pygame
import math
from src.ui.theme import *
from src.ui.widgets import Button, Panel, AnimatedText, WaterEffect
from src.ui.renderer import GridRenderer
from src.modules.game_state import GamePhase
from src.core.board import Board


# ── Yardımcı font fonksiyonu ─────────────────────────────────────────────────
def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("segoeui", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size + 4)


def draw_text(surface, text, x, y, font, color, center=False, right=False):
    surf = font.render(text, True, color)
    if center:
        surface.blit(surf, (x - surf.get_width() // 2, y))
    elif right:
        surface.blit(surf, (x - surf.get_width(), y))
    else:
        surface.blit(surf, (x, y))
    return surf.get_width()


# ── Ana Menü Ekranı ───────────────────────────────────────────────────────────
class MainMenuScreen:

    def __init__(self, screen_w: int, screen_h: int):
        self._w = screen_w
        self._h = screen_h
        self._water = WaterEffect(screen_w, screen_h)
        self._time = 0.0
        self._name_input = "Oyuncu"
        self._input_active = False
        self._difficulty = "orta"
        self._anim_texts: list[AnimatedText] = []

        cx = screen_w // 2
        # İsim kutusu
        self._name_rect = pygame.Rect(cx - 120, 210, 240, 42)
        # Zorluk butonları
        self._btn_easy = Button(cx - 185, 295, 110, 38, "KOLAY", BTN_SUCCESS, BTN_SUCCESS_H, font_size=15)
        self._btn_med  = Button(cx - 55,  295, 110, 38, "ORTA",  BTN_PRIMARY, BTN_PRIMARY_H, font_size=15)
        self._btn_hard = Button(cx + 75,  295, 110, 38, "ZOR",   BTN_DANGER,  BTN_DANGER_H,  font_size=15)
        # Ana butonlar
        self._btn_play   = Button(cx - 120, 365, 240, 50, "OYNA",           BTN_SUCCESS, BTN_SUCCESS_H, font_size=22)
        self._btn_scores = Button(cx - 120, 432, 240, 50, "YÜKSEK SKORLAR", BTN_NEUTRAL, BTN_NEUTRAL_H, font_size=18)
        self._btn_quit   = Button(cx - 120, 499, 240, 50, "ÇIKIŞ",          BTN_DANGER,  BTN_DANGER_H,  font_size=18)

        self._result = None  # "play" / "scores" / "quit"

    @property
    def result(self):
        return self._result

    @property
    def player_name(self) -> str:
        return self._name_input.strip() or "Oyuncu"

    @property
    def difficulty(self) -> str:
        return self._difficulty

    def reset_result(self):
        self._result = None

    def handle_event(self, event: pygame.event.Event):
        # İsim alanı tıklama
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._input_active = self._name_rect.collidepoint(event.pos)

        # Klavye girişi
        if event.type == pygame.KEYDOWN and self._input_active:
            if event.key == pygame.K_BACKSPACE:
                self._name_input = self._name_input[:-1]
            elif event.key == pygame.K_RETURN:
                self._input_active = False
            elif len(self._name_input) < 16 and event.unicode.isprintable():
                self._name_input += event.unicode

        # Buton tıklamaları
        if self._btn_play.is_clicked(event):
            self._result = "play"
        if self._btn_scores.is_clicked(event):
            self._result = "scores"
        if self._btn_quit.is_clicked(event):
            self._result = "quit"
        if self._btn_easy.is_clicked(event):
            self._difficulty = "kolay"
        if self._btn_med.is_clicked(event):
            self._difficulty = "orta"
        if self._btn_hard.is_clicked(event):
            self._difficulty = "zor"

    def update(self, dt: float):
        self._time += dt
        self._water.update(dt)
        mouse = pygame.mouse.get_pos()
        for btn in [self._btn_play, self._btn_scores, self._btn_quit,
                    self._btn_easy, self._btn_med, self._btn_hard]:
            btn.update(mouse)

    def draw(self, surface: pygame.Surface):
        surface.fill(DARK_BG)
        self._water.draw(surface)

        # Başlık
        title_y = 62
        t_font = get_font(68, bold=True)
        # Gölge
        draw_text(surface, "AMİRAL BATTI", self._w // 2 + 3, title_y + 3, t_font, (0, 0, 0), center=True)
        # Ana başlık
        draw_text(surface, "AMİRAL BATTI", self._w // 2, title_y, t_font, TEXT_ACCENT, center=True)

        sub_font = get_font(18)
        pulse = 0.5 + 0.5 * math.sin(self._time * 2)
        sub_color = (
            int(TEXT_SECONDARY[0] + 40 * pulse),
            int(TEXT_SECONDARY[1] + 40 * pulse),
            int(TEXT_SECONDARY[2] + 40 * pulse),
        )
        draw_text(surface, "Denizde Üstünlük Kur!", self._w // 2, 148, sub_font, sub_color, center=True)

        label_font = get_font(14)

        # İsim girişi
        draw_text(surface, "OYUNCU ADI", self._name_rect.x, self._name_rect.y - 20, label_font, TEXT_SECONDARY)
        border_color = BTN_PRIMARY if self._input_active else GRID_LINE
        pygame.draw.rect(surface, PANEL_BG, self._name_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self._name_rect, 2, border_radius=8)
        name_font = get_font(20)
        display_name = self._name_input
        if self._input_active and int(self._time * 2) % 2 == 0:
            display_name += "|"
        draw_text(surface, display_name, self._name_rect.x + 10, self._name_rect.y + 10, name_font, TEXT_PRIMARY)

        # Zorluk seçimi
        draw_text(surface, "ZORLUK SEVİYESİ", self._btn_easy.rect.x, self._btn_easy.rect.y - 20, label_font, TEXT_SECONDARY)
        for btn, diff in [(self._btn_easy, "kolay"), (self._btn_med, "orta"), (self._btn_hard, "zor")]:
            btn.draw(surface)
            if self._difficulty == diff:
                pygame.draw.rect(surface, GOLD, btn.rect, 2, border_radius=10)

        # Butonlar
        self._btn_play.draw(surface)
        self._btn_scores.draw(surface)
        self._btn_quit.draw(surface)


# ── Oyun Ekranı ───────────────────────────────────────────────────────────────
class GameScreen:

    AI_ATTACK_DELAY = 1.2   # saniye

    def __init__(self, screen_w: int, screen_h: int, game_service):
        self._w = screen_w
        self._h = screen_h
        self._svc = game_service
        self._water = WaterEffect(screen_w, screen_h)
        self._time = 0.0
        self._anim_texts: list[AnimatedText] = []
        self._ai_timer = 0.0
        self._waiting_ai = False
        self._result = None   # "menu" / "game_over"

        # Izgara renderers
        self._left_renderer = GridRenderer(LEFT_GRID_X, LEFT_GRID_Y)
        self._right_renderer = GridRenderer(RIGHT_GRID_X, RIGHT_GRID_Y)

        # Butonlar
        self._btn_menu = Button(WINDOW_W - 160, 20, 140, 40, "< MENU",
                                BTN_NEUTRAL, BTN_NEUTRAL_H, font_size=16)
        self._btn_rotate = Button(WINDOW_W - 210, WINDOW_H - 48, 190, 36,
                                  "Döndür  [R]", BTN_PRIMARY, BTN_PRIMARY_H, font_size=16)

        # Yerleştirme sırasında aktif, sonra gizlenir
        self._hover_left: tuple[int, int] | None = None
        self._hover_right: tuple[int, int] | None = None

    @property
    def result(self):
        return self._result

    def reset_result(self):
        self._result = None

    def handle_event(self, event: pygame.event.Event):
        state = self._svc.state

        if self._btn_menu.is_clicked(event):
            self._result = "menu"
            return

        if state.phase == GamePhase.SHIP_PLACEMENT:
            if self._btn_rotate.is_clicked(event):
                self._svc.toggle_placement_orientation()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._svc.toggle_placement_orientation()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = self._left_renderer.get_cell_from_mouse(*event.pos)
                if cell:
                    success = self._svc.try_place_ship(*cell)
                    if success:
                        ship = self._svc.current_placement_ship
                        if ship:
                            self._add_anim(f"{ship.name} sırası!", LEFT_GRID_X + GRID_W // 2, LEFT_GRID_Y - 60, TEXT_ACCENT)
                        else:
                            self._add_anim("Tüm gemiler yerleştirildi! Savaş başlıyor!", self._w // 2, self._h // 2, TEXT_SUCCESS)

        elif state.phase == GamePhase.PLAYER_TURN:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = self._right_renderer.get_cell_from_mouse(*event.pos)
                if cell:
                    result = self._svc.player_attack(*cell)
                    if result:
                        self._handle_attack_result(result)

        elif state.phase == GamePhase.GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._result = "game_over"

    def update(self, dt: float):
        self._time += dt
        self._water.update(dt)
        self._left_renderer.update(dt)
        self._right_renderer.update(dt)

        mouse = pygame.mouse.get_pos()
        self._btn_menu.update(mouse)
        self._btn_rotate.update(mouse)

        state = self._svc.state
        if state.phase == GamePhase.SHIP_PLACEMENT:
            self._hover_left = self._left_renderer.get_cell_from_mouse(*mouse)
        elif state.phase == GamePhase.PLAYER_TURN:
            self._hover_right = self._right_renderer.get_cell_from_mouse(*mouse)
        else:
            self._hover_right = None

        # AI saldırı gecikmesi
        if self._waiting_ai:
            self._ai_timer += dt
            if self._ai_timer >= self.AI_ATTACK_DELAY:
                self._waiting_ai = False
                self._ai_timer = 0.0
                result = self._svc.ai_attack()
                self._handle_attack_result(result)

        # Animasyon güncelleme
        self._anim_texts = [a for a in self._anim_texts if a.is_alive]
        for a in self._anim_texts:
            a.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill(DARK_BG)
        self._water.draw(surface)

        state = self._svc.state

        # Tahtaları çiz
        self._left_renderer.draw(
            surface,
            self._svc.human.board,
            show_ships=True,
            hover_cell=self._hover_left if state.phase == GamePhase.SHIP_PLACEMENT else None,
            placement_ship=self._svc.current_placement_ship if state.phase == GamePhase.SHIP_PLACEMENT else None,
            placement_horizontal=state.placement_horizontal,
            label=f"[ {self._svc.human.name} ]"
        )

        # Kayıpda düşman gemilerini göster
        reveal_ships = (state.phase == GamePhase.GAME_OVER and
                        self._svc.state.winner != self._svc.human.name)
        self._right_renderer.draw(
            surface,
            self._svc.ai.board,
            show_ships=reveal_ships,
            hover_cell=self._hover_right,
            label="Düşman Suları"
        )

        self._draw_info_panel(surface)
        self._draw_ship_list(surface)
        self._btn_menu.draw(surface)

        if state.phase == GamePhase.SHIP_PLACEMENT:
            self._draw_placement_ui(surface)

        if state.phase == GamePhase.GAME_OVER:
            self._draw_game_over_overlay(surface)

        for anim in self._anim_texts:
            anim.draw(surface)

    def _draw_info_panel(self, surface: pygame.Surface):
        # Panel çerçevesi — eksik draw() çağrısı düzeltildi
        panel = Panel(LEFT_GRID_X, 10, RIGHT_GRID_X + GRID_W - LEFT_GRID_X, 100, alpha=210)
        panel.draw(surface)

        font_title = get_font(26, bold=True)
        draw_text(surface, "AMİRAL BATTI", self._w // 2, 18, font_title, TEXT_ACCENT, center=True)

        state = self._svc.state

        # Tur ve skor (sol)
        draw_text(surface, f"Tur: {state.round_number}", LEFT_GRID_X + 8, 66, get_font(15), TEXT_SECONDARY)
        draw_text(surface, f"Puan: {self._svc.human.score}", LEFT_GRID_X + 110, 66, get_font(15), GOLD)

        # Faz göstergesi (orta)
        phase_texts = {
            GamePhase.SHIP_PLACEMENT: ("GEMİLERİ YERLEŞTIR", TEXT_WARNING),
            GamePhase.PLAYER_TURN:   ("SENİN SIRAN  -  Ateş Et!", TEXT_SUCCESS),
            GamePhase.AI_TURN:       ("Bilgisayar düşünüyor...", TEXT_DANGER),
            GamePhase.GAME_OVER:     ("OYUN BİTTİ", TEXT_WARNING),
        }
        phase_text, phase_color = phase_texts.get(state.phase, ("", TEXT_PRIMARY))
        draw_text(surface, phase_text, self._w // 2, 66, get_font(16, bold=True), phase_color, center=True)

        # Son saldırı sonucu (sağa yaslanmış)
        last = state.last_attack
        if last:
            letters = "ABCDEFGHIJ"
            coord = f"{letters[last.col]}{last.row + 1}"
            actor = "Sen" if last.is_player_attack else "Bilgisayar"
            if last.is_sunk:
                msg = f"{actor}: {coord}  >>  {last.ship_name} BATTI!"
                color = TEXT_DANGER
            elif last.is_hit:
                msg = f"{actor}: {coord}  >>  İSABET!"
                color = HIT_COLOR
            else:
                msg = f"{actor}: {coord}  >>  ISKALADI"
                color = TEXT_SECONDARY
            # Panelin sağ kenarına yasla
            draw_text(surface, msg, RIGHT_GRID_X + GRID_W - 12, 66, get_font(14), color, right=True)

    def _draw_ship_list(self, surface: pygame.Surface):
        """Sağ kenarda gemi durum paneli"""
        sb_x = RIGHT_GRID_X + GRID_W + 10
        sb_w = WINDOW_W - sb_x - 6
        sb_y = LEFT_GRID_Y - 8
        sb_h = GRID_H + 18

        # Arkaplan paneli
        panel = Panel(sb_x, sb_y, sb_w, sb_h, alpha=190)
        panel.draw(surface)

        x = sb_x + 10
        y = sb_y + 10
        font_hdr  = get_font(14, bold=True)
        font_item = get_font(12)

        # ── Oyuncu Gemileri ──────────────────────────────────
        draw_text(surface, "GEMİLER", x, y, font_hdr, TEXT_ACCENT)
        y += 22
        for ship in self._svc.human.board.ships:
            if ship.is_sunk():
                mark, color = "X", SUNK_COLOR
            else:
                mark, color = "+", TEXT_PRIMARY
            draw_text(surface, f"[{mark}] {ship.name} ({ship.size})", x, y, font_item, color)
            y += 19

        y += 14
        # ── Düşman Gemileri ──────────────────────────────────
        draw_text(surface, "DUSMAN", x, y, font_hdr, TEXT_DANGER)
        y += 22
        # Sadece batırılan gemilerin adı gösterilir; diğerleri gizli
        sunk_count = 0
        for ship in self._svc.ai.board.ships:
            if ship.is_sunk():
                sunk_count += 1
                draw_text(surface, f"[X] {ship.name}", x, y, font_item, SUNK_COLOR)
            else:
                draw_text(surface, f"[?] Gizli ({ship.size})", x, y, font_item, TEXT_SECONDARY)
            y += 19

        y += 14
        total = len(self._svc.ai.board.ships)
        draw_text(surface, f"Batirilan: {sunk_count}/{total}", x, y, get_font(13, bold=True), TEXT_WARNING)

    def _draw_placement_ui(self, surface: pygame.Surface):
        ship = self._svc.current_placement_ship
        if not ship:
            return
        orient = "YATAY" if self._svc.state.placement_horizontal else "DİKEY"
        font = get_font(16, bold=True)
        # Alt bilgi çubuğu arka planı
        bar = pygame.Surface((self._w, 52), pygame.SRCALPHA)
        bar.fill((10, 20, 40, 200))
        surface.blit(bar, (0, WINDOW_H - 52))
        # Sol: gemi bilgisi
        draw_text(surface, f"Yerleştir: {ship.name}   Boyut: {ship.size}   Yön: {orient}",
                  LEFT_GRID_X, WINDOW_H - 36, font, TEXT_WARNING)
        # Sağ: döndür butonu
        self._btn_rotate.draw(surface)

    def _draw_game_over_overlay(self, surface: pygame.Surface):
        overlay = pygame.Surface((self._w, self._h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        winner = self._svc.state.winner
        is_player_win = winner == self._svc.human.name

        font_big = get_font(64, bold=True)
        font_med = get_font(28)
        font_sm = get_font(20)

        if is_player_win:
            draw_text(surface, "KAZANDIN!", self._w // 2, self._h // 2 - 80,
                      font_big, GOLD, center=True)
        else:
            draw_text(surface, "KAYBETTİN!", self._w // 2, self._h // 2 - 80,
                      font_big, TEXT_DANGER, center=True)
            draw_text(surface, "(Dusmanin gizli gemileri gosterildi)",
                      self._w // 2, self._h // 2 - 20, get_font(17), TEXT_SECONDARY, center=True)

        draw_text(surface, f"Puan: {self._svc.human.score}", self._w // 2, self._h // 2 + 20,
                  font_med, TEXT_PRIMARY, center=True)
        draw_text(surface, "Devam etmek icin tıkla...", self._w // 2, self._h // 2 + 70,
                  font_sm, TEXT_SECONDARY, center=True)

    def _handle_attack_result(self, result):
        from src.core.board import Board as B
        letters = "ABCDEFGHIJ"
        coord = f"{letters[result.col]}{result.row + 1}"

        if result.is_player_attack:
            renderer = self._right_renderer
            if result.is_hit:
                renderer.trigger_explosion(result.row, result.col)
                if result.is_sunk:
                    self._add_anim(f"{result.ship_name} BATTI!", RIGHT_GRID_X + GRID_W // 2,
                                   RIGHT_GRID_Y + GRID_H + 20, TEXT_DANGER)
                else:
                    self._add_anim(f"İSABET!  {coord}", RIGHT_GRID_X + GRID_W // 2,
                                   RIGHT_GRID_Y + GRID_H + 20, HIT_COLOR)
            else:
                self._add_anim(f"Iskaladın ({coord})", RIGHT_GRID_X + GRID_W // 2,
                               RIGHT_GRID_Y + GRID_H + 20, TEXT_SECONDARY)

            # AI sırasını bekle
            if self._svc.state.phase == GamePhase.AI_TURN:
                self._waiting_ai = True
                self._ai_timer = 0.0
        else:
            renderer = self._left_renderer
            if result.is_hit:
                renderer.trigger_explosion(result.row, result.col)
                if result.is_sunk:
                    self._add_anim(f"[!] {result.ship_name} BATIRILDI!", LEFT_GRID_X + GRID_W // 2,
                                   LEFT_GRID_Y + GRID_H + 20, TEXT_DANGER)
                else:
                    self._add_anim(f"[!] Bilgisayar vurdu!  {coord}", LEFT_GRID_X + GRID_W // 2,
                                   LEFT_GRID_Y + GRID_H + 20, TEXT_WARNING)
            else:
                self._add_anim(f"Bilgisayar ıskaldı ({coord})", LEFT_GRID_X + GRID_W // 2,
                               LEFT_GRID_Y + GRID_H + 20, TEXT_SECONDARY)

    def _add_anim(self, text: str, x: int, y: int, color):
        self._anim_texts.append(AnimatedText(text, x, y, color, font_size=20))


# ── Yüksek Skor Ekranı ────────────────────────────────────────────────────────
class ScoresScreen:

    def __init__(self, screen_w: int, screen_h: int, scores: list[dict]):
        self._w = screen_w
        self._h = screen_h
        self._scores = scores
        self._water = WaterEffect(screen_w, screen_h)
        cx = screen_w // 2
        self._btn_back = Button(cx - 100, screen_h - 80, 200, 45, "< GERİ",
                                BTN_NEUTRAL, BTN_NEUTRAL_H, font_size=18)
        self._result = None

    @property
    def result(self):
        return self._result

    def reset_result(self):
        self._result = None

    def handle_event(self, event):
        if self._btn_back.is_clicked(event):
            self._result = "menu"

    def update(self, dt: float):
        self._water.update(dt)
        self._btn_back.update(pygame.mouse.get_pos())

    def draw(self, surface: pygame.Surface):
        surface.fill(DARK_BG)
        self._water.draw(surface)

        font_big = get_font(48, bold=True)
        draw_text(surface, "YÜKSEK SKORLAR", self._w // 2, 60, font_big, GOLD, center=True)

        if not self._scores:
            font_md = get_font(24)
            draw_text(surface, "Henüz skor kaydı yok.", self._w // 2, self._h // 2,
                      font_md, TEXT_SECONDARY, center=True)
        else:
            font_h = get_font(18, bold=True)
            font_r = get_font(18)
            y = 150
            header = Panel(self._w // 2 - 300, y - 8, 600, 36, alpha=200)
            header.draw(surface)
            draw_text(surface, "#", self._w // 2 - 260, y, font_h, TEXT_ACCENT)
            draw_text(surface, "OYUNCU", self._w // 2 - 180, y, font_h, TEXT_ACCENT)
            draw_text(surface, "PUAN", self._w // 2 + 80, y, font_h, TEXT_ACCENT)
            draw_text(surface, "TARİH", self._w // 2 + 160, y, font_h, TEXT_ACCENT)
            y += 46
            for i, entry in enumerate(self._scores):
                row_panel = Panel(self._w // 2 - 300, y - 6, 600, 34,
                                  color=PANEL_BG if i % 2 == 0 else GRID_BG, alpha=180)
                row_panel.draw(surface)
                medal = ["1.", "2.", "3."][i] if i < 3 else f"{i + 1}."
                draw_text(surface, medal, self._w // 2 - 260, y, font_r, GOLD)
                draw_text(surface, entry["player"], self._w // 2 - 180, y, font_r, TEXT_PRIMARY)
                draw_text(surface, str(entry["score"]), self._w // 2 + 80, y, font_r, TEXT_SUCCESS)
                draw_text(surface, entry.get("date", "-"), self._w // 2 + 160, y, font_r, TEXT_SECONDARY)
                y += 38

        self._btn_back.draw(surface)
