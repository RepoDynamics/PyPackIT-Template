import pytest


def run(path_root: str = ".", path_config: str = "pyproject.toml") -> int:
    """Run the test-suite."""
    args = [f"--rootdir={path_root}", f"--config-file={path_config}"]
    return pytest.main(args)  # noqa: S603, S607
