"""Script to run Dagster with a stable, portable home directory."""

import os
import pathlib
import subprocess
import sys


def find_project_root(start: pathlib.Path) -> pathlib.Path:
    """Walk up directories until a pyproject.toml is found."""
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise FileNotFoundError("pyproject.toml not found above run_dagster.py")


def build_env(root: pathlib.Path) -> dict[str, str]:
    dagster_home = root / ".dagster"
    dagster_home.mkdir(exist_ok=True)

    env = os.environ.copy()
    env["DAGSTER_HOME"] = str(dagster_home)

    pythonpath = str(root / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = pythonpath + ":" + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = pythonpath

    return env


SCRIPT_PATH = pathlib.Path(__file__).resolve()
ROOT = find_project_root(SCRIPT_PATH.parent)
ENV = build_env(ROOT)

cmd = [
    "dagster",
    "asset",
    "materialize",
    "-m",
    "orchestration.definitions",
    "--select",
    "*",
]
sys.exit(subprocess.call(cmd, cwd=ROOT, env=ENV))
