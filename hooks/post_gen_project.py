"""Scripts to run after the project generation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


def remove_if(path: str | Path, cond: bool) -> None:  # noqa: FBT001
    """Remove the file/directory if the condition is met."""
    path = Path(path)
    if cond:
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def run_git(*args: str) -> None:
    """Run a Git command with the given arguments."""
    subprocess.call(["git", *args])  # noqa: S603, S607


def format_json(file: str | Path, indent: str | int = 4) -> None:
    """Format a JSON file."""
    with Path(file).open("r+", encoding="utf-8") as f:
        data = json.load(f)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=indent, sort_keys=True)
        f.truncate()


def reindent_file(file: str | Path, indent: str | int = 4, tabsize: int = 8) -> None:
    """Reindent a file."""
    if isinstance(indent, int):
        indent = " " * indent

    with Path(file).open("r+", encoding="utf-8") as f:
        output_lines = []
        indent_stack = [0]

        for line in f.read().splitlines():
            stripped_line = line.lstrip()
            if not stripped_line:
                output_lines.append("")
                continue

            leading_whitespace = line[: len(line) - len(stripped_line)]
            current_columns = len(leading_whitespace.expandtabs(tabsize))

            while current_columns < indent_stack[-1]:
                indent_stack.pop()

            if current_columns > indent_stack[-1]:
                indent_stack.append(current_columns)

            level = len(indent_stack) - 1

            output_lines.append(indent * level + stripped_line)

        f.seek(0)
        f.write("\n".join(output_lines) + "\n")
        f.truncate()


# Remove the .jinja file extension from all template files.

for path, _, files in os.walk("."):
    for name in files:
        if name.endswith(".jinja"):
            old_path = Path(path) / name
            new_path = Path(path) / name[: -len(".jinja")]
            old_path.rename(new_path)

# User preferences.

use_vscode = "VS Code" in "{{ cookiecutter.editor }}"  # noqa: PLR0133
use_latexindent = "latexindent" in "{{ cookiecutter.formatter }}"  # noqa: PLR0133
use_chktex = "ChkTeX" in "{{ cookiecutter.linter }}"  # noqa: PLR0133
indent = "{{ cookiecutter.indent }}"
indent = " " * int(indent.split()[0]) if "spaces" in indent else "\t"

# Remove tool-specific config files based on user selection.

remove_if(".vscode", not use_vscode)
remove_if(".latexindent.yaml", not use_latexindent)
remove_if(".chktexrc", not use_chktex)

# Run formatters.

if use_vscode:
    format_json(".vscode/settings.json", indent)

if use_chktex:
    reindent_file(".chktexrc", indent)

# Initialize a Git repository and add all files.

if shutil.which("git"):
    run_git("init")
    for dirpath, _dirnames, filenames in os.walk("."):
        if any(name in dirpath for name in (".git", "optional_packages")):
            continue
        for f in filenames:
            if any(
                name in f
                for name in (
                    ".DS_Store",
                    "A_README",
                    "blahblah",
                    "egg",
                    "jack_pub",
                    "seagull",
                )
            ):
                continue
            run_git("add", "-f", str(Path(dirpath) / f))
    print("Git repository initialized. Files have been staged for commit.")  # noqa: T201
