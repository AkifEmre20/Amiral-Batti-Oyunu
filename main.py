"""
main.py - Amiral Battı Oyunu - Ana Giriş Noktası
BGT 132 Final Projesi
"""
import sys
import os

# Proje kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from src.ui.theme import WINDOW_W, WINDOW_H, FPS, DARK_BG
from src.ui.screens import MainMenuScreen, GameScreen, ScoresScreen
from src.services.game_service import GameService
from src.core.player import AIPlayer


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Amiral Battı Oyunu")

    # İkon yükleme (varsa)
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "icon.png")
    if os.path.exists(icon_path):
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except pygame.error:
            pass

    clock = pygame.time.Clock()

    # Başlangıç ekranı
    current_screen = "menu"
    menu_screen = MainMenuScreen(WINDOW_W, WINDOW_H)
    game_screen: GameScreen | None = None
    scores_screen: ScoresScreen | None = None
    game_service: GameService | None = None

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time (saniye)

        # ── Event işleme ─────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if current_screen == "game":
                    current_screen = "menu"
                    menu_screen.reset_result()
                    continue

            if current_screen == "menu":
                menu_screen.handle_event(event)
            elif current_screen == "game" and game_screen:
                game_screen.handle_event(event)
            elif current_screen == "scores" and scores_screen:
                scores_screen.handle_event(event)

        if not running:
            break

        # ── Ekran geçişleri ───────────────────────────────────────────────────
        if current_screen == "menu":
            result = menu_screen.result
            if result == "play":
                menu_screen.reset_result()
                game_service = GameService(
                    player_name=menu_screen.player_name,
                    ai_difficulty=menu_screen.difficulty
                )
                game_service.start_placement_phase()
                game_screen = GameScreen(WINDOW_W, WINDOW_H, game_service)
                current_screen = "game"

            elif result == "scores":
                menu_screen.reset_result()
                # Geçici servis ile skor oku
                temp_svc = GameService()
                scores_screen = ScoresScreen(WINDOW_W, WINDOW_H, temp_svc.get_scores())
                current_screen = "scores"

            elif result == "quit":
                running = False

        elif current_screen == "game" and game_screen:
            result = game_screen.result
            if result == "menu":
                game_screen.reset_result()
                menu_screen = MainMenuScreen(WINDOW_W, WINDOW_H)
                current_screen = "menu"
            elif result == "game_over":
                game_screen.reset_result()
                # Yeni oyun kurulumu için menüye dön
                menu_screen = MainMenuScreen(WINDOW_W, WINDOW_H)
                current_screen = "menu"

        elif current_screen == "scores" and scores_screen:
            result = scores_screen.result
            if result == "menu":
                scores_screen.reset_result()
                current_screen = "menu"

        # ── Güncelle ve Çiz ───────────────────────────────────────────────────
        if current_screen == "menu":
            menu_screen.update(dt)
            menu_screen.draw(screen)
        elif current_screen == "game" and game_screen:
            game_screen.update(dt)
            game_screen.draw(screen)
        elif current_screen == "scores" and scores_screen:
            scores_screen.update(dt)
            scores_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
