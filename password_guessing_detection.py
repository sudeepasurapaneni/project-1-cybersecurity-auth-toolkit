"""
Module 2 - Login Lockout Simulator
------------------------------------
Simulates a login system with a predefined username/password.
Locks the account after 3 failed attempts and prevents further tries.
"""

from modules.theme import Color, c, print_section_header, alert_box, success_box, pause

# Predefined credentials for the simulation
VALID_USERNAME = "admin"
VALID_PASSWORD = "Secure@123"

MAX_ATTEMPTS = 3


def run():
    print_section_header(
        "MODULE 2: LOGIN LOCKOUT SIMULATOR",
        f"Demo account -> username: '{VALID_USERNAME}'  (max {MAX_ATTEMPTS} attempts)"
    )

    attempts_used = 0
    locked = False

    while attempts_used < MAX_ATTEMPTS:
        remaining = MAX_ATTEMPTS - attempts_used
        print(c(f"\nAttempt {attempts_used + 1} of {MAX_ATTEMPTS}", Color.CYAN))
        username = input(c("  Username: ", Color.WHITE))
        password = input(c("  Password: ", Color.WHITE))

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            print()
            success_box([
                f"Login successful. Welcome, {username}!",
                "Session started with full privileges."
            ])
            pause()
            return

        attempts_used += 1
        remaining = MAX_ATTEMPTS - attempts_used

        if remaining > 0:
            print(c(f"  [X] Invalid username or password.", Color.RED))
            print(c(f"  Remaining attempts: {remaining}", Color.YELLOW + Color.BOLD))
        else:
            locked = True

    if locked:
        print()
        alert_box([
            "ACCOUNT LOCKED",
            f"Too many failed login attempts ({MAX_ATTEMPTS}/{MAX_ATTEMPTS}).",
            "This account has been temporarily locked for security reasons.",
            "Please contact an administrator or wait before retrying.",
        ], level="HIGH")
        print()
        print(c("  Further login attempts are blocked for this session.", Color.RED))

    pause()


if __name__ == "__main__":
    run()
