"""Gold layer example - Data aggregation.

This file demonstrates how to aggregate silver data and write it to the gold layer.
"""

from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

from .storage import read_parquet_latest, write_parquet


def aggregate() -> str:
    """Aggregate silver data and write to gold layer.

    Returns:
        str: Path to the written parquet file.
    """
    # Read latest silver orders data
    df = read_parquet_latest("silver", "silver_orders_")

    # Simple aggregation: total sales and order count by status
    result = (
        df.group_by("status")
        .agg(
            total_sales=pl.col("total_amount").sum().round(2),
            order_count=pl.len(),
            avg_order_value=(pl.col("total_amount").sum() / pl.len()).round(2),
        )
        .sort("total_sales", descending=True)
    )

    # Add aggregation timestamp
    aggregate_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result = result.with_columns(pl.lit(aggregate_time).alias("aggregated_at"))

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return write_parquet(result, "gold", f"gold_order_summary_{timestamp}.parquet")


if __name__ == "__main__":
    aggregate()
