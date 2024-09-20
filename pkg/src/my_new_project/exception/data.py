"""Exceptions raised by the data module."""

from typing import TYPE_CHECKING as _TYPE_CHECKING

from my_new_project.exception import PackageException as _PackageException

if _TYPE_CHECKING:
    from pathlib import Path


class DataFileNotFoundError(_PackageException):
    """Raised when a requested package data file is not found."""
    def __init__(
        self,
        path_relative: Path,
        path_absolute: Path,
    ):
        """
        Parameters
        ----------
        path_relative
            Path to the file relative to the package's data directory.
        path_absolute
            Absolute path to the file.
        """
        self.path_relative = path_relative
        self.path_absolute = path_absolute
        super().__init__(
            "Could not find the requested package data file "
            f"'{path_relative}' at '{path_absolute}'.",
        )
        return