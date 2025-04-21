#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
from PIL import Image
import oxipng
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed


def strip_metadata_and_optimize_with_pillow(src: str, dst: str) -> None:
    """Remove all metadata and optimize PNG using Pillow."""
    with Image.open(src) as img:
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))
        clean.save(dst, format="PNG", optimize=True, compress_level=9)


def optimize_with_oxipng(src: str, dst: str) -> None:
    """Optimize PNG using oxipng (Rust-based)."""
    oxipng.optimize(src, dst)


def optimize_with_zopflipng(src: str, dst: str) -> None:
    """Optimize PNG using zopflipng (lossless)."""
    if not shutil.which("zopflipng"):
        print("Warning: zopflipng not found, skipping zopflipng", file=sys.stderr)
        return
    subprocess.run([
        "zopflipng",
        "-y",
        "--iterations=15",
        src,
        dst
    ], check=True)


def get_color_count(path: str) -> int:
    """Count unique colors in image data."""
    with Image.open(path) as img:
        return len(set(img.getdata()))


def quantize_with_pngquant(path: str) -> None:
    """Quantize PNG using pngquant, clamping color count to [2..256]."""
    if not shutil.which("pngquant"):
        print("Warning: pngquant not found, skipping quantization", file=sys.stderr)
        return
    orig_colors = get_color_count(path)
    n_colors = max(2, min(orig_colors, 256))
    if orig_colors != n_colors:
        print(f"Clamping color count from {orig_colors} to {n_colors}", file=sys.stderr)
    subprocess.run([
        "pngquant",
        f"--colors={n_colors}",
        "--skip-if-larger",
        "--force",
        "--output", path,
        path
    ], check=True)


def process_file(src_path: str, dst_dir: str) -> None:
    """Run full optimization pipeline on a single file, saving into dst_dir."""
    filename = os.path.basename(src_path)
    name, _ = os.path.splitext(filename)
    dst = os.path.join(dst_dir, filename)
    tmp1 = os.path.join(dst_dir, f"{name}_tmp.png")
    tmp2 = os.path.join(dst_dir, f"{name}_tmp2.png")

    print(f"Processing {src_path} -> {dst}")
    strip_metadata_and_optimize_with_pillow(src_path, tmp1)
    optimize_with_oxipng(tmp1, tmp2)
    shutil.move(tmp2, dst)
    optimize_with_zopflipng(dst, tmp1)
    shutil.move(tmp1, dst)
    quantize_with_pngquant(dst)

    # cleanup temporary files
    for f in (tmp1, tmp2):
        if os.path.exists(f):
            os.remove(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively optimize PNGs, preserving folder structure.")
    parser.add_argument(
        "--input", "-i", dest="input_dir", required=True,
        help="Path to input folder (e.g. png_output)")
    parser.add_argument(
        "--output", "-o", dest="output_dir", required=True,
        help="Path to output folder (e.g. png)")
    parser.add_argument(
        "--workers", "-w", dest="workers", type=int,
        default=os.cpu_count(),
        help="Number of parallel workers (default: CPU count)")
    args = parser.parse_args()
    input_dir = args.input_dir.rstrip(os.sep)
    output_dir = args.output_dir.rstrip(os.sep)

    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Gather all PNG files recursively
    tasks = []  # tuples of (src_path, dst_subdir)
    for root, _, files in os.walk(input_dir):
        rel = os.path.relpath(root, input_dir)
        dst_subdir = os.path.join(output_dir, rel)
        os.makedirs(dst_subdir, exist_ok=True)
        for fname in files:
            if fname.lower().endswith(".png"):
                src_path = os.path.join(root, fname)
                tasks.append((src_path, dst_subdir))

    if not tasks:
        print("No PNG files found in", input_dir)
        return

    # Parallel processing
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_file, src, dst): (src, dst)
            for src, dst in tasks
        }
        for future in as_completed(futures):
            src, dst = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {src} -> {dst}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
