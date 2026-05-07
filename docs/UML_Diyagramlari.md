# UML Diyagramları — Amiral Battı Oyunu

## Class Diagram (Sınıf Diyagramı)

```
┌─────────────────────────────┐
│         <<abstract>>        │
│           Ship              │
├─────────────────────────────┤
│ - _name: str                │
│ - _size: int                │
│ - _symbol: str              │
│ - _positions: list          │
│ - _hits: set                │
│ - _is_horizontal: bool      │
├─────────────────────────────┤
│ + place(positions)          │
│ + receive_hit(row,col):bool │
│ + is_sunk(): bool           │
└─────────┬───────────────────┘
          │  Inheritance (Kalıtım)
    ┌─────┼──────────────────────────────────┐
    │     │                │                 │
┌───▼──┐ ┌▼───────┐ ┌─────▼────┐ ┌─────────▼──┐
│ Des- │ │Subma-  │ │Battle-   │ │  Carrier   │
│troyer│ │rine    │ │ship      │ │            │
│ (2)  │ │ (3)    │ │  (4)     │ │   (5)      │
└──────┘ └────────┘ └──────────┘ └────────────┘

┌─────────────────────────────┐
│           Board             │
├─────────────────────────────┤
│ - _owner: str               │
│ - _grid: list[list[int]]    │
│ - _ships: list[Ship]        │
├─────────────────────────────┤
│ + place_ship(): bool        │
│ + receive_attack(): int     │
│ + all_ships_sunk(): bool    │
│ + is_valid_placement(): bool│
└─────────────────────────────┘

┌─────────────────────────────┐      ┌─────────────────────┐
│       <<abstract>>          │      │      GameState       │
│          Player             │      ├─────────────────────┤
├─────────────────────────────┤      │ + phase: GamePhase  │
│ - _name: str                │      │ + round_number: int │
│ - _board: Board             │      │ + attack_log: list  │
│ - _attack_history: set      │      │ + winner: str|None  │
├─────────────────────────────┤      └─────────────────────┘
│ + choose_attack(): tuple    │ <<Polymorphism>>
└──────────┬──────────────────┘
           │
     ┌─────┴──────────┐
     │                │
┌────▼────┐    ┌──────▼──────┐
│ Human   │    │  AIPlayer   │
│ Player  │    │             │
│         │    │ +difficulty │
│         │    │ +hunt_target│
└─────────┘    └─────────────┘

┌─────────────────────────────┐
│        GameService          │
├─────────────────────────────┤
│ - _human: HumanPlayer       │
│ - _ai: AIPlayer             │
│ - _state: GameState         │
│ - _score_service: ScoreSvc  │
├─────────────────────────────┤
│ + player_attack(): Result   │
│ + ai_attack(): Result       │
│ + try_place_ship(): bool    │
│ + reset()                   │
└─────────────────────────────┘
```

## Use Case Diagram (Kullanım Senaryosu)

```
         ┌──────────────────────────────────┐
         │         Amiral Battı Oyunu        │
         │                                  │
         │  ○ Oyuncu Adı Gir                │
         │  ○ Zorluk Seç                    │
  [Oyun- │  ○ Gemileri Yerleştir            │
   cu]───┤  ○ Saldırı Yap                  │
         │  ○ Skoru Görüntüle               │
         │                                  │
         │  ○ Otomatik Saldırı ──── [AI]   │
         └──────────────────────────────────┘
```
