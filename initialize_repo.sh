#!/bin/bash

# GitHub Daily Logger Initialization Script
# Sets up a repository for ethical daily logging automation

set -e  # Exit on any error

echo "🚀 GitHub Daily Logger - Repository Initialization"
echo "================================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a Git repository. Please run this inside a Git repository or create one first."
    echo ""
    echo "To create a new repository:"
    echo "  mkdir your-repo-name"
    echo "  cd your-repo-name"
    echo "  git init"
    echo "  git remote add origin https://github.com/username/repo-name.git"
    exit 1
fi

echo "✅ Git repository detected"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Python3 detected"

# Check if git configuration is set
if [ -z "$(git config --get user.name)" ] || [ -z "$(git config --get user.email)" ]; then
    echo "❌ Git user name or email not configured"
    echo "Please run:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your@email.com'"
    exit 1
fi

echo "✅ Git configuration verified"

# Create the main Python script if it doesn't exist
if [ ! -f "github_daily_logger.py" ]; then
    echo "📄 Creating github_daily_logger.py..."
    curl -s -o github_daily_logger.py "https://raw.githubusercontent.com/your-repo/github_daily_logger.py" 2>/dev/null || {
        echo "⚠️  Could not download script, using local copy if available"
        if [ ! -f "../github_daily_logger.py" ]; then
            echo "❌ github_daily_logger.py not found locally"
            exit 1
        else
            cp ../github_daily_logger.py ./
            echo "✅ Copied local github_daily_logger.py"
        fi
    }
fi

# Create initial log file if it doesn't exist
if [ ! -f "learning_log.md" ]; then
    echo "📄 Creating initial learning_log.md..."
    cat > learning_log.md << EOF
# Learning Log

This file tracks daily learning activities and system maintenance tasks.

## Format
- Date and time of activity
- Description of work performed
- Technologies or concepts explored
- Challenges encountered and solutions

## Example Entry
[2024-01-15 09:30:00] Performed system maintenance, reviewed documentation, and practiced automation workflows. Researched ethical automation practices and implemented daily logging system.

EOF
    echo "✅ Initial learning_log.md created"
fi

# Create README if it doesn't exist
if [ ! -f "README.md" ]; then
    echo "📄 Creating README.md..."
    cat > README.md << EOF
# Daily Learning Log

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

Last updated: $(date)
EOF
    echo "✅ README.md created"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📄 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
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

# Logs
*.log
logs/
EOF
    echo "✅ .gitignore created"
fi

# Make the Python script executable
chmod +x github_daily_logger.py

# Add files to git if not already tracked
if [ -z "$(git ls-files -- learning_log.md)" ]; then
    git add learning_log.md
    echo "✅ Added learning_log.md to git"
fi

if [ -z "$(git ls-files -- README.md)" ]; then
    git add README.md
    echo "✅ Added README.md to git"
fi

if [ -z "$(git ls-files -- .gitignore)" ]; then
    git add .gitignore
    echo "✅ Added .gitignore to git"
fi

if [ -z "$(git ls-files -- github_daily_logger.py)" ]; then
    git add github_daily_logger.py
    echo "✅ Added github_daily_logger.py to git"
fi

# Commit initial files if there are staged changes
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "feat: Initialize daily learning log system

- Adds github_daily_logger.py automation script
- Creates initial learning_log.md with format
- Adds README explaining ethical automation
- Includes standard Python .gitignore"
    echo "✅ Initial commit created"
else
    echo "ℹ️  No new files to commit (already committed)"
fi

# Test the script
echo "🧪 Testing the daily logger script..."
python3 github_daily_logger.py --log-file learning_log.md

echo ""
echo "🎉 Repository initialized successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Review the generated learning_log.md entry"
echo "2. Customize the script as needed for your use case"
echo "3. Set up scheduling (cron job, Task Scheduler, etc.)"
echo "4. Ensure your Git authentication is configured"
echo ""
echo "🔄 To schedule daily execution:"
echo "   Linux/macOS: Add to crontab: 0 9 * * * cd $(pwd) && python3 github_daily_logger.py"
echo "   Windows: Use Task Scheduler to run daily"
echo ""
echo "⚠️  Remember: Use ethically and only for legitimate learning documentation!"