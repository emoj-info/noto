#!/usr/bin/env python3
from pathlib import Path

# Paths to input SVGs and one of the PNG size folders
SVG_DIR = Path('svg')
PNG_DIR = Path('raw') / '32'  # any of [32,72,128,512]

def find_missing() -> set[str]:
    """Return set of SVG stems that have no corresponding PNG."""
    svg_stems = {p.stem for p in SVG_DIR.glob('*.svg')}
    png_stems = {p.stem for p in PNG_DIR.glob('*.png')}
    return svg_stems - png_stems

def main() -> None:
    missing = find_missing()
    if not missing:
        print("All SVGs converted successfully.")
    else:
        print(f"Missing {len(missing)} files:")
        for name in sorted(missing):
            print(name + '.svg')

if __name__ == '__main__':
    main()
