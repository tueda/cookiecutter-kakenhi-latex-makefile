"""Scripts to run after generating the project root directory."""

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Optional, Sequence  # noqa: F401

import os
import shutil
import subprocess

if "which" not in dir(shutil):
    # Simplified implementation of shutil.which for Python < 3.3.
    # https://stackoverflow.com/a/9877856
    def __which(cmd):
        # type: (str) -> Optional[str]
        import os

        path = os.getenv("PATH")
        if path is None:
            return None

        for p in path.split(os.path.pathsep):
            p = os.path.join(p, cmd)  # noqa: PLW2901
            if os.path.exists(p) and os.access(p, os.X_OK):
                return p

        return None

    shutil.which = __which  # type: ignore[assignment]


def run_git(*args):
    # type: (str) -> None
    """Run the Git command."""
    subprocess.call(["git", *args])  # noqa: S603, S607


if shutil.which("git"):
    run_git("init")
    for dirpath, _dirnames, filenames in os.walk("."):
        if ".git" in dirpath:
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
