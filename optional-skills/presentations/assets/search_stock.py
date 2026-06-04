#!/usr/bin/env python3
"""
Search and download stock photos from Unsplash.

Usage:
    python search_stock.py <query> [--count N] [--download INDEX]

Requires an Unsplash API key. Get one for free at:
    https://unsplash.com/developers
    -> Register as developer -> Create app -> Copy Access Key

Set it via environment variable:
    $env:UNSPLASH_ACCESS_KEY = "your-key-here"

Examples:
    python search_stock.py "technology office" --count 10
    python search_stock.py "nature mountains" --download 3
    python search_stock.py "abstract background" --download 0 --output bg.jpg

If no --download flag, shows results with index, photographer, and dimensions.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path


UNSPLASH_API = "https://api.unsplash.com"


def get_key():
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        print("Error: UNSPLASH_ACCESS_KEY environment variable not set.")
        print("Get a free key at: https://unsplash.com/developers")
        print("Then run: $env:UNSPLASH_ACCESS_KEY = 'your-key-here'")
        sys.exit(1)
    return key


def search_photos(query: str, access_key: str, per_page: int = 10) -> list:
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": "landscape",
    })
    url = f"{UNSPLASH_API}/search/photos?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {access_key}"})

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    return data.get("results", [])


def download_photo(photo: dict, output_path: str = None) -> str:
    download_url = photo["urls"]["regular"]
    trigger_url = photo["links"]["download_location"]

    if not output_path:
        slug = photo.get("slug", "photo").replace("-", "_")
        output_path = f"{slug}.jpg"

    urllib.request.urlretrieve(download_url, output_path)
    return output_path


def main():
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    query = sys.argv[1]
    count = 10
    download_idx = None
    output = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == "--download" and i + 1 < len(args):
            download_idx = int(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output = args[i + 1]
            i += 2
        else:
            i += 1

    key = get_key()
    print(f"Searching Unsplash for: {query}")
    results = search_photos(query, key, per_page=count)

    if not results:
        print("No results found.")
        return

    for idx, photo in enumerate(results):
        desc = photo.get("description") or photo.get("alt_description") or "(no description)"
        user = photo["user"]["name"]
        w, h = photo["width"], photo["height"]
        print(f"\n  [{idx}] {desc[:80]}")
        print(f"      by {user} — {w}x{h}")
        print(f"      raw: {photo['urls']['raw']}")

    if download_idx is not None:
        if 0 <= download_idx < len(results):
            photo = results[download_idx]
            path = download_photo(photo, output)
            print(f"\nDownloaded: {path}")
        else:
            print(f"\nError: index {download_idx} out of range (0-{len(results)-1})")
    else:
        print(f"\nTo download: add --download <index> (0-{len(results)-1})")


if __name__ == "__main__":
    main()
