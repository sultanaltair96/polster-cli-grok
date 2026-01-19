"""Gold example asset."""

from dagster import asset

from ...core.gold_example import aggregate
from ..utils import create_output_with_metadata


@asset(
    group_name="gold",
    description="Gold example asset - data aggregation",
    compute_kind="polars",
)
def run_gold_example():
    """Run gold example aggregation."""
    gold_path = aggregate()
    return create_output_with_metadata(gold_path)
