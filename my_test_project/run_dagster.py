"""Dagster runner for my_test_project."""

import os
import sys

if __name__ == "__main__":
    # Set DAGSTER_HOME to project-local directory
    os.environ["DAGSTER_HOME"] = os.path.join(os.getcwd(), ".dagster")

    # Run Dagster with default command line arguments
    from dagster import cli

    sys.argv[0] = "dagster"  # Make dagster think it's being called normally
    cli.main()