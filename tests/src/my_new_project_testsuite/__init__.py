import pytest


def run(path_root: str = ".", path_config: str = "pyproject.toml") -> int:
    """Run the test-suite.

    Parameters
    ----------
    path_root
        Path to the root directory.
    path_config
        Path to the PyTest configuration file.
    """
    args = [f"--rootdir={path_root}", f"--config-file={path_config}"]
    return pytest.main(args)
