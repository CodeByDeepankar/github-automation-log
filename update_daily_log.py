#!/usr/bin/env python3
"""
GitHub Actions Script for Daily Log Updates

This script is designed to run in a GitHub Actions environment
to update a daily log file automatically.
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path


def run_command(command, check=True):
    """
    Execute a shell command and return the result
    
    Args:
        command (str): Command to execute
        check (bool): Whether to raise exception on non-zero exit code
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout.strip(), e.stderr.strip()


def create_or_update_log_file(log_file_path, log_entry):
    """
    Create or update the log file with a new entry
    
    Args:
        log_file_path (Path): Path to the log file
        log_entry (str): Entry to add to the log
    """
    print(f"📝 Updating log file: {log_file_path}")
    
    # Create the log file if it doesn't exist
    if not log_file_path.exists():
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        log_file_path.write_text("# Learning Log\n\nThis file tracks daily learning activities and system maintenance tasks.\n\n")
        print(f"📄 Created new log file: {log_file_path}")
    
    # Read existing content
    content = log_file_path.read_text(encoding='utf-8')
    
    # Append the new log entry
    if content and not content.endswith('\n'):
        content += '\n'
    content += log_entry + '\n'
    
    # Write back to file
    log_file_path.write_text(content, encoding='utf-8')
    print(f"✅ Log entry added to {log_file_path}")


def check_if_already_logged_today(log_file_path, today_str):
    """
    Check if an entry for today already exists in the log
    
    Args:
        log_file_path (Path): Path to the log file
        today_str (str): Today's date string in YYYY-MM-DD format
    
    Returns:
        bool: True if already logged today, False otherwise
    """
    if not log_file_path.exists():
        return False
    
    content = log_file_path.read_text(encoding='utf-8')
    return today_str in content


def generate_daily_entry():
    """
    Generate a meaningful daily entry for the log
    
    Returns:
        str: Timestamped log entry
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    weekday = now.strftime("%A")
    
    # Create a meaningful log entry
    log_entry = f"[{timestamp}] Daily automation: Updated learning log on {weekday}. "
    log_entry += f"Performed system maintenance, reviewed documentation, and practiced automation workflows. "
    log_entry += f"Task ID: AUTO-{now.strftime('%Y%m%d')}-{hash(timestamp) % 10000:04d}"
    
    return log_entry


def main():
    """
    Main function to execute the daily logging process in GitHub Actions
    """
    print("🚀 GitHub Actions Daily Logging System")
    print("=" * 50)
    
    # Get today's date for the log entry
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # Define log file path
    log_file_path = Path("learning_log.md")
    
    # Check if we've already logged today
    if check_if_already_logged_today(log_file_path, today_str):
        print(f"ℹ️  Already logged for {today_str}, skipping...")
        print("💡 This prevents duplicate daily entries as intended.")
        return 0
    
    # Generate daily log entry
    log_entry = generate_daily_entry()
    print(f"📝 Generated log entry for {today_str}")
    
    # Create or update the log file
    create_or_update_log_file(log_file_path, log_entry)
    
    # Stage the changes
    print("🔄 Staging changes...")
    ret_code, _, stderr = run_command("git add learning_log.md")
    if ret_code != 0:
        print(f"❌ Failed to stage file: {stderr}")
        return 1
    
    print("✅ File staged successfully")
    
    # Check if there are actually changes to commit
    ret_code, diff_result, _ = run_command("git diff --cached --quiet learning_log.md", check=False)
    if ret_code == 0:
        # No changes staged
        print("ℹ️  No changes to commit")
        return 0
    
    # Commit the changes
    commit_message = f"docs: Update daily learning log for {today_str}"
    ret_code, _, stderr = run_command(f'git commit -m "{commit_message}"')
    if ret_code != 0:
        print(f"❌ Failed to commit: {stderr}")
        return 1
    
    print("✅ Changes committed successfully")
    
    # For GitHub Actions, we don't push here as the workflow handles that
    print(f"📅 Log entry created for {today_str}")
    print("✅ Daily logging completed successfully!")
    
    return 0


if __name__ == "__main__":
    exit(main())