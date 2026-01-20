"""CLI entry point for Polster."""

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

import typer
from rich import print as rprint
from rich.prompt import Confirm, Prompt

app = typer.Typer(help="Polster CLI - Generate data orchestration projects and assets")


def validate_project_name(name: str) -> str:
    """Validate project name format."""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        raise typer.BadParameter(
            "Project name must start with a letter and contain only letters, numbers, hyphens, and underscores."
        )
    return name


def validate_asset_name(name: str) -> str:
    """Validate asset name (snake_case)."""
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        raise typer.BadParameter(
            "Asset name must be lowercase snake_case (letters, numbers, underscores), "
            "and start with a letter."
        )
    return name


def copy_template_file(
    src: Path, dest: Path, replacements: dict[str, str] | None = None
) -> None:
    """Copy template file with optional string replacements."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    if replacements is None:
        shutil.copy2(src, dest)
        return

    content = src.read_text()
    for key, value in replacements.items():
        content = content.replace(key, value)
    dest.write_text(content)


def ensure_polster_project() -> Path:
    """Ensure we're in a valid Polster project directory."""
    cwd = Path.cwd()

    # Look for src/core and src/orchestration directories
    if (
        not (cwd / "src" / "core").exists()
        or not (cwd / "src" / "orchestration").exists()
    ):
        rprint("[red]Error: Not in a valid Polster project directory.[/red]")
        rprint("Make sure you're in a directory created with 'polster init <name>'.")
        raise typer.Exit(1)

    return cwd


def generate_setup_commands(project_name: str, project_path: Path) -> tuple[str, str]:
    """Generate platform-specific commands for project setup."""
    is_windows = platform.system() == "Windows"

    if is_windows:
        activation_cmd = ".venv\\Scripts\\activate"
        quick_cmd = f"cd ..\\{project_name} && {activation_cmd} && dagster dev"
    else:
        activation_cmd = ".venv/bin/activate"
        quick_cmd = f"cd ../{project_name} && source {activation_cmd} && dagster dev"

    return activation_cmd, quick_cmd


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    """Run a command and return success status."""
    try:
        subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        rprint(f"[red]Command failed: {' '.join(cmd)}[/red]")
        if e.stderr:
            rprint(f"[red]{e.stderr}[/red]")
        return False


def _find_available_port(start_port: int = 3000) -> int:
    """Find an available port starting from start_port."""
    import socket

    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            port += 1
    return start_port  # Fallback to start_port even if potentially taken


def _start_dagster_ui(project_path: Path) -> None:
    """Start Dagster UI in the project directory."""
    port = _find_available_port(3000)

    rprint(f"[green]✓[/green] Starting Dagster UI on port {port}...")
    rprint(f"[blue]🚀[/blue] Dagster UI will be available at: http://localhost:{port}")
    rprint("[dim]Press Ctrl+C to stop...[/dim]")
    rprint()

    # Check if virtual environment exists and find python executable
    venv_python = None

    # Try Unix-style path first
    candidate = project_path / ".venv" / "bin" / "python"
    if candidate.exists():
        # Since we'll be in the project directory, use relative path
        venv_python = Path(".venv/bin/python")
    else:
        # Try Windows-style path
        candidate = project_path / ".venv" / "Scripts" / "python.exe"
        if candidate.exists():
            venv_python = Path(".venv/Scripts/python.exe")

    if venv_python is None:
        rprint(
            "[red]❌ Virtual environment Python not found. Please run the following manually:[/red]"
        )
        rprint(f"  cd {project_path.name}")
        rprint("  source .venv/bin/activate")
        rprint("  dagster dev")
        return
        return

    # Change to project directory
    original_cwd = os.getcwd()
    os.chdir(project_path)

    try:
        # Start Dagster using the project's virtual environment
        # Since we're already in the project directory, just use "run_dagster.py"
        cmd = [str(venv_python), "run_dagster.py", "dev", "--port", str(port)]
        rprint(f"[dim]Running: {' '.join(cmd)}[/dim]")

        subprocess.run(cmd)
    except KeyboardInterrupt:
        rprint("[yellow]⚠[/yellow] Dagster UI stopped")
    except Exception as e:
        rprint(f"[red]❌ Failed to start Dagster: {e}[/red]")
        rprint("[dim]You can start it manually with:[/dim]")
        rprint(f"  cd {project_path.name}")
        rprint("  source .venv/bin/activate")
        rprint("  dagster dev")
    finally:
        # Restore original directory
        os.chdir(original_cwd)


