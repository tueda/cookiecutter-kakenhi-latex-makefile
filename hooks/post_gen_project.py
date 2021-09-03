import shutil

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

import os
import subprocess

if TYPE_CHECKING:
    from typing import Optional, Sequence

if "which" not in dir(shutil):
    # Simplified implementation of shutil.which for Python < 3.3.
    # https://stackoverflow.com/a/9877856
    def __which(cmd):  # type: (str) -> Optional[str]
        import os

        path = os.getenv("PATH")
        if path is None:
            return None

        for p in path.split(os.path.pathsep):
            p = os.path.join(p, cmd)
            if os.path.exists(p) and os.access(p, os.X_OK):
                return p

        return None

    shutil.which = __which  # type: ignore[assignment]


if shutil.which("git"):
    subprocess.call(["git", "init"])
    for dirpath, dirnames, filenames in os.walk("."):
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
            subprocess.call(["git", "add", "-f", os.path.join(dirpath, f)])
