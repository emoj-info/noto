#!/usr/bin/env python3

import argparse
import shutil
import unicodedata  # for unicode normalization
from pathlib import Path

def codes_to_emoji(code_seq: str) -> str:
    # Convert underscore-separated hex codes into an emoji string,
    # then normalize to NFD for macOS compatibility.
    emoji = ''.join(chr(int(h, 16)) for h in code_seq.split('_'))
    return unicodedata.normalize('NFD', emoji)

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
            # remove prefix "emoji_u"
            code_seq = src.stem.removeprefix('emoji_u')
            emoji = codes_to_emoji(code_seq)
            # add .png extension
            dst = target_folder / f"{emoji}"
            try:
                shutil.copy2(src, dst)  # preserve metadata
                print(f"Copied {src.name} → {dst.name}")
            except OSError as e:
                # выводим ошибку, но скрипт не падает
                print(f"Failed to copy {src.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create emoji‑named copies of codepoint PNGs"
    )
    parser.add_argument(
        "--input-dir", "-i",
        type=Path, default=Path("png"),
        help="source root (e.g. png/)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path, default=Path("emoji"),
        help="target root (e.g. emoji/)"
    )
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
