# Zyra Wallet Checker GUI

A simple offline tool to check the activity status and balance score of EVM-compatible wallet addresses.

## Features
- Simulated balance scoring
- GUI interface (Tkinter-based)
- Result export (.txt)
- Offline tool, no network activity

## Files
- `zyra_checker.py` — GUI launcher
- `zyra_core.py` — internal scanner engine
- `scanner.data` — required data module

## Requirements
- Python 3.9+
- `tkinter` (included in standard library)

## Run
```bash
pip install -r requirements.txt
python zyra_checker.py
```
