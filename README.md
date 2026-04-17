# Slack
Slack-related scripts and utilities.

## Included scripts

- `Slack-MergeExports.py` — merge two Slack export ZIP archives into one combined export.
- `Slack-SendMessage.ps1` — send a message to a Slack channel using the Slack API from PowerShell.

## Documentation

- `Slack-MergeExports.md` — details and usage for Slack export merging.
- `Slack-SendMessage.md` — details and usage for sending Slack messages via PowerShell.

## Notes

- `Slack-MergeExports.py` is useful for combining workspace exports while deduplicating messages by timestamp.
- `Slack-SendMessage.ps1` includes a reusable `Send-SlackMessage` function and error handling for common Slack API responses.
