#!/usr/bin/env python3

import argparse

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent / "plastex"))
sys.path.insert(0, str(Path(__file__).absolute().parent / "overrides"))

import os, shutil
from distutils.dir_util import copy_tree, mkpath
from tempfile import TemporaryDirectory

import plastex_patch
from plasTeX.Compile import run as run_
from plasTeX.Config import config as config_base
from CustomRenderer.Config import config as config_extra

from plasTeX import TeXDocument
# Remove this charsub because it breaks search
TeXDocument.charsubs = [x for x in TeXDocument.charsubs if x[0] != "'"]


def rm_tree(d):
    for f in os.listdir(d):
        f = os.path.join(d, f)
        if os.path.isfile(f) or os.path.islink(f):
            os.unlink(f)
        else:
            shutil.rmtree(f)

def run(f: Path, target_dir: str, options={}):
    f = f.absolute() # We will later change directories
    source_dir = f.parent

    if f.suffix != ".tex":
        raise ValueError("{} does not have extension .tex".format(f))

    print("Compiling {}".format(f.name))

    renderer = str(Path("CustomRenderer").absolute())

    cwd = Path.cwd()
    os.chdir(str(source_dir))

    with TemporaryDirectory() as tmp_dir:
        config = config_base.copy() + config_extra

        config.set("images", "imager", "gspdfpng")
        config.set("images", "vector-imager", "pdf2svg")
        config.set("images", "scale-factor", 1.4)
        config.set("general", "renderer", renderer)
        config.set("files", "directory", tmp_dir)
        config.set("document", "disable-charsub", "'")

        for key, value in options.items():
            config.set("custom", key, value)

        run_(f.name, config)

        mkpath(target_dir)
        rm_tree(target_dir)
        copy_tree(tmp_dir, target_dir)
        shutil.copy(f.name, target_dir)
        try:
            shutil.copy(f.stem + ".pdf", target_dir)
        except OSError:
            pass

        try:
            os.remove(f.stem + ".paux")
        except OSError:
            pass

    os.chdir(str(cwd))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform tex files into pdf")
    parser.add_argument("file", type=str, help='tex file to process')
    parser.add_argument("output_dir", type=str, help='output directory')

    args = parser.parse_args()
    run(Path(args.file), args.output_dir)