@app.command()
def init(
    project_name: str,
    git: bool = typer.Option(False, "--git", help="Initialize git repository"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git initialization"),
    sample_assets: bool = typer.Option(
        True, "--sample-assets/--no-sample-assets", help="Create sample stub assets"
    ),
    install_uv: bool = typer.Option(
        True, "--install-uv/--no-install-uv", help="Install uv if missing"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be created without creating"
    ),
    start_dagster: bool = typer.Option(
        False, "--start-dagster", help="Start Dagster UI after project creation"
    ),
) -> None:
    """Initialize a new Polster project."""
    rprint(f"[bold]Creating new Polster project: {project_name}[/bold]")

    # Validate project name
    project_name = validate_project_name(project_name)

    # Create project directory in parent folder (next to repo)
    project_path = Path("..") / project_name
    if project_path.exists():
        rprint(
            f"[red]Directory '{project_name}' already exists in parent directory.[/red]"
        )
        raise typer.Exit(1)

    if not dry_run:
        project_path.mkdir()

    # Get template directory
    template_dir = Path(__file__).parent / "templates" / "project"

    if not template_dir.exists():
        rprint("[red]Template directory not found.[/red]")
        raise typer.Exit(1)

    # Copy base template
    def copy_tree(src_dir: Path, dest_dir: Path) -> None:
        skip_dirs = {
            ".ruff_cache",
            "__pycache__",
            ".git",
            ".pytest_cache",
            ".mypy_cache",
        }
        for item in src_dir.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(src_dir)
                if any(part in skip_dirs for part in rel_path.parts):
                    continue
                dest_file = dest_dir / rel_path
                replacements = {"{{PROJECT_NAME}}": project_name}
                if dry_run:
                    rprint(f"Would create: {dest_file}")
                else:
                    copy_template_file(item, dest_file, replacements)

    if dry_run:
        rprint("[bold]Dry run - would create:[/bold]")
    else:
        rprint("[green]✓[/green] Created directory and copied template files")

    copy_tree(template_dir, project_path)

    # Create workspace.yaml for Dagster
    workspace_content = """load_from:
  - python_file: src/orchestration/definitions.py
"""
    workspace_file = project_path / "workspace.yaml"
    if dry_run:
        rprint(f"Would create: {workspace_file}")
    else:
        workspace_file.write_text(workspace_content)
        rprint("[green]✓[/green] Created workspace.yaml for Dagster")

    if not sample_assets and not dry_run:
        # Remove sample assets if not requested
        for asset_file in project_path.glob("src/core/*_example.py"):
            asset_file.unlink()
        for asset_file in project_path.glob("src/orchestration/assets/*/*_example.py"):
            asset_file.unlink()
        rprint("[green]✓[/green] Removed sample assets as requested")

    # Handle git initialization
    init_git = False
    if git:
        init_git = True
    elif no_git:
        init_git = False
    else:
        if not dry_run:
            init_git = Confirm.ask("Initialize git repository?")

    if init_git and not dry_run:
        if run_command(["git", "init"], cwd=project_path):
            rprint("[green]✓[/green] Initialized git repository")
        else:
            rprint("[yellow]⚠[/yellow] Git initialization failed")

    # Handle uv installation
    do_install_uv = False
    if install_uv and not shutil.which("uv") and not dry_run:
        do_install_uv = Confirm.ask("Install uv (Python package installer)?")

    if do_install_uv and not dry_run:
        rprint("Installing uv...")
        # Install uv using the official installer
        if run_command(["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]):
            rprint("[green]✓[/green] Installed uv")
            # Need to update PATH for subprocess to see uv
            os.environ["PATH"] = os.path.expanduser("~/.cargo/bin:") + os.environ.get(
                "PATH", ""
            )
            if not shutil.which("uv"):
                # Try common installation locations
                uv_paths = [
                    Path.home() / ".cargo" / "bin" / "uv",
                    Path.home() / ".local" / "bin" / "uv",
                ]
                for uv_path in uv_paths:
                    if uv_path.exists():
                        os.environ["PATH"] = f"{uv_path.parent}:" + os.environ.get(
                            "PATH", ""
                        )
                        break
        else:
            rprint("[yellow]⚠[/yellow] uv installation failed")

    # Create virtual environment and install dependencies
    if not dry_run:
        rprint("Setting up Python environment...")
        if shutil.which("uv"):
            # Use uv
            if run_command(["uv", "venv"], cwd=project_path):
                rprint("[green]✓[/green] Created virtual environment with uv")

                # Try uv sync first, then fall back to uv pip install
                if run_command(["uv", "sync", "--extra", "dev"], cwd=project_path):
                    rprint("[green]✓[/green] Installed dependencies with uv sync")
                elif run_command(
                    ["uv", "pip", "install", "-e", ".[dev]"], cwd=project_path
                ):
                    rprint("[green]✓[/green] Installed dependencies with uv pip")
                else:
                    rprint("[yellow]⚠[/yellow] Failed to install dependencies with uv")
            else:
                rprint("[yellow]⚠[/yellow] Failed to create virtual environment")
        else:
            # Fallback to python -m venv
            if run_command([sys.executable, "-m", "venv", ".venv"], cwd=project_path):
                rprint("[green]✓[/green] Created virtual environment")

                # Install dependencies
                pip_cmd = (
                    [".venv/bin/pip"]
                    if os.name != "nt"
                    else [".venv\\Scripts\\pip.exe"]
                )
                if run_command(pip_cmd + ["install", "-e", ".[dev]"], cwd=project_path):
                    rprint("[green]✓[/green] Installed dependencies")
                else:
                    rprint("[yellow]⚠[/yellow] Failed to install dependencies")
            else:
                rprint("[yellow]⚠[/yellow] Failed to create virtual environment")

    # Final instructions
    if not dry_run:
        rprint("\n[bold green]✓ Project created successfully![/bold green]")
        rprint(f"📁 Location: ../{project_name}")

        # Check if virtual environment exists and generate commands
        venv_path = project_path / ".venv"
        if venv_path.exists():
            activation_cmd, quick_cmd = generate_setup_commands(
                project_name, project_path
            )
            rprint("\n🚀 Quick start (copy & paste):")
            rprint(f"  {quick_cmd}")
            rprint("\n📝 Or manually:")
            rprint(f"  cd ../{project_name}")
            rprint(f"  source {activation_cmd}")
            rprint("  dagster dev")
        else:
            # Fallback when virtual environment setup failed
            rprint("\nTo get started:")
            rprint(f"  cd ../{project_name}")
            rprint("  # Set up virtual environment and run dagster dev")

        rprint("\nTo add new assets:")
        rprint("  polster add-asset")

        # Start Dagster UI if requested
        if start_dagster:
            _start_dagster_ui(project_path)


@app.command()
def add_asset(
    layer: str = typer.Option(None, "--layer", help="Layer (bronze/silver/gold)"),
    name: str = typer.Option(None, "--name", help="Asset name (lowercase snake_case)"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview files without creating"
    ),
) -> None:
    """Add a new asset to the current Polster project."""
    # Ensure we're in a valid project
    project_path = ensure_polster_project()

    rprint("[bold]Adding new asset to Polster project[/bold]")

    # Handle layer selection
    if layer:
        layer = layer.lower()
        if layer not in ["bronze", "silver", "gold"]:
            rprint("[red]Layer must be one of: bronze, silver, gold[/red]")
            raise typer.Exit(1)
    else:
        layer = Prompt.ask(
            "Which layer?",
            choices=["bronze", "silver", "gold"],
            case_sensitive=False,
        ).lower()

    # Handle asset name
    if name:
        asset_name = validate_asset_name(name)
    else:
        asset_name = Prompt.ask("Asset name (lowercase snake_case)")
        asset_name = validate_asset_name(asset_name)

    # Define file paths
    core_file = project_path / "src" / "core" / f"{layer}_{asset_name}.py"
    orch_file = (
        project_path
        / "src"
        / "orchestration"
        / "assets"
        / layer
        / f"run_{layer}_{asset_name}.py"
    )

    # Check if files already exist
    if core_file.exists() or orch_file.exists():
        rprint("[red]Error: Asset files already exist.[/red]")
        raise typer.Exit(1)

    if dry_run:
        rprint("[bold]Dry run - would create:[/bold]")
        rprint(f"  Core file: {core_file.relative_to(project_path)}")
        rprint(f"  Orchestration file: {orch_file.relative_to(project_path)}")
        return

    # Get template files
    template_dir = Path(__file__).parent / "templates" / "assets"
    core_template = template_dir / f"core_{layer}.py"
    orch_template = template_dir / f"orch_{layer}.py"

    if not core_template.exists() or not orch_template.exists():
        rprint(f"[red]Template files not found for layer: {layer}[/red]")
        raise typer.Exit(1)

    # Create files with replacements
    replacements = {"{{ASSET_NAME}}": asset_name}

    copy_template_file(core_template, core_file, replacements)
    copy_template_file(orch_template, orch_file, replacements)

    asset_function_name = f"run_{layer}_{asset_name}"

    # Update the assets/{layer}/__init__.py to include the new asset
    init_file = (
        project_path / "src" / "orchestration" / "assets" / layer / "__init__.py"
    )
    if init_file.exists():
        content = init_file.read_text()

        # Add import if not already present
        import_block = f"""try:
    from . import {asset_function_name}
except ImportError:
    pass"""
        if f"from . import {asset_function_name}" not in content:
            # Insert before __all__ or at end
            if "__all__" in content:
                content = content.replace("__all__", import_block + "\n\n__all__", 1)
            else:
                content += f"\n{import_block}\n"

        # Update __all__ if it exists
        if "__all__" in content:
            # Find __all__ and add the new name
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("__all__"):
                    # Parse the __all__ list
                    all_start = lines[i].find("[")
                    if all_start != -1:
                        all_end = lines[i].find("]", all_start)
                        if all_end != -1:
                            current_all = lines[i][all_start : all_end + 1]
                            # Add the new name if not present
                            if f'"{asset_function_name}"' not in current_all:
                                # Remove closing ] and add
                                updated_all = (
                                    current_all[:-1]
                                    + f', "{asset_function_name}"'
                                    + current_all[-1:]
                                )
                                lines[i] = lines[i].replace(current_all, updated_all)
                                content = "\n".join(lines) + "\n"
                    break

        init_file.write_text(content)
        rprint(f"[green]✓[/green] Updated: {init_file.relative_to(project_path)}")

    rprint(f"[green]✓[/green] Created core file: {core_file.relative_to(project_path)}")
    rprint(
        f"[green]✓[/green] Created orchestration file: {orch_file.relative_to(project_path)}"
    )

    rprint("\n[bold]Next steps:[/bold]")
    rprint("1. Edit the core file to implement your logic")
    rprint("2. Uncomment the example code to test")
    rprint("3. Run 'dagster dev' to see your asset in the UI")
    rprint(
        f"4. Materialize: 'dagster asset materialize --select run_{layer}_{asset_name}'"
    )


if __name__ == "__main__":
    app()
