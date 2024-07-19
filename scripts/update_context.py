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

__doc__ = """Update the cookiecutter context variables."""  # noqa: A001

KAKENHI_LATEX_URL = "http://osksn2.hep.sci.osaka-u.ac.jp/~taku/kakenhiLaTeX/"


class DocumentType:
    """Document type."""

    def __init__(self, zipname: str) -> None:
        """Construct a document type."""
        m = re.match(
            r"(\d{4}[^\"/]*\/[^\"]*)_(utf|sjis|euc)_(single|multi)_(\d+)\.zip",
            zipname,
        )
        if m is None:
            msg = f"unexpected zipname: {zipname}"
            raise ValueError(msg)

        self.prefix = m.group(1)
        self.encoding = m.group(2)
        self.format = m.group(3)
        self.date = m.group(4)
        self.zipname_valid = True

        if self.zipname != zipname:
            msg = f"failed to reconstruct zipname: {zipname}"
            raise ValueError(msg)

    @property
    def zipname(self) -> str:
        """Return the ZIP file name."""
        if not self.zipname_valid:
            msg = "don't have a valid zipname"
            raise ValueError(msg)
        return f"{self.prefix}_{self.encoding}_{self.format}_{self.date}.zip"

    @property
    def name(self) -> str:
        """Return the name."""
        return f"{self.prefix} [{self.date}] ({self.encoding}, {self.format})"

    def join(self, other: DocumentType) -> bool:
        """Try to join another document type."""
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
    """Update the context variables."""
    path = Path(filename)

    input_lines = path.read_text().splitlines()

    output_lines = []

    skipping = False
    inserted = False

    indentation = "  "

    # This code assumes "document_type: [" and "]," are in different lines.
    for line in input_lines:
        if not skipping:
            if "document_type" in line:
                skipping = True
            else:
                output_lines.append(line)
        elif "]," in line:
            skipping = False
            if not inserted:
                inserted = True
                output_lines.append(f'{indentation}"document_type": [')
                for i, dt in enumerate(doc_types):
                    sep = "," if i < len(doc_types) - 1 else ""
                    output_lines.append(f'{indentation * 2}"{dt.name}"{sep}')
                output_lines.append(f"{indentation}],")

    if input_lines != output_lines:
        print(f"update {path}")
        path.write_text("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    text = urlopen(KAKENHI_LATEX_URL).read().decode("utf-8")  # noqa: S310

    document_types: list[DocumentType] = []

    for s in re.findall(
        r"\d{4}[^\"/]*\/[^\"]*_(?:utf|sjis|euc)_(?:single|multi)_\d+\.zip",
        text,
    ):
        dt1 = DocumentType(s)
        for dt in document_types:
            if dt.join(dt1):
                break
        else:
            document_types.append(dt1)

    update_context("cookiecutter.json", document_types)
