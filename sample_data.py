"""
Module 5 - Password Guessing Detection
------------------------------------------
Identifies password-guessing attacks by tracking failed login attempts
per USERNAME (rather than per IP) and flagging accounts where multiple
different passwords were attempted -- a hallmark of credential
guessing / dictionary attacks against a specific account.
"""

from collections import defaultdict
from modules.theme import Color, c, print_section_header, print_box, alert_box, pause
from modules.sample_data import SAMPLE_LOGIN_ATTEMPTS

DISTINCT_PASSWORD_THRESHOLD = 3


def analyze_password_guessing(login_attempts, threshold=DISTINCT_PASSWORD_THRESHOLD):
    """
    Track failed attempts per username, recording the set of distinct
    passwords tried and the IPs involved.
    Returns: user_stats dict, and flagged dict of usernames meeting threshold.
    """
    user_stats = defaultdict(lambda: {"failed": 0, "passwords": set(), "ips": set()})

    for ip, username, password, status, ts in login_attempts:
        if status == "FAILED":
            user_stats[username]["failed"] += 1
            user_stats[username]["passwords"].add(password)
            user_stats[username]["ips"].add(ip)

    flagged = {
        user: stats for user, stats in user_stats.items()
        if len(stats["passwords"]) >= threshold
    }
    return user_stats, flagged


def run():
    print_section_header(
        "MODULE 5: PASSWORD GUESSING DETECTION",
        f"Flags accounts with {DISTINCT_PASSWORD_THRESHOLD}+ distinct failed password attempts"
    )

    print(c(f"  Analyzing {len(SAMPLE_LOGIN_ATTEMPTS)} simulated login records...\n", Color.CYAN))

    user_stats, flagged = analyze_password_guessing(SAMPLE_LOGIN_ATTEMPTS)

    rows = []
    for user, stats in sorted(user_stats.items(), key=lambda x: -len(x[1]["passwords"])):
        flag = " <-- SUSPICIOUS" if user in flagged else ""
        rows.append(
            f"{user:<10} failed: {stats['failed']:<3} distinct passwords: {len(stats['passwords']):<3}{flag}"
        )
    print_box(rows, color=Color.WHITE, title="Failed Attempts by Username")

    print()
    if flagged:
        alert_box(["PASSWORD GUESSING ATTACK(S) DETECTED"], level="HIGH")
        for user, stats in flagged.items():
            print()
            print(c(f"  [ALERT] Targeted account: {user}", Color.RED + Color.BOLD))
            print(c(f"          Distinct passwords tried: {len(stats['passwords'])}", Color.RED))
            print(c(f"          Source IP(s): {', '.join(sorted(stats['ips']))}", Color.RED))

        print()
        print(c("  SUMMARY", Color.YELLOW + Color.BOLD))
        print(c(f"  Total usernames analyzed : {len(user_stats)}", Color.WHITE))
        print(c(f"  Flagged as suspicious    : {len(flagged)}", Color.RED))
    else:
        print(c("  No password-guessing activity detected in this dataset.", Color.GREEN))

    pause()


if __name__ == "__main__":
    run()
