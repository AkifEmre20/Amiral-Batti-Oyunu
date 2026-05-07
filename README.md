# Amiral Battı Oyunu

## Proje Adı
**Amiral Battı Oyunu** — Pygame tabanlı modern masaüstü oyunu

## Proje Amacı
BGT 132 Yazılım Geliştirme Teknolojileri dersi Final Projesi kapsamında geliştirilmiş,  
Nesne Yönelimli Programlama (OOP) prensipleri ile tasarlanmış, modern arayüzlü  
Amiral Battı oyunudur. Oyuncu, yapay zekaya karşı denizde üstünlük kurmaya çalışır.

## Özellikler
- Modern koyu lacivert / neon mavi UI (Pygame)
- 3 farklı AI zorluk seviyesi (Kolay / Orta / Zor)
- Patlama ve animasyon efektleri
- Skor tablosu (JSON tabanlı kalıcı kayıt)
- Gemi yerleştirme aşaması (döndürme desteği)
- Hunt & Target + Olasılık haritası AI algoritması

## Klasör Yapısı
```
AmiralbattiOyunu/
├── docs/                  # Gereksinim analizi ve UML diyagramları
├── src/
│   ├── core/              # Ship, Board, Player sınıfları
│   ├── modules/           # GameState (durum yönetimi)
│   ├── services/          # GameService, ScoreService
│   ├── ui/                # Theme, Widgets, Renderer, Screens
│   ├── utils/             # Yardımcı fonksiyonlar
│   └── data/              # Veri modelleri
├── assets/
│   ├── images/
│   ├── sounds/
│   └── icons/
├── data/                  # scores.json (otomatik oluşturulur)
├── tests/                 # Birim testleri
├── main.py                # Giriş noktası
├── requirements.txt
└── README.md
```

## Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10+
- pygame 2.x

### Kurulum
```bash
pip install -r requirements.txt
```

### Çalıştırma
```bash
python main.py
```

### Testleri Çalıştırma
```bash
python -m pytest tests/ -v
# veya
python -m unittest discover tests
```

## Oynanış
1. Ana menüden oyuncu adı ve zorluk seç → **OYNA**
2. Sol tahtaya gemilerini yerleştir (R ile döndür, sol tıkla yerleştir)
3. Sağ tahtaya tıklayarak düşman gemilerini bul ve batır
4. Tüm düşman gemilerini batıran kazanır!

## OOP Tasarımı
| Prensip | Uygulama |
|---|---|
| **Encapsulation** | `Ship`, `Board`, `Player` → private `_` alanlar + property |
| **Inheritance** | `Destroyer`, `Submarine`, `Battleship`, `Carrier` → `Ship`'ten türetildi |
| **Polymorphism** | `choose_attack()` → `HumanPlayer` ve `AIPlayer`'da farklı davranış |
| **Abstraction** | `Player` soyut sınıfı (ABC) |
