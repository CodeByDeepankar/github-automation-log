# GitHub Actions Setup for Daily Log Updates

This document explains how to set up and use the GitHub Actions workflow for daily log updates.

## Overview

The GitHub Actions workflow (`daily-commit.yml`) automatically updates a learning log file daily with meaningful entries that represent actual learning or maintenance activities.

## Workflow Configuration

### Schedule
The workflow runs daily at 9:00 AM UTC:

```yaml
schedule:
  - cron: '0 9 * * *'
```

You can adjust this schedule by modifying the cron expression:
- `0 9 * * *` = Daily at 9:00 AM UTC
- `0 14 * * *` = Daily at 2:00 PM UTC
- `30 6 * * 1-5` = Weekdays at 6:30 AM UTC

### Manual Trigger
The workflow can also be triggered manually:

```yaml
workflow_dispatch: # Allows manual trigger
```

## Setup Instructions

### 1. Enable GitHub Actions
1. Navigate to your repository on GitHub
2. Go to the "Actions" tab
3. If prompted, enable GitHub Actions for your repository

### 2. Repository Settings
Make sure your repository allows GitHub Actions to create commits:
1. Go to your repository settings
2. Navigate to "Actions" → "General"
3. Under "Workflow permissions", select "Read and write permissions"
4. Save the changes

### 3. Branch Protection (if applicable)
If you have branch protection rules:
1. Go to repository settings
2. Navigate to "Branches"
3. Edit the protection rules for your default branch
4. Ensure "Allow force pushes" is set appropriately or that GitHub Actions is authorized

## Files Created

### `.github/workflows/daily-commit.yml`
- The main GitHub Actions workflow file
- Contains the schedule and steps for daily updates

### `update_daily_log.py`
- Python script that handles the core logic
- Validates if an entry already exists for today
- Creates meaningful log entries
- Manages Git operations

## How It Works

### 1. Daily Check
- The workflow runs according to the schedule
- Checks if an entry for today's date already exists in `learning_log.md`

### 2. Conditional Update
- If no entry exists for today, creates a new meaningful entry
- If an entry exists, skips the update (idempotent operation)

### 3. Git Operations
- Adds the updated file to Git
- Commits with a descriptive message
- Pushes changes to the repository

## Customization Options

### 1. Environment Variables
You can set repository variables in Settings → Secrets and variables → Actions:
- `GIT_USERNAME`: Git username for commits (defaults to 'github-actions[bot]')
- `GIT_EMAIL`: Git email for commits (defaults to 'github-actions[bot]@users.noreply.github.com')

### 2. Log File Location
The script currently writes to `learning_log.md` but can be modified to use a different file.

### 3. Entry Format
The format of the daily entry can be customized in `update_daily_log.py`.

## Monitoring

### 1. Workflow Runs
Monitor workflow runs in the "Actions" tab of your repository.

### 2. Commit History
Check the commit history to verify daily updates are occurring.

### 3. Log File
Review `learning_log.md` to ensure entries are being added as expected.

## Troubleshooting

### 1. Workflow Not Running
- Verify GitHub Actions is enabled for the repository
- Check that the workflow file is in the correct location
- Ensure the repository has appropriate permissions

### 2. Push Failures
- Verify branch protection settings allow GitHub Actions to push
- Check that the workflow has appropriate permissions

### 3. Duplicate Entries
- The system is designed to prevent this, but if occurring, check the date parsing logic

## Ethical Considerations

This system is designed for legitimate educational and documentation purposes:
- Each entry represents actual learning or maintenance activities
- Not intended to artificially inflate contribution metrics
- Focuses on real documentation and skill development