# TRON: Light Cycles

Un joc clasic TRON recreat in Pygame cu AI si powerup-uri.

## Cerinte

- Python 3.x
- Pygame

```bash
pip install pygame
```

## Rulare

```bash
python main.py
```

## Comenzi

**Player 1:**
- W/A/S/D - Miscare
- Left Shift - Turbo

**Player 2 (PvP):**
- Arrow Keys - Miscare
- Right Shift - Turbo

## Features

- **Singleplayer** - Joaca impotriva AI
- **Multiplayer** - PvP local (2 jucatori)
- **Sistem Turbo** - Viteza dubla cu bare de energie
- **Powerup-uri:**
  - 🟡 Eraser - Sterge toate trail-urile
  - 🔵 Ghost - Invincibilitate temporara
  - 🟢 Freeze - Ingheata adversarul
- **Audio** - Muzica si efecte sonore

## Structura

- `main.py` - Entry point
- `game.py` - Loop principal si logica jocului
- `player.py` - Clasa LightCycle
- `ai_player.py` - AI
- `powerup.py` - Powerup
- `ui.py` - Butoane de meniu
- `audio.py` - Manager sunet/muzica
- `settings.py` - Constante si configurari
