import os
import os.path
import shutil

from cookiecutter.config import get_user_config
from cookiecutter.zipfile import unzip

raw_doc_type = "{{cookiecutter.document_type}}"

doc_type = raw_doc_type.split(" ")[0]
doc_date = raw_doc_type.split(" ")[1][1:-1]
doc_enc = "{{cookiecutter.character_encoding}}"
doc_fmt = "{{cookiecutter.format_type}}"

use_platex = "{{cookiecutter.latex}}" == "platex"  # type: ignore[comparison-overlap]
use_uplatex = "{{cookiecutter.latex}}" == "uplatex"  # type: ignore[comparison-overlap]

zip_url = f"http://osksn2.hep.sci.osaka-u.ac.jp/~taku/kakenhiLaTeX/{doc_type}_{doc_enc}_{doc_fmt}_{doc_date}.zip"

config_dict = get_user_config()
tempdir = unzip(zip_url, True, config_dict["cookiecutters_dir"])
for f in os.listdir(tempdir):
    src = os.path.join(tempdir, f)
    dest = os.path.join(".", f)
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def comment_out(line, disabled=True):  # type: (str, bool) -> str
    if disabled:
        if line[:1] != "%":
            line = "%" + line
    else:
        if line[:1] == "%":
            line = line[1:]
    return line


def patch_tex_file(filename):  # type: (str) -> None
    with open(filename, "r") as f:
        input_lines = f.read().splitlines()

    output_lines = []
    for line in input_lines:
        if "for platex" in line:
            line = comment_out(line, not use_platex)
        elif "for uplatex" in line:
            line = comment_out(line, not use_uplatex)
        output_lines.append(line)

    if input_lines != output_lines:
        with open(filename, "w") as f:
            f.write("\n".join(output_lines) + "\n")


for f in os.listdir("."):
    if os.path.isfile(f) and f.endswith(".tex"):
        patch_tex_file(f)
