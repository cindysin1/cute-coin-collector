# Cute Coin Collector

Simple Pygame coin-collection demo.

## Files
- [game.py](game.py) — main game implementation (see symbols below)
- [assets/music/bg_music.mp3](assets/music/bg_music.mp3)
- [assets/sounds/coin_sound.wav](assets/sounds/coin_sound.wav)
- [assets/sounds/win_sound.wav](assets/sounds/win_sound.wav)
- [assets/sounds/lose_sound.wav](assets/sounds/lose_sound.wav)

## Key symbols in [game.py](game.py)
- [`get_font`](game.py) — font selection helper  
- [`resource_path`](game.py) — resource path helper for packaging  
- [`Resources`](game.py) — loads images & audio assets  
- [`Player`](game.py) — player sprite and input handling  
- [`Coin`](game.py) — falling coin sprite  
- [`Game`](game.py) — main game loop and UI

## Requirements
- Python 3.7+
- pygame

Install pygame:
```sh
pip install pygame