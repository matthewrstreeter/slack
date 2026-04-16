# Slack-MergeExports.py
# A script to merge two Slack export ZIP files into a single export.
# Usage: python merge_slack_exports.py export1.zip export2.zip merged.zip
# Note: This script assumes both exports are from the same workspace and have compatible formats.
# V1.0 - 15-Apr-2026 - Initial version

import json
import os
import zipfile
import shutil
import argparse
import sys
from collections import defaultdict


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def merge_users(base_users, new_users):
    seen = {u["id"] for u in base_users}
    for u in new_users:
        if u["id"] not in seen:
            base_users.append(u)
            seen.add(u["id"])
    return base_users


def merge_channels(base_channels, new_channels):
    seen = {c["id"] for c in base_channels}
    for c in new_channels:
        if c["id"] not in seen:
            base_channels.append(c)
            seen.add(c["id"])
    return base_channels


def merge_message_files(base_file, new_file):
    if not os.path.exists(base_file):
        shutil.copy(new_file, base_file)
        return

    base_msgs = load_json(base_file)
    new_msgs = load_json(new_file)

    # deduplicate by ts
    seen = {m.get("ts") for m in base_msgs}
    for msg in new_msgs:
        if msg.get("ts") not in seen:
            base_msgs.append(msg)
            seen.add(msg.get("ts"))

    base_msgs.sort(key=lambda m: m.get("ts", "0"))
    save_json(base_file, base_msgs)


def merge_exports(zip1, zip2, out_zip, temp_dir="merged_tmp"):
    # Validate input files exist
    if not os.path.exists(zip1):
        raise FileNotFoundError(f"Input file not found: {zip1}")
    if not os.path.exists(zip2):
        raise FileNotFoundError(f"Input file not found: {zip2}")
    
    print(f"Merging {os.path.basename(zip1)} and {os.path.basename(zip2)}...")
    
    # Extract both zips
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    extract1 = os.path.join(temp_dir, "export1")
    extract2 = os.path.join(temp_dir, "export2")
    out_dir = os.path.join(temp_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    print("Extracting first export...")
    with zipfile.ZipFile(zip1, "r") as z:
        z.extractall(extract1)
    print("Extracting second export...")
    with zipfile.ZipFile(zip2, "r") as z:
        z.extractall(extract2)

    # Assume root folder name inside export
    def find_root(path):
        entries = list(os.scandir(path))
        # Case 1: Slack export with files at the top level
        if any(e.name == "users.json" for e in entries):
            return path
        # Case 2: Slack export nested inside a single folder
        subdirs = [e for e in entries if e.is_dir()]
        if len(subdirs) == 1:
            return subdirs[0].path
        raise RuntimeError(f"Could not determine export root in {path}")
    root1 = find_root(extract1)
    root2 = find_root(extract2)

    # Merge users.json
    users1 = load_json(os.path.join(root1, "users.json"))
    users2 = load_json(os.path.join(root2, "users.json"))
    merged_users = merge_users(users1, users2)
    save_json(os.path.join(out_dir, "users.json"), merged_users)

    # Merge channels.json
    channels1 = load_json(os.path.join(root1, "channels.json"))
    channels2 = load_json(os.path.join(root2, "channels.json"))
    merged_channels = merge_channels(channels1, channels2)
    save_json(os.path.join(out_dir, "channels.json"), merged_channels)

    # Merge channel message folders
    for root in [root1, root2]:
        for entry in os.scandir(root):
            # skip top-level JSON files (users.json, channels.json, canvases.json, etc.)
            if entry.is_file():
                continue

            # handle only channel folders
            if entry.is_dir():
                out_chan_dir = os.path.join(out_dir, os.path.basename(entry.path))
                os.makedirs(out_chan_dir, exist_ok=True)

                for file in os.scandir(entry.path):
                    if not file.name.endswith(".json"):
                        continue
                    out_file = os.path.join(out_chan_dir, file.name)
                    merge_message_files(out_file, file.path)

    # Zip it up
    print("Creating merged export...")
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(out_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, out_dir)
                z.write(full, rel)

    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"✓ Merged export written to {out_zip}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge two Slack export ZIP files into a single export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python merge_slack_exports.py export1.zip export2.zip merged.zip
  python merge_slack_exports.py /path/to/export1.zip /path/to/export2.zip /path/to/merged.zip
        """
    )
    parser.add_argument("zip1", help="First Slack export ZIP file")
    parser.add_argument("zip2", help="Second Slack export ZIP file")
    parser.add_argument("output", help="Output merged ZIP file path")
    
    args = parser.parse_args()
    
    try:
        merge_exports(args.zip1, args.zip2, args.output)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
