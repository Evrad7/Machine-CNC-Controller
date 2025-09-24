"""Utilities for accessing packaged application resources."""
from __future__ import annotations

from pathlib import Path
from typing import Final


_PACKAGE_ROOT: Final[Path] = Path(__file__).resolve().parent
_PROJECT_ROOT: Final[Path] = _PACKAGE_ROOT.parent
IMAGES_DIR: Final[Path] = _PROJECT_ROOT / "images"
UI_DIR: Final[Path] = _PROJECT_ROOT / "resources" / "ui"


def image_path(name: str) -> str:
    """Return the filesystem path to an image asset.

    Parameters
    ----------
    name:
        File name located in the :mod:`images` directory.
    """
    return str(IMAGES_DIR / name)


def ui_path(name: str) -> Path:
    """Return the filesystem path to a Qt Designer `.ui` file."""

    return UI_DIR / name
