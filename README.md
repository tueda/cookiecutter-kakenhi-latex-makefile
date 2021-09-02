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


Font embedding
--------------

If you know how to embed fonts into PDF files via divpdfmx on your system, then use that method.
If this is rather difficult, then we recommend to use the [`pxchfon`](https://github.com/zr-tex8r/PXchfon) package.
Or, you may try [this](https://github.com/tueda/makefile4latex/wiki#embedding-ipaex-fonts) or
[this](https://github.com/tueda/makefile4latex/wiki#embedding-ms-fonts-on-wslcygwin).
