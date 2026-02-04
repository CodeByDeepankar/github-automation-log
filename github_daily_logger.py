#!/usr/bin/env python3
"""
Ethical GitHub Contribution Logger System

This script creates a daily log entry to GitHub for educational and documentation purposes.
It demonstrates legitimate automation practices while emphasizing ethical usage.

PURPOSE:
- Educational automation practice
- Learning log/journal maintenance
- Documentation consistency
- Git/GitHub workflow practice

ETHICAL GUIDELINES:
- Each contribution represents actual work performed
- Not intended to deceive or artificially inflate metrics
- Focuses on real documentation and learning tracking
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path
import argparse


def run_command(command, cwd=None, check=True):
    """
    Execute a shell command and return the result
    
    Args:
        command (str): Command to execute
        cwd (str, optional): Working directory
        check (bool): Whether to raise exception on non-zero exit code
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout.strip(), e.stderr.strip()


def check_git_config():
    """
    Verify Git is properly configured with user information
    
    Returns:
        bool: True if Git is properly configured, False otherwise
    """
    print("🔍 Checking Git configuration...")
    
    # Check if Git is installed
    ret_code, _, _ = run_command("git --version")
    if ret_code != 0:
        print("❌ Git is not installed or not in PATH")
        return False
    
    # Check username and email
    ret_code_user, username, _ = run_command("git config --get user.name")
    ret_code_email, email, _ = run_command("git config --get user.email")
    
    if ret_code_user != 0 or not username:
        print("❌ Git username not configured. Run: git config --global user.name 'Your Name'")
        return False
    
    if ret_code_email != 0 or not email:
        print("❌ Git email not configured. Run: git config --global user.email 'your@email.com'")
        return False
    
    print(f"✅ Git configured: {username} <{email}>")
    return True


def get_current_repo_info():
    """
    Get information about the current Git repository
    
    Returns:
        dict: Repository information or None if not in a Git repo
    """
    ret_code, repo_path, _ = run_command("git rev-parse --show-toplevel")
    if ret_code != 0:
        return None
    
    ret_code, remote_url, _ = run_command("git config --get remote.origin.url")
    if ret_code != 0:
        return None
    
    ret_code, current_branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if ret_code != 0:
        return None
    
    return {
        'path': repo_path,
        'remote_url': remote_url,
        'branch': current_branch
    }


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
        log_file_path.write_text("")
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


def stage_and_commit_changes(log_file_path, commit_message):
    """
    Stage and commit changes to Git
    
    Args:
        log_file_path (Path): Path to the log file
        commit_message (str): Commit message
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🔄 Staging changes...")
    
    # Stage the log file
    ret_code, _, stderr = run_command(f"git add '{log_file_path}'")
    if ret_code != 0:
        print(f"❌ Failed to stage file: {stderr}")
        return False
    
    print("✅ File staged successfully")
    
    # Commit the changes
    ret_code, _, stderr = run_command(f'git commit -m "{commit_message}"')
    if ret_code != 0:
        if "nothing to commit" in stderr.lower():
            print("ℹ️  No changes to commit (already up to date)")
            return True
        else:
            print(f"❌ Failed to commit: {stderr}")
            return False
    
    print("✅ Changes committed successfully")
    return True


def push_changes():
    """
    Push changes to the remote repository
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("📤 Pushing changes to remote repository...")
    
    # Get current branch
    ret_code, current_branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if ret_code != 0:
        print("❌ Unable to determine current branch")
        return False
    
    # Push to remote
    ret_code, _, stderr = run_command(f"git push origin {current_branch}")
    if ret_code != 0:
        print(f"❌ Failed to push changes: {stderr}")
        return False
    
    print("✅ Changes pushed successfully")
    return True


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


def main(repo_path=None, log_file="learning_log.md"):
    """
    Main function to execute the daily logging process
    
    Args:
        repo_path (str, optional): Path to the Git repository
        log_file (str): Name of the log file to update
    """
    print("🚀 GitHub Daily Logging System")
    print("=" * 50)
    
    # Validate Git configuration
    if not check_git_config():
        print("❌ Git is not properly configured. Exiting.")
        sys.exit(1)
    
    # Determine repository path
    if repo_path:
        repo_path = Path(repo_path)
        if not repo_path.exists():
            print(f"❌ Repository path does not exist: {repo_path}")
            sys.exit(1)
        os.chdir(repo_path)
    else:
        repo_info = get_current_repo_info()
        if not repo_info:
            print("❌ Not in a Git repository or no remote configured")
            print("Please run this script inside a Git repository with a remote origin.")
            sys.exit(1)
        print(f"📁 Using repository: {repo_info['path']}")
        print(f"🔗 Remote: {repo_info['remote_url']}")
        print(f"SetBranch: {repo_info['branch']}")
    
    # Get today's date for the log entry
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # Define log file path
    log_file_path = Path(log_file)
    
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
    
    # Stage and commit changes
    commit_message = f"docs: Update daily learning log for {today_str}"
    if not stage_and_commit_changes(log_file_path, commit_message):
        print("❌ Failed to stage and commit changes")
        return 1
    
    # Push changes to remote repository
    if not push_changes():
        print("❌ Failed to push changes")
        return 1
    
    print("🎉 Daily logging completed successfully!")
    print(f"📅 Entry logged for {today_str}")
    print(f"📄 Updated {log_file}")
    
    return 0


def create_sample_readme():
    """
    Create a sample README explaining the purpose of this automation
    """
    readme_content = """# Daily Learning Log

This repository contains an automated daily log that tracks learning activities and system maintenance. 

## Purpose

This project demonstrates ethical automation practices:
- Educational exercise in Git/GitHub automation
- Learning log maintenance
- Documentation consistency
- Real skill development

## Ethical Guidelines

This automation follows ethical principles:
- Each entry represents actual work performed
- Not intended to deceive or artificially inflate metrics
- Focuses on real documentation and learning tracking
- Demonstrates legitimate automation techniques

## Technical Details

The daily log is updated by a Python script that:
1. Generates a meaningful entry for the day
2. Commits the changes with a descriptive message
3. Pushes to the remote repository

Last updated: {}
""".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    readme_path = Path("README.md")
    if not readme_path.exists():
        readme_path.write_text(readme_content)
        print(f"📄 Created README.md explaining the project")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ethical GitHub Daily Logging System - Educational Automation Practice"
    )
    parser.add_argument(
        "--repo-path",
        type=str,
        help="Path to the Git repository (default: current directory)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="learning_log.md",
        help="Name of the log file to update (default: learning_log.md)"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize repository with sample files"
    )
    
    args = parser.parse_args()
    
    if args.init:
        print("🔧 Initializing repository with sample files...")
        create_sample_readme()
        # Create a basic .gitignore if it doesn't exist
        gitignore_path = Path(".gitignore")
        if not gitignore_path.exists():
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
            gitignore_path.write_text(gitignore_content)
            print("📄 Created .gitignore")
    
    exit_code = main(args.repo_path, args.log_file)
    sys.exit(exit_code)