"""
Module 1 - Password Strength Checker
-------------------------------------
Evaluates the strength of a user-supplied password using a scoring
system based on length, character variety, and common-password checks.
"""

import re
from modules.theme import (
    Color, c, print_section_header, print_box, pause
)

# A small sample of extremely common / breached passwords for demonstration.
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "password1", "111111", "letmein",
    "admin", "welcome", "iloveyou", "monkey", "dragon"
}


def evaluate_password(password: str) -> dict:
    """
    Analyze a password and return a dict with score, strength label,
    and a list of feedback tips.
    """
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\[\]/\\+=~`;']", password))
    is_common = password.lower() in COMMON_PASSWORDS

    score = 0
    feedback = []

    # --- Length scoring ---
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters (12+ recommended).")

    # --- Character variety scoring ---
    variety = sum([has_upper, has_lower, has_digit, has_special])
    score += variety

    if not has_upper:
        feedback.append("Add at least one uppercase letter (A-Z).")
    if not has_lower:
        feedback.append("Add at least one lowercase letter (a-z).")
    if not has_digit:
        feedback.append("Add at least one number (0-9).")
    if not has_special:
        feedback.append("Add at least one special character (e.g. !@#$%).")

    # --- Common password penalty ---
    if is_common:
        score = 0
        feedback.insert(0, "This password appears in common password lists. Avoid it entirely.")

    # --- Repeated / sequential character penalty ---
    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 1)
        feedback.append("Avoid repeating the same character 3+ times in a row.")

    # Cap score at 6 for classification
    score = max(0, min(score, 6))

    if score <= 1:
        strength = "Very Weak"
        color = Color.RED
    elif score <= 2:
        strength = "Weak"
        color = Color.RED
    elif score <= 4:
        strength = "Moderate"
        color = Color.YELLOW
    elif score == 5:
        strength = "Strong"
        color = Color.GREEN
    else:
        strength = "Very Strong"
        color = Color.GREEN

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "is_common": is_common,
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback,
    }


def render_strength_bar(score, max_score=6, width=20):
    filled = int((score / max_score) * width)
    bar = "#" * filled + "-" * (width - filled)
    return bar


def run():
    """Entry point called from the main menu."""
    print_section_header(
        "MODULE 1: PASSWORD STRENGTH CHECKER",
        "Evaluates password quality using length, variety, and breach checks"
    )

    password = input(c("Enter a password to evaluate: ", Color.CYAN))
    result = evaluate_password(password)

    print()
    bar = render_strength_bar(result["score"])
    print(c(f"  Strength: {result['strength']}", result["color"] + Color.BOLD))
    print(c(f"  [{bar}]  Score: {result['score']}/6", result["color"]))
    print()

    checklist = [
        f"Length >= 8 chars      : {'YES' if result['length'] >= 8 else 'NO'} ({result['length']} chars)",
        f"Uppercase letter (A-Z) : {'YES' if result['has_upper'] else 'NO'}",
        f"Lowercase letter (a-z) : {'YES' if result['has_lower'] else 'NO'}",
        f"Digit (0-9)            : {'YES' if result['has_digit'] else 'NO'}",
        f"Special character      : {'YES' if result['has_special'] else 'NO'}",
        f"Common password list   : {'FOUND - DANGER' if result['is_common'] else 'Not found'}",
    ]
    print_box(checklist, color=Color.WHITE, title="Password Analysis")

    if result["feedback"]:
        print()
        print(c("  Recommendations:", Color.YELLOW + Color.BOLD))
        for tip in result["feedback"]:
            print(c(f"   - {tip}", Color.YELLOW))

    pause()


if __name__ == "__main__":
    run()
