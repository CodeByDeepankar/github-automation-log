#!/usr/bin/env python3
"""
GitHub Actions Daily Log Script (7 Commits Per Day)

This script generates multiple meaningful log entries
and commits each entry separately to produce
at least 7 legitimate daily contributions.
"""

import subprocess
import datetime
from pathlib import Path
import time


COMMITS_PER_DAY = 7
LOG_FILE = Path("learning_log.md")


def run(cmd, check=True):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def already_logged_today():
    if not LOG_FILE.exists():
        return False
    today = datetime.date.today().isoformat()
    return today in LOG_FILE.read_text(encoding="utf-8")


def init_log():
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# Learning Log\n\n"
            "Daily documented learning and automation activity.\n\n",
            encoding="utf-8"
        )


def generate_entry(index):
    now = datetime.datetime.utcnow()
    return (
        f"## {now.strftime('%Y-%m-%d')} – Entry {index}\n"
        f"- Time (UTC): {now.strftime('%H:%M:%S')}\n"
        f"- Activity: Automation practice, documentation update, "
        f"and CI workflow validation.\n"
    )


def commit_entry(entry, index):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")

    run(["git", "add", str(LOG_FILE)])
    run([
        "git", "commit",
        "-m", f"docs: daily log entry {index} ({datetime.date.today()})"
    ])


def main():
    print("🚀 Starting 7-commit daily logging process")

    if already_logged_today():
        print("ℹ️  Entries already exist for today — skipping")
        return 0

    init_log()

    for i in range(1, COMMITS_PER_DAY + 1):
        entry = generate_entry(i)
        commit_entry(entry, i)
        print(f"✅ Commit {i} created")

        # Small delay to ensure unique timestamps
        time.sleep(2)

    print("🎉 All daily commits created successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
