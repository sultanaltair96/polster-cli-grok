"""Dagster runner for {{PROJECT_NAME}}."""

import os
import sys

if __name__ == "__main__":
    # Add src directory to Python path for proper imports
    src_path = os.path.join(os.getcwd(), "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Set DAGSTER_HOME to project-local directory
    dagster_home = os.path.join(os.getcwd(), ".dagster")
    os.environ["DAGSTER_HOME"] = dagster_home

    # Ensure DAGSTER_HOME directory exists
    os.makedirs(dagster_home, exist_ok=True)

    # Run Dagster with default command line arguments
    from dagster import cli

    sys.argv[0] = "dagster"  # Make dagster think it's being called normally
    cli.main()
