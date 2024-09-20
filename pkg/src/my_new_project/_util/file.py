"""Utility functions for file operations."""

from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import pkgdata as _pkgdata

if _TYPE_CHECKING:
    from pathlib import Path


def get_internal_filepath(relative_path: str) -> Path:
    """Get the absolute path to a file included in the package.

    Parameters
    ----------
    relative_path
        Path to the file relative to the package's root directory.
    """
    package_path = _pkgdata.get_package_path_from_caller()
    return package_path / relative_path
