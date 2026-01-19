"""Gold layer example - Data aggregation.

This file demonstrates how to aggregate silver data and write it to the gold layer.
"""

from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

try:
    # Try relative imports (when run as module through Dagster)
    from .paths import PROJECT_ROOT, DATA_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR
    from .storage import read_parquet_latest, write_parquet
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    import os

    # Add src directory to path for absolute imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from core.paths import PROJECT_ROOT, DATA_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR
    from core.storage import read_parquet_latest, write_parquet


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
