cookiecutter-kakenhi-latex-makefile
===================================

[cookiecutter-latex-makefile](https://github.com/tueda/cookiecutter-latex-makefile)
meets
[KAKENHI-LaTeX](http://osksn2.hep.sci.osaka-u.ac.jp/~taku/kakenhiLaTeX/).


Usage
-----

```bash
cookiecutter gh:tueda/cookiecutter-kakenhi-latex-makefile
cd <directory_name>
make
```

The default `.chktexrc` in this template ignores the following warnings:
- All warnings found in the preamble (`-H0`).
- Warning 1: Command terminated with space for `\itshape` (`Silent` section).
    * [TeX - LaTeX Stack Exchange: Why does ChkTeX complain when there is a space after \itshape but not when \bfseries is used?](https://tex.stackexchange.com/q/627808)
- Warning 3: You should enclose the previous parenthesis with '{}' (`-n3`).
    * [TeX - LaTeX Stack Exchange: Why should I "enclose the previous parenthesis with '{}'"?](https://tex.stackexchange.com/a/529940)
- Warning 8: Wrong length of dash may have been used (`-n8`).
    * Jens T. Berger Thielemann, [ChkTEX v1.7.6 (PDF)](http://mirrors.ctan.org/systems/doc/chktex/ChkTeX.pdf), p.15.
      > This is more or less correct, according to my references. One
      > complication is that most often a hyphen (single dash) is
      > desired between letters, but occasionally an n-dash (double
      > dash) is required. This is the case for theorems named after
      > two people e.g. Jordan–Hölder."
- Warning 24: Delete this space to maintain correct pagereferences (`-n24`).
    * [TeX - LaTeX Stack Exchange: When is leading/opening whitespace of a line
      in a tex file important?](https://tex.stackexchange.com/a/264115)
- Warning 38: You should not use punctuation in front of/after quotes (`-n38`).
    * [Debian Bug report logs - #224939: chktex: punctuation in front of quotes](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=224939)
    * [[texhax] chktex: false positives](https://tug.org/pipermail/texhax/2003-December/001423.html)


Font embedding
--------------

If you know how to embed fonts into PDF files via divpdfmx on your system, then use that method.
If this is rather difficult, then I recommend to use the [`pxchfon`](https://github.com/zr-tex8r/PXchfon) package.
For example,
```latex
\usepackage[haranoaji]{pxchfon}
```
Or, you may try [this](https://github.com/tueda/makefile4latex/wiki#embedding-ipaex-fonts) or
[this](https://github.com/tueda/makefile4latex/wiki#embedding-ms-fonts-on-wslcygwin).


Contributing
------------

If you find the "document_type" shown by this project template is not up-to-date,
then please consider opening an issue in the repository (if not yet reported).
Or even better to create a pull request as follows:

1. Fork this repository and clone the forked repository.

2. In the cloned source directory, run `python3 ./scripts/update_context.py`,
   which (hopefully) updates the `document_type` in `cookiecutter.json`.

3. Commit the change with a message like `update document_type (20YY-MM-DD)`.
   Push it and create a pull request.

Of course, other types of suggestions and questions are also welcome.
