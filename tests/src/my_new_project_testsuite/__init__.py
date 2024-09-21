"""My New Project Test-Suite.

Copyright (C) 2024 RepoDynamics

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tempfile
from pathlib import Path

import pkgdata
import pytest


def run(
    pyargs: list[str] | None = None,
    args: list[str] | None = None,
    overrides: dict[str, str] | None = None,
    path_cache: str | Path | None = None,
    path_report: str | Path | None = None,
    template_start: str = "$|| ",
    template_end: str = " ||",
) -> int:
    """Run the test-suite.

    Parameters
    ----------
    path_root
        Path to the root directory.
    path_config
        Path to the PyTest configuration file.
    """
    path_root = pkgdata.get_package_path_from_caller(top_level=True).resolve()
    path_config = path_root / "data" / "config"
    path_pytest_config = None
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        path_config_temp = temp_dir_path / "config"
        path_cache = Path(path_cache) if path_cache else temp_dir_path / "cache"
        path_report = Path(path_report) if path_report else temp_dir_path / "report"
        for path in (path_config_temp, path_cache, path_report):
            path.mkdir(parents=True, exist_ok=True)
        for path in path_config.iterdir():
            if not path.is_file():
                continue
            (path_cache / path.stem).mkdir(exist_ok=True)
            (path_report / path.stem).mkdir(exist_ok=True)
            config = path.read_text()
            for template, value in (
                (f"{template_start}{template_name}{template_end}", template_value)
                for template_name, template_value in (
                    ("path_config", path_config_temp),
                    ("path_report", path_report),
                    ("path_cache", path_cache),
                )
            ):
                config = config.replace(template, str(value))
            file_temp_path = path_config_temp / path.name
            file_temp_path.write_text(config)
            if path.stem == "pytest":
                path_pytest_config = file_temp_path
        final_args = [f"--rootdir={path_root}"]
        if path_pytest_config:
            final_args.append(f"--config-file={path_pytest_config}")
        if args:
            final_args.extend(args)
        if overrides:
            for key, value in overrides.items():
                # https://docs.pytest.org/en/stable/reference/reference.html#configuration-options
                final_args.extend(["--override-ini", f"{key}={value}"])
        pyargs = pyargs or [pkgdata.get_package_name_from_caller(top_level=True)]
        final_args.extend(["--pyargs", *pyargs])
        print(final_args)
        return pytest.main(final_args)
