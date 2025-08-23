"""Script to run before the template process."""

from __future__ import annotations

import shutil
from pathlib import Path

from cookiecutter.config import get_user_config
from cookiecutter.zipfile import unzip

raw_doc_type = "{{cookiecutter.document_type}}"

doc_type = raw_doc_type.split(" ")[0]
doc_date = raw_doc_type.split(" ")[1][1:-1]
doc_enc = "{{cookiecutter.character_encoding}}"
doc_fmt = "{{cookiecutter.format_type}}"

use_platex = "{{cookiecutter.latex}}" == "platex"  # type: ignore[comparison-overlap]  # noqa: PLR0133
use_uplatex = "{{cookiecutter.latex}}" == "uplatex"  # type: ignore[comparison-overlap]  # noqa: PLR0133

zip_url = f"http://osksn2.hep.sci.osaka-u.ac.jp/~taku/kakenhiLaTeX/{doc_type}_{doc_enc}_{doc_fmt}_{doc_date}.zip"

config_dict = get_user_config()
tempdir = unzip(zip_url, is_url=True, clone_to_dir=config_dict["cookiecutters_dir"])
for f in Path(tempdir).iterdir():
    src = Path(tempdir) / f
    dest = Path(f)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def comment_out(line: str, disabled: bool = True) -> str:  # noqa: FBT001, FBT002
    """Comment out or uncomment the given line."""
    if disabled:
        if line[:1] != "%":
            line = "%" + line
    else:  # noqa: PLR5501
        if line[:1] == "%":
            line = line[1:]
    return line


def patch_tex_file(file: str | Path) -> None:
    """Patch the TeX file."""
    path = Path(file)
    with path.open() as f:
        input_lines = f.read().splitlines()

    output_lines = []
    for line in input_lines:
        if "for platex" in line:
            new_line = comment_out(line, not use_platex)
        elif "for uplatex" in line:
            new_line = comment_out(line, not use_uplatex)
        elif "only for demonstration" in line and "egg" not in path.name:
            new_line = comment_out(line)
        else:
            new_line = line
        output_lines.append(new_line)

    if input_lines != output_lines:
        with path.open("w") as f:
            f.write("\n".join(output_lines) + "\n")


for f in Path().iterdir():
    if f.is_file() and f.name.endswith(".tex"):
        patch_tex_file(f)
