"""
score_service.py - Skor kayıt/okuma servisi
JSON dosyasına skor kaydeder ve okur
"""
import json
import os
from datetime import datetime

SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "scores.json")


class ScoreService:
    """Yüksek skor yönetimi"""

    MAX_RECORDS = 10

    def __init__(self):
        self._scores_file = os.path.abspath(SCORES_FILE)
        self._ensure_file()

    def _ensure_file(self):
        """Skor dosyası yoksa oluştur"""
        os.makedirs(os.path.dirname(self._scores_file), exist_ok=True)
        if not os.path.exists(self._scores_file):
            self._write([])

    def save_score(self, player_name: str, score: int):
        """Yeni skoru kaydet"""
        scores = self._read()
        entry = {
            "player": player_name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        scores.append(entry)
        # Skora göre büyükten küçüğe sırala ve en fazla MAX_RECORDS tut
        scores.sort(key=lambda x: x["score"], reverse=True)
        self._write(scores[:self.MAX_RECORDS])

    def get_top_scores(self) -> list[dict]:
        """En yüksek skorları döndür"""
        return self._read()

    def _read(self) -> list[dict]:
        try:
            with open(self._scores_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, data: list[dict]):
        with open(self._scores_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
