# Unified Emoji & Regional Flags Repository

This repository combines all [Noto Emoji](https://github.com/googlefonts/noto-emoji) icons and regional flag SVGs in one place, making it easy to work with both emoji and flags in one unified structure.

## Table of Contents

- [Contents](#contents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Dev](#dev)
  - [Download SVGs](#download-svgs)
  - [Convert to PNG](#convert-to-png)
  - [Optimize PNGs](#optimize-pngs)
- [Saved (png optimization)](#saved-png-optimization)
- [File Naming Convention](#file-naming-convention)
- [CDN Usage](#cdn-usage)
- [Example](#example)
- [License](#license)
  - [Repository Code](#repository-code)
  - [Noto Assets](#noto-assets)
- [Contributing](#contributing)

## Contents

- **download.py**: Download all SVG files from the Noto Emoji repository.
- **convert.py**: Convert downloaded SVGs to raw PNG images.
- **optimizer.py**: Optimize PNG images using a multi-stage pipeline (Pillow, oxipng, zopflipng, pngquant).

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` (or `pipenv`) for dependency management
- System tools: `pngquant`, `zopflipng`

### Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/unified-emoji-flags.git
cd unified-emoji-flags
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Dev

1. **Download SVGs**

```bash
python download.py
```

2. **Convert to PNG**

```bash
python convert.py
```

3. **Optimize PNGs**

```bash
python optimizer.py --input ./raw --output ./png --workers 4
```

Optimized files will be written to `png/` preserving the original folder structure.

## Saved (png optimization)

<!-- DIR-STATS-START -->
| Metric       | raw          | png (opt)       | Size ratio               |
|--------------|--------------|-----------------|-------------------------|
| Files        | 15380        | 15380           | -                         |
| Total size   | 195.96 MB    | 81.64 MB        | 2.40× (240.04%)           |
<!-- DIR-STATS-END -->

## File Naming Convention

When generating filenames for Noto assets, we join Unicode codepoints with underscores (`_`), **excluding** the variation selector U+FE0F (`0xFE0F`).

Example:

```sh
Codepoints: U+1F3C7 U+1F3FD U+200D U+2642
Filename:   emoji_u1f3c7_1f3fd_200d_2642.png
```

See the reference implementation at [strip_vs_from_filenames.py](https://github.com/googlefonts/noto-emoji/blob/main/strip_vs_from_filenames.py).

## CDN Usage

Load emojis and Unicode assets via jsDelivr:

__Sizes__: 32/72/128/512

| Format      | URL Template                                                             | Example                                                              |
|-------------|---------------------------------------------------------------------------|----------------------------------------------------------------------|
| Emoji Char  | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/{size}/{emoji}`     | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/128/%F0%9F%98%8D`  |
| Unicode PNG | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/png/{size}/emoji_u{code}.png` | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/png/128/emoji_u1f60d.png` |
| Unicode SVG | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/svg/emoji_u{code}.svg` | `https://cdn.jsdelivr.net/gh/emoj-info/noto@main/svg/emoji_u1f60d.svg` |

## Example

Inspired by [https://github.com/benborgers/emojicdn](https://github.com/benborgers/emojicdn).

[DEMO 👀](https://codepen.io/dejurin/pen/LEENVNv)

```html
<img src="https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/32/🥳" />
<img src="https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/72/🥳" />
<img src="https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/128/🥳" />
<img src="https://cdn.jsdelivr.net/gh/emoj-info/noto@main/emoji/512/🥳" />
```


## License

### Repository Code

This code is licensed under the MIT License. See [LICENSE](LICENSE.md) for details.

### Noto Assets

All emoji SVGs and font files are provided by the Noto Emoji project and are licensed under the Apache License, Version 2.0. You can review their license here: <https://github.com/googlefonts/noto-emoji/blob/main/LICENSE>.

By including these assets, this repository complies with the original terms of the Apache 2.0 License. Any modifications you make must also comply with Apache 2.0 when redistributing.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your branch and open a pull request

Please follow existing code style and update documentation/tests as needed.

---

<p align="center">Built with ❤️ by <a href="https://emoj.info/">emoj.info</a></p>
