"""Bronze example asset."""

from dagster import asset

from ...core.bronze_example import extract
from ..utils import create_output_with_metadata


@asset(
    group_name="bronze",
    description="Bronze example asset - data extraction",
    compute_kind="polars",
)
def run_bronze_example():
    """Run bronze example extraction."""
    bronze_path = extract()
    return create_output_with_metadata(bronze_path)
