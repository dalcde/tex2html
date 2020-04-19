# About
This repository contains the customizations and scripts I use to convert
`latex` to `html` via `plastex`. The main pieces of code are

 - A plastex renderer in `CustomRenderer/`. This is based on the `HTML5`
   renderer.
 - Custom package implementations in `overrides/`.
 - A plastex patch in `overrides/plastex_patch.py`.

See [here](http://dec41.user.srcf.net/exp/global_analysis/index.html) for an
example output.

To turn a tex file into html, run
```console
 $ ./tex2html.py [source.tex] [target directory]
```
If `source.pdf` is present, it will be copied to the target directory as well.
Note that the command removes everything in the target directory.

The script `./compile_srcf.py` is the script I use on my webserver to compile
multiple tex files with some extra configuration.

# Custom Renderer
The main output differences from the `HTML5` renderer are

 - This uses KaTeX to render the math, and rendering is performed server side.
   As a consequence, the resulting HTML file does not use any javascript.

   A vendered copy of KaTeX is found at `CustomRenderer/katex.min.js`. The
   current version is 0.11.1. The latest version can be found at
   [https://github.com/Khan/KaTeX](https://github.com/Khan/KaTeX)

 - Styling differences:
   - A custom css stylesheet is used
   - The page template is completely different and is found at
     `CustomRenderer/layout.jinja2`.
   - Some macros have different templates. They can be found at
     `CustomRenderer/Templates/`. The unspecified macros use the `HTML5`
     templates.

## To do
 - Support multiple authors
 - Booktabs
 - Proper \fakeqed/\qedhere when ending a proof with an equation
 - KaTeX tag leaves page
 - Table of contents number alignment
 - cite brackets - use nbsp
 - Style bibliography properly

# Dependencies
On top of the plastex dependencies (see `plastex/requirements.txt`), this
requires `pyduktape` for math rendering.

# plastex.sty
Included in the root directory is a LaTeX package `plastex.sty`. This package
has some helper commands and environments:

## The `useimager` environment
Everything in the `useimager` environment will be compiled with LaTeX and then
rendered into SVG. This can be used for parts of the document that cannot be
handled by plastex (yet). The imager is already automatically used for
`tikzpicture`, hence this doesn't have to be wrapped in `useimager.

## \ifplastex
The package defines a new variable `\ifplastex`. This can be used as follows:
```latex
\ifplastex
  % commands to be run when processed by plastex
\else
  % commands to be run when processed by a usual tex engine
\fi
```
## \tph
A version of `\texorpdfstring` that now has three arguments, where the third
argument is what plastex should use.
