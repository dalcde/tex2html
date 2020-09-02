#!/usr/bin/env python3

import sys, shutil
from pathlib import Path
from tex2html import run

BASE_DIR = Path("/home/dec41/public_html/exp/")
IGNORE = ["geometric_topology"]

options = {
    # Seting css-path prevents Compile.compile from copying style.css to the
    # output directory and instead uses the css specified at this path.
    "css-path": "/exp/style.css",
    # This is where the generated file looks for KaTeX css. By default it gets
    # it from a CDN.
    "katex-css-path": "/includes/katex.min.css",
    # This is a file that loads the Lora and Marcellus SC fonts, generated by https://google-webfonts-helper.herokuapp.com/fonts .
    # By default it gets it from Google directly.
    "font-css-path": "/includes/fonts.css",
}

if not BASE_DIR.is_dir():
    BASE_DIR = Path("/tmp/exp/")
    options = {}

for f in Path("sources").iterdir():
    if f.suffix != ".tex":
        continue

    if f.stem in IGNORE:
        print("Copying " + f.name)
        target_dir = (BASE_DIR / f.stem)
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy("sources/" + f.stem + ".pdf", str(target_dir))
        shutil.copy("sources/" + f.stem + ".tex", str(target_dir))
        continue

    path = BASE_DIR / f.stem

    if (len(sys.argv) > 1 or
          not path.is_dir() or
          not (path / "index.html").is_file() or
          (path / "index.html").stat().st_mtime < f.stat().st_mtime):

        run(f, str(path), options)

shutil.copy("plugin/Renderers/CustomRenderer/style.css", str(BASE_DIR))
