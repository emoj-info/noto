#!/usr/bin/env python3

# Run this script to update stats in README for PNG files only:
# python ./scripts/stat.py ./raw ./png

import argparse
import os
import re
import sys
from pathlib import Path

# Markers for embedding table in README
MARKER_START = '<!-- DIR-STATS-START -->'
MARKER_END = '<!-- DIR-STATS-END -->'


def get_stats(path: Path) -> tuple[int, int, int]:
    """
    Walk through a directory and count only PNG files:
      - total number of PNG files
      - total number of subdirectories (all)
      - cumulative size of PNG files in bytes
    """
    files = 0
    folders = 0
    size = 0
    for root, dirs, filenames in os.walk(path):
        folders += len(dirs)
        for name in filenames:
            # consider only .png files (case-insensitive)
            if Path(name).suffix.lower() != '.png':
                continue
            files += 1
            try:
                size += (Path(root) / name).stat().st_size
            except Exception:
                continue
    return files, folders, size


def human_readable(num: int) -> str:
    """
    Convert byte count into a human-readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
    return f"{num:.2f} EB"


def build_markdown(name1: str,
                   stats1: tuple[int, int, float],
                   name2: str,
                   stats2: tuple[int, int, float]) -> str:
    """
    Build a markdown table comparing two directories,
    showing size ratio as both factor and percentage.
    """
    files1, _, size1 = stats1
    files2, _, size2 = stats2

    # compute factor and percentage
    if size2:
        factor = size1 / size2
        percent = factor * 100
        ratio = f"{factor:.2f}× ({percent:.2f}%)"
    else:
        ratio = "N/A"

    col1 = name1
    col2 = f"{name2} (opt)"
    header    = f"| Metric       | {col1:<12} | {col2:<15} | Size ratio               |"
    separator = f"|{'-'*14}|{'-'*14}|{'-'*17}|{'-'*25}|"
    row_files = f"| Files        | {files1:<12} | {files2:<15} | {'-':<25} |"
    row_size  = f"| Total size   | {human_readable(size1):<12} | {human_readable(size2):<15} | {ratio:<25} |"

    return "\n".join([header, separator, row_files, row_size])


def update_readme(readme_path: Path, table_md: str) -> None:
    """
    Insert or update the comparison table between markers in README.
    """
    content = readme_path.read_text(encoding='utf-8')
    pattern = re.compile(
        rf'{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}',
        re.DOTALL
    )
    replacement = f"{MARKER_START}\n{table_md}\n{MARKER_END}"

    if MARKER_START in content and MARKER_END in content:
        new_content = pattern.sub(replacement, content)
    else:
        new_content = content.rstrip() + '\n\n' + replacement + '\n'

    readme_path.write_text(new_content, encoding='utf-8')
    print(f"Updated {readme_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Compare two directories of PNG files: count files, folders, size and update README.md'
    )
    parser.add_argument('dir1', type=Path, help='Path to first directory')
    parser.add_argument('dir2', type=Path, help='Path to second directory')
    parser.add_argument(
        '-o', '--output', type=Path,
        default=Path('README.md'),
        help='README file to update (default: README.md)'
    )
    args = parser.parse_args()

    if not args.dir1.is_dir() or not args.dir2.is_dir():
        print('Error: one of the paths is not a directory', file=sys.stderr)
        sys.exit(1)

    stats1 = get_stats(args.dir1)
    stats2 = get_stats(args.dir2)
    table_md = build_markdown(
        args.dir1.name,
        stats1,
        args.dir2.name,
        stats2
    )

    update_readme(args.output, table_md)


if __name__ == '__main__':
    main()
