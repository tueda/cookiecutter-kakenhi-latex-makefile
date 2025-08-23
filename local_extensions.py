"""Local extensions."""

from __future__ import annotations

from cookiecutter.utils import simple_filter


@simple_filter  # type: ignore[misc]
def indent_string(indent: str) -> str:
    """Return the appropriate indentation string based on the input."""
    return " " * int(indent.split()[0]) if "spaces" in indent else r"\t"


@simple_filter  # type: ignore[misc]
def indent_editorconfig(indent: str) -> str:
    """Return the appropriate indentation settings string for EditorConfig."""
    if "spaces" in indent:
        n = int(indent.split()[0])
        return f"indent_size = {n}\nindent_style = space"
    return "indent_style = tab"


@simple_filter  # type: ignore[misc]
def indent_vscode(indent: str) -> str:
    """Return the appropriate indentation settings string for VS Code."""
    if "spaces" in indent:
        n = int(indent.split()[0])
        return f'"editor.insertSpaces": true,\n"editor.tabSize": {n}'
    return '"editor.insertSpaces": false'
