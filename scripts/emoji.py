#!/usr/bin/env python3

# python ./scripts/emoji.py -i test -o emoji

import argparse
import shutil
from pathlib import Path

def codes_to_emoji(code_seq: str) -> str:
    """
    Convert a sequence of hex codes (e.g. "00a9_1f600") to actual emoji string.
    """
    # split on underscores, parse each hex as integer, then to chr
    return ''.join(chr(int(h, 16)) for h in code_seq.split('_'))

def main(input_dir: Path, output_dir: Path) -> None:
    """
    Scan input_dir/<size>/emoji_u*.png → copy to output_dir/<size>/<emoji>.png
    """
    for size_folder in input_dir.iterdir():
        if not size_folder.is_dir():
            continue

        target_folder = output_dir / size_folder.name
        target_folder.mkdir(parents=True, exist_ok=True)

        for src in size_folder.glob('emoji_u*.png'):
            stem = src.stem                 # e.g. "emoji_u00a9"
            # remove prefix "emoji_u"
            code_seq = stem.removeprefix('emoji_u')
            emoji = codes_to_emoji(code_seq)
            dst = target_folder / f"{emoji}"
            shutil.copy2(src, dst)         # preserve metadata
            print(f"Copied {src.name} → {dst.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create emoji‑named copies of codepoint PNGs"
    )
    parser.add_argument(
        "--input-dir", "-i",
        type=Path, default=Path("test"),
        help="source root (e.g. test/)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path, default=Path("emoji"),
        help="target root (e.g. emoji/)"
    )
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
