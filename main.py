# Secure Authentication Toolkit

A Python command-line toolkit built for **Python for Cybersecurity**, demonstrating
password security and authentication-attack detection concepts.

## Features / Modules

All modules are accessible from a single themed home menu (`main.py`):

| # | Module | Description |
|---|--------|-------------|
| 1 | Password Strength Checker | Scores a user-entered password on length, character variety, and known-common-password checks. |
| 2 | Login Lockout Simulator | Validates a fixed demo account and locks it after 3 failed attempts. |
| 3 | Secure Password Generator | Generates a random password to user-chosen length and character-set criteria. |
| 4 | Brute Force Attack Detection | Scans simulated login logs and flags IP addresses with 3+ failed attempts. |
| 5 | Password Guessing Detection | Scans simulated login logs and flags usernames targeted with 3+ distinct guessed passwords. |

## Project Structure

```
auth_toolkit/
├── main.py                       # Home menu / navigation hub
├── README.md
└── modules/
    ├── __init__.py
    ├── theme.py                       # Shared CLI theme (colors, banners, boxes)
    ├── password_strength.py           # Module 1
    ├── login_lockout.py               # Module 2
    ├── password_generator.py          # Module 3
    ├── brute_force_detection.py       # Module 4
    ├── password_guessing_detection.py # Module 5
    └── sample_data.py                 # Shared simulated login log data (Modules 4 & 5)
```

## Requirements

- Python 3.8+
- No third-party packages required (standard library only)
- A terminal that supports ANSI color codes (most modern terminals, including
  Windows Terminal / VS Code / macOS Terminal / Linux). If your terminal does
  not render colors correctly, set `USE_COLOR = False` in `modules/theme.py`.

## How to Run

```bash
cd auth_toolkit
python3 main.py
```

You'll see a home screen with a numbered menu (1–5) to jump into any module,
plus `0` to exit. After each module finishes, you're returned to the home menu.

## Demo Credentials (Module 2)

```
Username: admin
Password: Secure@123
```

## Notes on Detection Logic

- **Module 4 (Brute Force):** groups login attempts by **IP address** and
  flags any IP with `failed_count >= 3`. This models an attacker hammering
  a login endpoint from one source, regardless of which account they target.
- **Module 5 (Password Guessing):** groups login attempts by **username** and
  flags any account where `3+ distinct passwords` were attempted and failed.
  This models an attacker (possibly from multiple IPs) guessing passwords
  against one specific, high-value account.
- Sample log data lives in `modules/sample_data.py` — replace it with real
  log data (or wire up file/CSV input) to analyze actual authentication logs.

## Possible Future Improvements

- Persist lockouts and login attempts to a file/database instead of in-memory.
- Add time-window based detection (e.g., 5 failures within 60 seconds).
- Support importing real log files (CSV/JSON) for Modules 4 & 5.
- Add password strength checking via entropy calculation (zxcvbn-style).
- Hash and salt stored passwords in the lockout simulator using `hashlib`/`bcrypt`.
