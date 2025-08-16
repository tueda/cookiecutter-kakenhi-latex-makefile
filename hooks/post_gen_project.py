"""Scripts to run after the project generation."""

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # type: ignore[misc]

if TYPE_CHECKING:
    from typing import Optional  # noqa: F401

import os
import shutil
import subprocess

if "which" not in dir(shutil):
    # Simplified implementation of shutil.which() for Python < 3.3.
    # https://stackoverflow.com/a/9877856
    def __which(cmd):
        # type: (str) -> Optional[str]
        path = os.getenv("PATH")
        if path is None:
            return None

        for p in path.split(os.path.pathsep):
            cmd_path = os.path.join(p, cmd)
            if os.path.exists(cmd_path) and os.access(cmd_path, os.X_OK):
                return cmd_path

        return None

    shutil.which = __which  # type: ignore[assignment]


def remove_if(path, cond):
    # type: (str, bool) -> None
    """Remove the file/directory if the condition is met."""
    if cond:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def run_git(*args):
    # type: (*str) -> None
    """Run a Git command with the given arguments."""
    subprocess.call(["git", *args])  # noqa: S603, S607


# Remove the .jinja file extension from all template files.

for path, _, files in os.walk("."):
    for name in files:
        if name.endswith(".jinja"):
            os.rename(
                os.path.join(path, name),
                os.path.join(path, name[: -len(".jinja")]),
            )

# Remove tool-specific config files based on user selection.

use_vscode = "VS Code" in "{{cookiecutter.editor}}"  # noqa: PLR0133
use_latexindent = "latexindent" in "{{cookiecutter.formatter}}"  # noqa: PLR0133
use_chktex = "ChkTeX" in "{{cookiecutter.linter}}"  # noqa: PLR0133

remove_if(".vscode", not use_vscode)
remove_if(".latexindent.yaml", not use_latexindent)
remove_if(".chktexrc", not use_chktex)

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
            run_git("add", "-f", os.path.join(dirpath, f))
    print("Git repository initialized. Files have been staged for commit.")  # noqa: T201
