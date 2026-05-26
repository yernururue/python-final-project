# Game Analytics Analyzer

Final project for the **Introduction to Programming 2** course (Case 8).

A command-line tool that loads game performance data from a JSON file, classifies players into tiers, and produces a leaderboard, daily best performances, and a list of pro players eligible for tournaments.

---

## Features

- **Leaderboard** — ranks all players by total score, showing average score and tier
- **Daily best performance** — finds the highest-scoring player for each date
- **Pro player roster** — lists players eligible for tournaments using a generator
- **Date validation** — validates dates with a regex before displaying records

---

## Project Structure

```
python-final-project/
├── main.py                 # Entry point
├── data.json               # Input data file
├── models/
│   └── player.py           # Stat, Player, ProPlayer, BeginnerPlayer classes
├── services/
│   ├── analyzer.py         # Analyzer class — core logic
│   ├── data_loader.py      
│   └── load_game_data.py   # JSON loader
└── tests/
    └── test.py             # Unit tests
```

---

## Player Tiers

Players are classified once, based on their **first recorded score**:

| Tier | Condition |
|---|---|
| Pro Player | first score >= 150 |
| Standard | first score 101–149 |
| Beginner Player | first score <= 100 |

---

## Data Format

The input file `data.json` must be a JSON array of objects with these fields:

```json
[
  {"player": "Alice", "score": 120, "date": "2026-01-01"},
  {"player": "Bob",   "score": 150, "date": "2026-01-01"},
  {"player": "Alice", "score": 180, "date": "2026-01-02"}
]
```

| Field | Type | Description |
|---|---|---|
| `player` | string | Player name |
| `score` | integer | Score for this session |
| `date` | string | Date in `YYYY-MM-DD` format |

---

## How to Run

```bash
python3 main.py
```

Example output:

```
Game analyzer v1.0

 -- Leaderboard --
1. Alice | Total: 300 | Average score: 150.0 | Tier: Standard
2. Bob | Total: 150 | Average score: 150.0 | Tier: Pro Player

 -- Daily Best performances --
2026-01-01: Bob scored 150 points
2026-01-02: Alice scored 180 points

 -- Pro players for tournaments --
Bob is a pro
```

---

## How to Run Tests

```bash
python3 -m unittest tests/test.py -v
```

35 tests covering:

- `valid_date()` — regex date validation
- `Stat` — date and score getters
- `Player` — total score, average score, empty stats, tier label
- `ProPlayer` / `BeginnerPlayer` — tier labels and stat inheritance
- `Analyzer.process_data()` — tier classification, multiple entries
- `Analyzer.get_leaderboard()` — sort order and correctness
- `Analyzer.get_best_daily_performance()` — daily winner selection
- `Analyzer.get_pro_players()` — generator type and filtering

---

## Requirements

- Python 3.6+
- No external dependencies
