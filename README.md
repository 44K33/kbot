# OSRS Woodcutting Bot

A woodcutting bot for Old School RuneScape. For a School project.

## Setup
pip install -r requirements.txt

Run the game in windowed mode, then start main.py.

## Structure
```
osrs-bot/
├── main.py            # Entry point
├── vision.py          # Screen capture & tree detection
├── fsm.py             # State machine
├── randomizer.py      # Human-like delays & click variation
├── input_handler.py   # Mouse control
└── templates/         # Reference images
```

## Disclaimer
For educational purposes only.