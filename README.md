## Features
- **Interactive REPL**: Command-line interface with commands like `look`, `move <room>`, `inspect <item>`, `use <item>`, `inventory`, `hint`, `save`, `load`, and `quit`.
- **Room-Based Puzzles**: 5 rooms + intro lobby and final gate, each producing a token via data analysis.
- **Transcript Logging**: All interactions logged to `run.txt` for review.
- **Save/Load State**: Progress persists in JSON format.
- **Modular Architecture**: Clean separation of engine, rooms, and utilities for easy extension.

## Team
- **Supervisor**: [Your Name] - Project oversight, architecture design, integration, and demo preparation.
- **Apprentice Developer 1**: [Name 1] - Implementation of Rooms 2 (SOC) and 3 (DNS), including log parsing and base64 decoding.
- **Apprentice Developer 2**: [Name 2] - Implementation of Rooms 4 (Vault) and 5 (Malware), including regex matching and graph traversal (DFS/BFS).

Contributions were divided to align with skill-building: apprentices focused on puzzle logic, while the supervisor handled the REPL engine and final integration.

## Installation
1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd escape-room
   ```
2. Ensure Python 3.8+ is installed (no external dependencies beyond standard library; base64, re, json are built-in).
3. Place provided data files in `data/` (e.g., `auth.log`, `dns.cfg`, `vault_dump.txt`, `proc_tree.jsonl`, `final_gate.txt`). These are group-seeded—do not hardcode solutions.
4. (Optional) Install development tools:
   ```
   pip install pytest black flake8
   ```

## Usage
Run the game from the project root:
```
python escape.py --start intro --transcript run.txt
```

This starts the interactive REPL in the Intro Lobby. Example session:
```
[Game] Cyber Escape Room started. Type 'help' for commands.
> look
You are in the Intro Lobby.
A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final.
> move soc
You enter the SOC Triage Desk.
A cluttered screen shows failed SSH login attempts.
Items here: auth.log
> inspect auth.log
[Room SOC] Parsing logs...
TOKEN[KEYPAD]=4217
EVIDENCE[KEYPAD].TOP24=203.0.113.0/24
... (full evidence)
> inventory
You currently hold: KEYPAD
> quit
[Game] Goodbye. Transcript written to run.txt
```

- **Navigation**: `move <room>` (e.g., `move dns`).
- **Puzzles**: `inspect <item>` triggers room-specific logic (e.g., parsing files).
- **Progress**: `use gate` at the final room checks collected tokens.
- **Save/Load**: `save <file.json>` / `load <file.json>` for state persistence.
- **Transcript**: Always logs to specified file for grading.

For automated testing, run:
```
pytest tests/
```

## Project Structure
```
escape-room/
├── README.md                  # This file
├── escape.py                  # CLI entry point (REPL launcher)
├── escaperoom/
│   ├── __init__.py
│   ├── engine.py              # Game loop, command routing, GameState
│   ├── transcript.py          # Logger for run.txt
│   ├── utils.py               # Helpers (e.g., IP parsing, config loader)
│   └── rooms/
│       ├── __init__.py
│       ├── base.py            # Abstract Room base class
│       ├── soc.py             # Room 2: SOC Triage Desk (auth.log parsing)
│       ├── dns.py             # Room 3: DNS Closet (dns.cfg decoding)
│       ├── vault.py           # Room 4: Vault Corridor (regex on vault_dump.txt)
│       └── malware.py         # Room 5: Malware Lab (graph on proc_tree.jsonl)
├── data/                      # Input files (group-specific; gitignored)
│   ├── auth.log
│   ├── dns.cfg
│   ├── vault_dump.txt
│   ├── proc_tree.jsonl
│   └── final_gate.txt
├── tests/                     # Unit/integration tests (optional but recommended)
└── .gitignore                 # Ignores data/, pycache, etc.
```

## Skills Practiced
- **File I/O & Parsing**: Line-by-line log reading, JSONL graphs, config files.
- **Data Structures**: Dicts for grouping, sets for visited nodes, regex for patterns.
- **Algorithms**: Subnet aggregation, base64 decoding, DFS/BFS traversal, checksum validation.
- **Best Practices**: Type hints, docstrings, exception handling (e.g., skip malformed lines with warnings), modular functions.

## Common Pitfalls & Tips
- **Data Sensitivity**: Solutions are per-group; always parse dynamically—never hardcode tokens.
- **Error Handling**: Log warnings for skips (e.g., malformed JSON) but don't crash the REPL.
- **Testing**: Break puzzles into small functions (e.g., `parse_ssh_line(line)`) and test independently.
- **Performance**: For graphs, use iterative BFS to avoid recursion depth issues.
- **PEP8 Compliance**: Run `black .` and `flake8` before committing.

## Deliverables & Grading
Submit the full repo with a generated `run.txt` from a complete playthrough. Expected outputs include all `TOKEN[...]` lines and `FINAL_GATE=PENDING` with `MSG` and `EXPECTED_HMAC`.

Grading (as per assignment):
- Correctness: 40% (all tokens collected, gate unlocks).
- Design & Decomposition: 25% (modular classes/functions).
- Demo & Defense: 25% (live run + Q&A).
- Code and documentation quality (10%): naming, docstrings, README, error handling, PEP 8 cleanliness.

For questions, contact the supervisor.

## License
MIT License—feel free to fork and extend for educational use.

