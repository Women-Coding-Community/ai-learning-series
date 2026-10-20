"""File tools for the agents. Sandboxed to fixtures/shipit, no path traversal."""
import pathlib
from typing import Callable, Optional

FIXTURE_ROOT = (pathlib.Path(__file__).parent / "fixtures" / "shipit").resolve()


class PathNotAllowed(ValueError):
    """Raised when a path escapes the fixture folder."""


def safe_path(path: str, root: pathlib.Path = FIXTURE_ROOT) -> pathlib.Path:
    """Resolve path inside root, or raise PathNotAllowed (absolute paths and '..' included)."""
    candidate = (root / path).resolve()
    if pathlib.PurePath(path).is_absolute() or not candidate.is_relative_to(root):
        raise PathNotAllowed(f"path is outside the project: {path}")
    return candidate


def read_file(path: str) -> str:
    """Read a project file and return it with line numbers.

    Args:
        path: File path relative to the project root, for example "app/payments.py".
    """
    try:
        target = safe_path(path)
        lines = target.read_text().splitlines()
    except (PathNotAllowed, OSError) as error:
        return f"Error: {error}"
    return "\n".join(f"{number}: {line}" for number, line in enumerate(lines, 1))


def list_files(path: str = ".") -> str:
    """List the files under a project folder, one per line.

    Args:
        path: Folder relative to the project root. Defaults to the root.
    """
    try:
        folder = safe_path(path)
        found = sorted(p.relative_to(FIXTURE_ROOT).as_posix() for p in folder.rglob("*") if p.is_file())
    except (PathNotAllowed, OSError) as error:
        return f"Error: {error}"
    return "\n".join(found)


def make_read_file(allowed: Optional[tuple] = None) -> Callable[[str], str]:
    """Build a read_file tool that can only open the listed files.

    A narrow tool is stronger than a narrow instruction: the specialist cannot
    wander into another file even if it wants to.
    """
    if allowed is None:
        return read_file

    def read_file_narrow(path: str) -> str:
        """Read one of your assigned files and return it with line numbers.

        Args:
            path: File path relative to the project root.
        """
        if path not in allowed:
            return f"Error: you may only read {', '.join(allowed)}"
        return read_file(path)

    read_file_narrow.__name__ = "read_file"
    return read_file_narrow
