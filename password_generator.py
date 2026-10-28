"""
Module 4 - Brute Force Attack Detection
------------------------------------------
Analyzes login attempt logs to detect IP addresses with 3 or more
failed login attempts, which is a common indicator of brute-force
attacks against a login system.
"""

from collections import defaultdict
from modules.theme import Color, c, print_section_header, print_box, alert_box, pause
from modules.sample_data import SAMPLE_LOGIN_ATTEMPTS

FAILED_THRESHOLD = 3


def analyze_brute_force(login_attempts, threshold=FAILED_THRESHOLD):
    """
    Count failed attempts per IP address.
    Returns a dict: { ip: {"failed": int, "usernames": set} }
    and a list of flagged IPs meeting/exceeding the threshold.
    """
    ip_stats = defaultdict(lambda: {"failed": 0, "usernames": set(), "total": 0})

    for ip, username, password, status, ts in login_attempts:
        ip_stats[ip]["total"] += 1
        if status == "FAILED":
            ip_stats[ip]["failed"] += 1
            ip_stats[ip]["usernames"].add(username)

    flagged = {
        ip: stats for ip, stats in ip_stats.items()
        if stats["failed"] >= threshold
    }
    return ip_stats, flagged


def run():
    print_section_header(
        "MODULE 4: BRUTE FORCE ATTACK DETECTION",
        f"Flags IP addresses with {FAILED_THRESHOLD}+ failed login attempts"
    )

    print(c(f"  Analyzing {len(SAMPLE_LOGIN_ATTEMPTS)} simulated login records...\n", Color.CYAN))

    ip_stats, flagged = analyze_brute_force(SAMPLE_LOGIN_ATTEMPTS)

    # Show per-IP summary table
    rows = []
    for ip, stats in sorted(ip_stats.items(), key=lambda x: -x[1]["failed"]):
        flag = " <-- SUSPICIOUS" if ip in flagged else ""
        rows.append(f"{ip:<16} failed: {stats['failed']:<3} total: {stats['total']:<3}{flag}")
    print_box(rows, color=Color.WHITE, title="Login Attempts by IP Address")

    print()
    if flagged:
        alert_box(["BRUTE FORCE ATTACK(S) DETECTED"], level="HIGH")
        for ip, stats in flagged.items():
            print()
            print(c(f"  [ALERT] Suspicious IP: {ip}", Color.RED + Color.BOLD))
            print(c(f"          Failed attempts : {stats['failed']}", Color.RED))
            print(c(f"          Usernames targeted: {', '.join(sorted(stats['usernames']))}", Color.RED))

        print()
        print(c("  SUMMARY", Color.YELLOW + Color.BOLD))
        print(c(f"  Total IPs analyzed   : {len(ip_stats)}", Color.WHITE))
        print(c(f"  Flagged as suspicious: {len(flagged)}", Color.RED))
    else:
        print(c("  No brute-force activity detected in this dataset.", Color.GREEN))

    pause()


if __name__ == "__main__":
    run()
