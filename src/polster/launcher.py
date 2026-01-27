"""
Polster CLI Launcher - Automatic Virtual Environment Management

This launcher automatically detects and activates the project's virtual environment
before running the actual CLI commands.
"""

import os
import subprocess
import sys
from pathlib import Path


def find_project_root(start_path: Path | None = None) -> Path:
    """Find the polster project root by searching for pyproject.toml."""
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Search up the directory tree for pyproject.toml (works for both dev and generated projects)
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent

    raise FileNotFoundError("Could not find polster project root. Are you in a polster project directory?")


def create_venv(venv_path: Path) -> None:
    """Create a virtual environment at the specified path."""
    print(f"Creating virtual environment in {venv_path}")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)


def install_package_in_venv(venv_path: Path, project_root: Path) -> None:
    """Install the polster package in editable mode within the venv."""
    if os.name == "nt":  # Windows
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:  # Unix
        pip_path = venv_path / "bin" / "pip"

    print("Installing polster in virtual environment...")
    subprocess.run([str(pip_path), "install", "-e", str(project_root)], check=True)


def activate_venv_and_run(venv_path: Path, args: list[str]) -> None:
    """Activate the virtual environment and run the polster CLI."""
    if os.name == "nt":  # Windows
        # On Windows, we need to set environment variables
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(venv_path)
        env["PATH"] = str(venv_path / "Scripts") + os.pathsep + env.get("PATH", "")
        # Run the actual CLI
        from polster.cli import app
        # Remove 'polster' from args if present
        if args and args[0].endswith("polster"):
            args = args[1:]
        app(args=args)
    else:  # Unix
        # On Unix, set environment variables for activation
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(venv_path)
        env["PATH"] = str(venv_path / "bin") + os.pathsep + env.get("PATH", "")

        # Run the actual CLI
        from polster.cli import app
        if args and args[0].endswith("polster"):
            args = args[1:]
        app(args=args)


def is_development_environment(project_root: Path) -> bool:
    """Check if we're running from the development repository."""
    return (project_root / "src" / "polster" / "launcher.py").exists() and \
           (project_root / "src" / "polster" / "cli.py").exists()


def main() -> None:
    """Main entry point that handles venv auto-activation."""
    try:
        # Check if this is an init command (doesn't need existing project)
        args = sys.argv
        if len(args) >= 2 and args[1] == "init":
            # For init command, run directly without venv activation
            from polster.cli import app
            app(args=args[1:])  # Remove 'polster' from args
            return

        # For all other commands, find project and activate venv
        project_root = find_project_root()

        # Check if we're in the development environment
        if is_development_environment(project_root):
            # In development, run CLI directly without venv
            from polster.cli import app
            if args and args[0].endswith("polster"):
                args = args[1:]  # Remove 'polster' from args
            app(args=args)
            return

        # For generated projects, use venv activation
        venv_path = project_root / ".venv"

        # Check if venv exists
        if not venv_path.exists():
            print("Virtual environment not found. Creating one...")
            create_venv(venv_path)
            install_package_in_venv(venv_path, project_root)

        # Activate venv and run CLI
        activate_venv_and_run(venv_path, sys.argv)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure you're in a polster project directory.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during virtual environment setup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
