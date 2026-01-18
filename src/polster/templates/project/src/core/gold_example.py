"""Gold layer example - Data aggregation.

This file demonstrates how to aggregate silver data and write it to the gold layer.
Uncomment the example code below to test quickly.
"""

from __future__ import annotations

from datetime import datetime

import polars as pl

from core.storage import read_parquet_latest, write_parquet


def aggregate() -> str:
    """Aggregate silver data and write to gold layer.

    Returns:
        str: Path to the written parquet file.

    Example:
        # Read latest silver data
        df = read_parquet_latest("silver", "silver_example")

        # Apply one aggregation (example: total value by date)
        result = df.group_by("date").agg(
            total_value=pl.col("value").sum(),
            record_count=pl.len()
        ).sort("date")

        # Add aggregation metadata
        result = result.with_columns(
            pl.lit(datetime.utcnow().isoformat()).alias("aggregated_at")
        )

        # Write with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        return write_parquet(result, "gold", f"gold_example_{timestamp}.parquet")
    """
    # TODO: Implement your data aggregation logic here

    # Example code - uncomment to test (requires silver data):
    # df = read_parquet_latest("silver", "silver_example")
    #
    # result = df.group_by("date").agg(
    #     total_value=pl.col("value").sum(),
    #     record_count=pl.len()
    # ).sort("date")
    #
    # result = result.with_columns(
    #     pl.lit(datetime.utcnow().isoformat()).alias("aggregated_at")
    # )
    #
    # timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # return write_parquet(result, "gold", f"gold_example_{timestamp}.parquet")

    raise NotImplementedError("Implement the aggregate() function")