#!/usr/bin/env python3
import io
import sys
import zipfile
import requests
from pathlib import Path

# URL of the main‑branch ZIP archive
REPO_ZIP_URL = (
    "https://github.com/googlefonts/noto-emoji"
    "/archive/refs/heads/main.zip"
)

# Local directory to collect all SVGs
OUTPUT_DIR = Path("svg")

# Internal ZIP paths to pull from
TARGET_PATHS = [
    "noto-emoji-main/svg/",
    "noto-emoji-main/third_party/region-flags/waved-svg/",
]

def is_target_svg(info: zipfile.ZipInfo) -> bool:
    """Return True if entry is an SVG under one of TARGET_PATHS."""
    name = info.filename.lower()
    if not name.endswith(".svg"):
        return False
    return any(info.filename.startswith(p) for p in TARGET_PATHS)

def download_and_extract():
    """Download repo ZIP and extract matching SVGs into OUTPUT_DIR."""
    resp = requests.get(REPO_ZIP_URL, stream=True)
    resp.raise_for_status()

    buffer = io.BytesIO(resp.content)
    with zipfile.ZipFile(buffer) as z:
        OUTPUT_DIR.mkdir(exist_ok=True)
        for info in z.infolist():
            if not is_target_svg(info):
                continue

            # Flatten into OUTPUT_DIR by filename only
            filename = Path(info.filename).name
            dest = OUTPUT_DIR / filename
            if dest.exists():
                print(f"Skip exists: {filename}")
                continue

            with z.open(info) as src, open(dest, "wb") as out:
                out.write(src.read())
            print(f"Extracted: {filename}")

if __name__ == "__main__":
    try:
        download_and_extract()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
