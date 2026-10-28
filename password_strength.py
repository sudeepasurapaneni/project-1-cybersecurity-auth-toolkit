"""
Module 3 - Secure Password Generator
--------------------------------------
Generates a random password based on user-selected criteria:
length, uppercase, lowercase, numbers, and special characters.
Guarantees at least one character from each selected category.
"""

import random
import string
from modules.theme import Color, c, print_section_header, print_box, pause


def ask_yes_no(prompt, default_yes=True):
    suffix = " [Y/n]: " if default_yes else " [y/N]: "
    ans = input(c(prompt + suffix, Color.CYAN)).strip().lower()
    if ans == "":
        return default_yes
    return ans.startswith("y")


def generate_password(length, use_upper, use_lower, use_digits, use_special):
    """
    Build a password of the given length guaranteeing at least one
    character from each selected category, then fill the rest randomly
    and shuffle so category order isn't predictable.
    """
    pools = []
    guaranteed = []

    if use_upper:
        pools.append(string.ascii_uppercase)
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:
        pools.append(string.ascii_lowercase)
        guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:
        pools.append(string.digits)
        guaranteed.append(random.choice(string.digits))
    if use_special:
        specials = "!@#$%^&*()-_=+[]{}?"
        pools.append(specials)
        guaranteed.append(random.choice(specials))

    if not pools:
        return None

    all_chars = "".join(pools)
    remaining_length = max(0, length - len(guaranteed))
    remaining_chars = [random.choice(all_chars) for _ in range(remaining_length)]

    password_chars = guaranteed + remaining_chars
    # If length was smaller than number of categories, trim safely
    password_chars = password_chars[:length] if length >= len(guaranteed) else guaranteed[:length]

    random.shuffle(password_chars)
    return "".join(password_chars)


def rate_generated_password(password, use_upper, use_lower, use_digits, use_special):
    """Quick strength label reused for user feedback (not the full Module 1 logic)."""
    variety = sum([use_upper, use_lower, use_digits, use_special])
    if len(password) >= 12 and variety >= 3:
        return "Very Strong", Color.GREEN
    elif len(password) >= 8 and variety >= 2:
        return "Strong", Color.GREEN
    else:
        return "Moderate", Color.YELLOW


def run():
    print_section_header(
        "MODULE 3: SECURE PASSWORD GENERATOR",
        "Creates a random password matching your selected security criteria"
    )

    try:
        length = int(input(c("Desired password length (recommended 12+): ", Color.CYAN)))
    except ValueError:
        print(c("  Invalid number. Defaulting to length 12.", Color.YELLOW))
        length = 12

    if length < 1:
        length = 12

    print()
    use_upper = ask_yes_no("Include UPPERCASE letters?")
    use_lower = ask_yes_no("Include lowercase letters?")
    use_digits = ask_yes_no("Include numbers?")
    use_special = ask_yes_no("Include special characters?")

    if not any([use_upper, use_lower, use_digits, use_special]):
        print(c("\n  [X] You must select at least one character type.", Color.RED))
        pause()
        return

    if length < sum([use_upper, use_lower, use_digits, use_special]):
        print(c(
            f"\n  [!] Length too short for all selected categories; "
            f"using minimum length {sum([use_upper, use_lower, use_digits, use_special])}.",
            Color.YELLOW
        ))
        length = sum([use_upper, use_lower, use_digits, use_special])

    password = generate_password(length, use_upper, use_lower, use_digits, use_special)
    strength, color = rate_generated_password(password, use_upper, use_lower, use_digits, use_special)

    print()
    print_box([f"Generated Password: {password}"], color=Color.GREEN, title="Result")
    print(c(f"\n  Estimated Strength: {strength}", color + Color.BOLD))
    print(c(f"  Length: {len(password)} characters", Color.WHITE))

    criteria = []
    if use_upper: criteria.append("Uppercase")
    if use_lower: criteria.append("Lowercase")
    if use_digits: criteria.append("Numbers")
    if use_special: criteria.append("Special characters")
    print(c(f"  Criteria used: {', '.join(criteria)}", Color.WHITE))

    pause()


if __name__ == "__main__":
    run()
