"""Silver example asset."""

from dagster import asset, AutomationCondition

from src.core.silver_example import transform
from src.orchestration.utils import create_output_with_metadata


@asset(
    group_name="silver",
    description="Silver example asset - data transformation",
    compute_kind="polars",
    automation_condition=AutomationCondition.eager(),
)
def run_silver_example():
    """Run silver example transformation."""
    silver_path = transform()
    return create_output_with_metadata(silver_path)
