#!/usr/bin/env python3
"""
main.py
-------
Secure Authentication Toolkit - Home Menu

This is the entry point for the toolkit. It presents a themed home
screen and lets the user navigate to any of the five modules:

  1. Password Strength Checker
  2. Login Lockout Simulator
  3. Secure Password Generator
  4. Brute Force Attack Detection
  5. Password Guessing Detection

Run with:  python3 main.py
"""

from modules.theme import (
    Color, c, print_home_banner, menu_option, pause, clear_screen
)
from modules import (
    password_strength,
    login_lockout,
    password_generator,
    brute_force_detection,
    password_guessing_detection,
)


MENU_ITEMS = {
    "1": ("Password Strength Checker", password_strength.run),
    "2": ("Login Lockout Simulator", login_lockout.run),
    "3": ("Secure Password Generator", password_generator.run),
    "4": ("Brute Force Attack Detection", brute_force_detection.run),
    "5": ("Password Guessing Detection", password_guessing_detection.run),
}


def print_menu():
    print_home_banner()
    print()
    print(c("  MAIN MENU", Color.BOLD + Color.WHITE))
    print(c("  " + "-" * 40, Color.BLUE))
    for key, (label, _) in MENU_ITEMS.items():
        print(menu_option(key, label))
    print(menu_option("0", c("Exit Toolkit", Color.RED)))
    print(c("  " + "-" * 40, Color.BLUE))


def main():
    while True:
        print_menu()
        choice = input(c("\n  Select a module (0-5): ", Color.CYAN)).strip()

        if choice == "0":
            clear_screen()
            print(c("\n  Thank you for using the Secure Authentication Toolkit.", Color.CYAN))
            print(c("  Stay safe out there.\n", Color.CYAN))
            break

        if choice in MENU_ITEMS:
            _, module_func = MENU_ITEMS[choice]
            try:
                module_func()
            except KeyboardInterrupt:
                print(c("\n\n  Module interrupted. Returning to main menu.", Color.YELLOW))
                pause()
        else:
            print(c("\n  Invalid selection. Please choose a number between 0 and 5.", Color.RED))
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n\n  Toolkit closed.", Color.CYAN))
