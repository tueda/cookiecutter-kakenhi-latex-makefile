#!/bin/sh
""":" .

exec python3 "$0" "$@"
"""


from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path
from typing import Sequence
from urllib.request import urlopen

__doc__ = """Update the cookiecutter context variables."""

KAKENHI_LATEX_URL = "http://osksn2.hep.sci.osaka-u.ac.jp/~taku/kakenhiLaTeX/"


class DocumentType:
    def __init__(self, zipname: str) -> None:
        m = re.match(
            r"(\d{4}[^\"/]*\/[^\"]*)_(utf|sjis|euc)_(single|multi)_(\d+)\.zip", zipname
        )
        if m is None:
            raise ValueError(f"unexpected zipname: {zipname}")

        self.prefix = m.group(1)
        self.encoding = m.group(2)
        self.format = m.group(3)
        self.date = m.group(4)
        self.zipname_valid = True

        if self.zipname != zipname:
            raise ValueError(f"failed to reconstruct zipname: {zipname}")

    @property
    def zipname(self) -> str:
        if not self.zipname_valid:
            raise ValueError("don't have a valid zipname")
        return f"{self.prefix}_{self.encoding}_{self.format}_{self.date}.zip"

    @property
    def name(self) -> str:
        return f"{self.prefix} [{self.date}] ({self.encoding}, {self.format})"

    def join(self, other: DocumentType) -> bool:
        if self.prefix != other.prefix:
            return False
        if self.date != other.date:
            return False

        encoding_list = self.encoding.split("/") + other.encoding.split("/")
        format_list = self.format.split("/") + other.format.split("/")

        encoding_list = list(OrderedDict.fromkeys(encoding_list))
        format_list = list(OrderedDict.fromkeys(format_list))

        self.encoding = "/".join(encoding_list)
        self.format = "/".join(format_list)

        self.zipname_valid = len(encoding_list) == 1 and len(format_list) == 1

        return True


def update_context(filename: str, doc_types: Sequence[DocumentType]) -> None:
    path = Path(filename)

    input_lines = path.read_text().splitlines()

    output_lines = []

    skipping = False
    inserted = False

    # This code assumes "document_type: [" and "]," are in different lines.
    for line in input_lines:
        if not skipping:
            if "document_type" in line:
                skipping = True
            else:
                output_lines.append(line)
        else:
            if "]," in line:
                skipping = False
                if not inserted:
                    inserted = True
                    output_lines.append('    "document_type": [')
                    for i, dt in enumerate(doc_types):
                        if i == len(doc_types) - 1:
                            sep = ""
                        else:
                            sep = ","
                        output_lines.append(f'        "{dt.name}"{sep}')
                    output_lines.append("    ],")

    if input_lines != output_lines:
        print(f"update {path}")
        path.write_text("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    text = urlopen(KAKENHI_LATEX_URL).read().decode("utf-8")

    document_types: list[DocumentType] = []

    for s in re.findall(
        r"\d{4}[^\"/]*\/[^\"]*_(?:utf|sjis|euc)_(?:single|multi)_\d+\.zip", text
    ):
        dt1 = DocumentType(s)
        for dt in document_types:
            if dt.join(dt1):
                break
        else:
            document_types.append(dt1)

    update_context("cookiecutter.json", document_types)
