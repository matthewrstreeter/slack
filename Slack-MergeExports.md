# Slack-MergeExports.py

A small utility to merge two Slack export ZIP files into a single combined export.

## Overview

This script extracts two Slack export ZIP files, merges `users.json`, `channels.json`, and channel message files, removes duplicate messages by timestamp, and writes a new merged ZIP archive.

## Requirements

- Python 3.8+
- Standard library only (`json`, `os`, `zipfile`, `shutil`, `argparse`, `sys`, `tempfile`, `collections`)

## Usage

```bash
git clone <repo>
cd /path/to/Slack
python merge_slack_exports.py export1.zip export2.zip merged.zip
```

### Example

```bash
python merge_slack_exports.py slack-export-1.zip slack-export-2.zip slack-merged.zip
```

## How it works

- Extracts both ZIP files to temporary directories
- Detects the export root directory in each archive
- Merges `users.json` and `channels.json` by unique `id`
- Merges channel message JSON files and deduplicates messages using the `ts` field
- Sorts merged channel message files by timestamp
- Creates a new ZIP archive containing the merged export

## Notes

- The script expects both exports to come from the same Slack workspace.
- It assumes export folder structure matches Slack export format, with top-level `users.json` and `channels.json`.
- Non-JSON files inside channel folders are ignored.
- The output file will be overwritten if it already exists.

## Limitations

- Does not merge or validate files beyond `users.json`, `channels.json`, and channel message JSON files.
- Does not handle workspace export format changes or incompatible export versions.

## License

Use this script freely for Slack export merging tasks.
