#!/usr/bin/env python3
import sys
from pathlib import Path
import cairosvg

# Input directory with SVG files
INPUT_DIR = Path('svg')
# Root output directory; inside will be folders with sizes
OUTPUT_ROOT = Path('raw')
# Sizes for generation
SIZES = [32, 72, 128, 512]

def load_svg_bytes(svg_path: Path) -> bytes:
    """
    Load SVG bytes; if file content is a reference to another .svg,
    load bytes from that target instead.
    """
    text = svg_path.read_text(encoding='utf-8').strip()
    # If content is not XML and ends with ".svg", treat it as alias
    if not text.lstrip().startswith('<') and text.lower().endswith('.svg'):
        target = INPUT_DIR / text
        if not target.exists():
            print(f"Warning: alias target not found {text}", file=sys.stderr)
            return b''
        return target.read_bytes()
    # Otherwise return original SVG bytes
    return svg_path.read_bytes()

def convert_svg(svg_path: Path) -> None:
    """Convert one SVG (or its alias target) into PNGs at all specified sizes."""
    svg_data = load_svg_bytes(svg_path)
    if not svg_data:
        return

    stem = svg_path.stem  # without extension
    for size in SIZES:
        out_dir = OUTPUT_ROOT / str(size)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{stem}.png"
        # render PNG
        cairosvg.svg2png(
            bytestring=svg_data,
            write_to=str(out_file),
            output_width=size,
            output_height=size,
        )
        print(f"Saved: {out_file}")

def main() -> None:
    if not INPUT_DIR.is_dir():
        print(f"Error: folder {INPUT_DIR} not found", file=sys.stderr)
        sys.exit(1)

    svg_files = list(INPUT_DIR.glob('*.svg'))
    if not svg_files:
        print(f"No SVG files found in {INPUT_DIR}", file=sys.stderr)
        sys.exit(0)

    for svg in svg_files:
        try:
            convert_svg(svg)
        except Exception as e:
            print(f"Error processing {svg.name}: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
