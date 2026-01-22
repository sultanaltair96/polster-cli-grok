"""Script to run Dagster with a stable, portable home directory.

This script provides a reliable way to run Dagster operations with proper
environment setup for absolute imports.

Usage:
  python run_dagster.py              # Materialize all assets
  python run_dagster.py --ui         # Materialize + launch Dagster UI
  python run_dagster.py --no-materialize --ui  # Launch UI only
"""

import argparse
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
    """Build environment with proper Dagster and Python path configuration."""
    dagster_home = root / ".dagster"
    dagster_home.mkdir(exist_ok=True)

    env = os.environ.copy()
    env["DAGSTER_HOME"] = str(dagster_home)

    pythonpath = str(root / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = pythonpath + os.pathsep + env["PYTHONPATH"]
    else:
        env["PYTHONPATH"] = pythonpath

    return env


def materialize_assets(root: pathlib.Path, env: dict[str, str]) -> bool:
    """Materialize all assets and return success status."""
    print("[START] Materializing all assets...")
    cmd = [
        "dagster",
        "asset",
        "materialize",
        "-m",
        "orchestration.definitions",
        "--select",
        "*",
    ]
    result = subprocess.call(cmd, cwd=root, env=env)
    if result == 0:
        print("[OK] Assets materialized successfully!")
        return True
    else:
        print("[ERROR] Asset materialization failed!")
        return False


def launch_ui(root: pathlib.Path, env: dict[str, str]):
    """Launch the Dagster development UI."""
    print("[WEB] Launching Dagster UI...")
    print("   Open http://127.0.0.1:3000 in your browser")
    print("   Press Ctrl+C to stop the server")
    try:
        subprocess.call(["dagster", "dev"], cwd=root, env=env)
    except KeyboardInterrupt:
        print("\n👋 Dagster UI stopped.")


def main():
    SCRIPT_PATH = pathlib.Path(__file__).resolve()
    ROOT = find_project_root(SCRIPT_PATH.parent)
    ENV = build_env(ROOT)

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run Dagster operations with proper environment setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_dagster.py              # Materialize all assets
  python run_dagster.py --ui         # Materialize + launch UI
  python run_dagster.py --no-materialize --ui  # Launch UI only
        """,
    )
    parser.add_argument(
        "--ui", action="store_true", help="Launch Dagster UI after operations"
    )
    parser.add_argument(
        "--no-materialize",
        action="store_true",
        help="Skip asset materialization (use with --ui)",
    )
    args = parser.parse_args()

    # Materialize assets unless skipped
    if not args.no_materialize:
        success = materialize_assets(ROOT, ENV)
        if not success and not args.ui:
            sys.exit(1)  # Exit if materialization failed and not launching UI
    else:
        print("⏭️  Skipping asset materialization")

    # Launch UI if requested
    if args.ui:
        launch_ui(ROOT, ENV)
    else:
        print("💡 Tip: Use --ui to launch the Dagster UI after materialization")


if __name__ == "__main__":
    main()
