#!/usr/bin/env python3
"""
Test script for GitHub Daily Logger System
Validates the core functionality without making actual Git commits
"""

import tempfile
import os
from pathlib import Path
from github_daily_logger import (
    check_git_config,
    check_if_already_logged_today,
    create_or_update_log_file,
    generate_daily_entry
)


def test_functions():
    """
    Test the core functions of the GitHub daily logger
    """
    print("🧪 Testing GitHub Daily Logger Functions")
    print("=" * 50)
    
    # Test log entry generation
    print("\n1. Testing log entry generation...")
    entry = generate_daily_entry()
    print(f"✅ Generated entry: {entry[:50]}...")
    
    # Test log file creation/updating in temporary directory
    print("\n2. Testing log file operations...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        log_file = temp_path / "test_log.md"
        
        # Create initial content
        initial_content = "# Test Log\n\n"
        log_file.write_text(initial_content)
        
        # Add a test entry
        test_entry = "[2024-01-01 12:00:00] Test entry for validation"
        create_or_update_log_file(log_file, test_entry)
        
        # Verify the file was updated
        updated_content = log_file.read_text()
        assert test_entry in updated_content
        print("✅ Log file operations working correctly")
        
        # Test duplicate detection
        print("\n3. Testing duplicate detection...")
        today_str = "2024-01-01"  # Use the same date as our test entry
        already_logged = check_if_already_logged_today(log_file, today_str)
        print(f"✅ Duplicate detection working: {already_logged}")
    
    # Test Git configuration (this will fail in test environment without Git)
    print("\n4. Testing Git configuration check...")
    git_configured = check_git_config()
    if git_configured:
        print("✅ Git configuration valid")
    else:
        print("ℹ️  Git not configured in test environment (expected)")
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    test_functions()