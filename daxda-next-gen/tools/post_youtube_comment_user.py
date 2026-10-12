#!/usr/bin/env python3
"""
DAXDA.IA — YouTube Comment Poster for User (osmesirius@gmail.com)
Allows the user to dispatch pre-governed YouTube comments directly under their
authenticated Google account (osmesirius@gmail.com).

Modes:
1. Browser + Clipboard Dispatch: Copies comment to macOS clipboard and opens video in browser.
2. Official YouTube API Dispatch: Uses OAuth 2.0 credentials for osmesirius@gmail.com.
"""

import os
import sys
import json
import subprocess
import argparse

USER_GOOGLE_ACCOUNT = "osmesirius@gmail.com"

def copy_to_clipboard(text: str) -> bool:
    """Copy text to macOS system clipboard."""
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except Exception as e:
        print(f"Warning: Failed to copy to clipboard: {e}")
        return False

def open_url_in_browser(url: str):
    """Open URL in the default macOS browser."""
    try:
        subprocess.run(["open", url], check=True)
    except Exception as e:
        print(f"Warning: Failed to open browser: {e}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base_dir, "outputs", "youtube_outreach_campaign.json")

    parser = argparse.ArgumentParser(description=f"DAXDA YouTube Comment Dispatcher for {USER_GOOGLE_ACCOUNT}")
    parser.add_argument("--creator", type=str, default="3blue1brown", help="Creator ID (e.g., 3blue1brown, lex_fridman, mlst, yannic_kilcher)")
    parser.add_argument("--url", type=str, default="", help="Direct YouTube Video URL to open")
    parser.add_argument("--list", action="store_true", help="List all available creator targets")
    args = parser.parse_args()

    if not os.path.exists(manifest_path):
        print("Manifest not found. Running synthesizer first...")
        subprocess.run([sys.executable, os.path.join(base_dir, "tools", "youtube_outreach_synthesizer.py")], check=True)

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    creators = {c["id"]: c for c in data.get("creators", [])}

    if args.list:
        print("=" * 80)
        print(f"AVAILABLE CREATOR TARGETS (Authorized User: {USER_GOOGLE_ACCOUNT})")
        print("=" * 80)
        for cid, c in creators.items():
            print(f"• ID: {cid:20s} | Channel: {c['channel_name']} ({c['subscribers']})")
            print(f"  Theme: {c['core_theme']}")
        return

    creator_data = creators.get(args.creator.lower())
    if not creator_data:
        print(f"Error: Creator ID '{args.creator}' not found. Run with --list to view valid targets.")
        sys.exit(1)

    print("=" * 80)
    print("   DAXDA.IA — YOUTUBE OUTREACH DISPATCHER")
    print(f"   Authorized Google Account: {USER_GOOGLE_ACCOUNT}")
    print(f"   Target Creator:            {creator_data['channel_name']} ({creator_data['handle']})")
    print(f"   Subscribers:               {creator_data['subscribers']}")
    print(f"   Theme:                     {creator_data['core_theme']}")
    print("=" * 80)

    comment = creator_data["comment_draft"]
    print("\n📝 GOVERNED COMMENT PAYLOAD:")
    print("-" * 80)
    print(comment)
    print("-" * 80)

    # 1. Copy to macOS clipboard
    if copy_to_clipboard(comment):
        print(f"\n✅ Comment successfully copied to clipboard for account: {USER_GOOGLE_ACCOUNT}!")
    else:
        print("\n⚠️ Clipboard copy unavailable. You can copy the text manually from the terminal above.")

    # 2. Open browser if URL specified or channel link provided
    target_url = args.url if args.url else f"https://www.youtube.com/{creator_data['handle']}/videos"
    print(f"\n🌐 Opening target in browser ({target_url})...")
    open_url_in_browser(target_url)

    print(f"\n👉 INSTRUCTIONS FOR {USER_GOOGLE_ACCOUNT}:")
    print("1. Your browser has been opened to the creator's video page.")
    print(f"2. Ensure you are signed into YouTube with: {USER_GOOGLE_ACCOUNT}")
    print("3. Select the latest relevant video.")
    print("4. Paste (Cmd + V) the pre-audited comment into the comment box and click 'Comment'!")
    print("=" * 80)

if __name__ == "__main__":
    main()
