# Scooter Management CLI

A small Python-based command-line application for managing scooters, travellers, users, logs and backups. The project separates concerns across `Access`, `Logic`, `Models`, `Presentation` and `Utils`.

## Features
- Manage users and accounts
- Manage scooters and travellers
- Encrypted logs and backups
- Simple CLI presentation layer

## Repository Structure

- Access/: data access layer (e.g. `DataAccess.py`, `LogAccess.py`)
- Logic/: business logic for accounts, scooters, travellers, backups and logs
- Models/: data models used across the app
- Presentation/: CLI entry points and interactive menus (e.g. `login.py`, `menus.py`)
- Utils/: utilities (encryption, etc.)
- Logs/: encrypted log file (`logs.enc`)
- System Backups/: backup storage
- databasechange.py, um_members.py: helper scripts

Example important files:

- [Access/DataAccess.py](Access/DataAccess.py) — persistence helpers
- [Utils/encryption.py](Utils/encryption.py) — encryption utilities used for logs/backups
- [Presentation/login.py](Presentation/login.py) — CLI login entrypoint

## Requirements
- Python 3.8+
- No pinned requirements file is included; the project uses only Python standard libraries and small helpers. If you add dependencies, include a `requirements.txt`.

## Quick setup (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Run the application (CLI entry):

```powershell
python Presentation\login.py
```


## Data & Backups
- Logs are stored encrypted in `Logs/logs.enc` and are handled via `Access/LogAccess.py` and `Logic/logs_logic.py`.
- Backups are placed in the `System Backups/` folder; see `Logic/backup_logic.py` and `Presentation/backup_presentation.py` for usage flows.

## Development notes
- Presentation scripts implement the user-facing flows; the `Logic/` layer contains testable, side-effect-free logic where possible.
- If you change persistence, update `Access/DataAccess.py` to keep a single data access point.

## Contributing
- Open an issue or submit a pull request. Keep changes small and focused.

## License
- No license file is included. Add `LICENSE` if you wish to clarify reuse terms.

---

If you'd like, I can:

- add a `requirements.txt` by scanning imports,
- expand the README with step-by-step flows for the main features, or
- add a short developer README describing how to run and test specific logic modules.

Please tell me which of those you'd like next.
