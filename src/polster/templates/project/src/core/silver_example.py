"""Silver layer example - Data transformation.

This file demonstrates how to transform bronze data and write it to the silver layer.
"""

from __future__ import annotations

from datetime import datetime

import polars as pl

try:
    # Try relative imports (when run as module through Dagster)
    from .storage import read_parquet_latest, write_parquet
except ImportError:
    # Fall back to absolute imports (when run directly)
    import os
    import sys

    # Add src directory to path for absolute imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from core.storage import read_parquet_latest, write_parquet


def transform() -> str:
    """Transform bronze data and write to silver layer.

    Returns:
        str: Path to the written parquet file.
    """
    # Read latest bronze orders data
    df = read_parquet_latest("bronze", "bronze_orders_")

    # Simple transformation: filter out cancelled orders and standardize data types
    cleaned = (
        df.filter(pl.col("status") != "cancelled")
        .with_columns(
            [
                pl.col("order_date").cast(pl.Datetime),
                pl.col("total_amount").cast(pl.Float64).round(2),
            ]
        )
        .with_columns(pl.col("order_date").dt.date().alias("order_day"))
    )

    # Add transformation timestamp
    transform_time = datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
    cleaned = cleaned.with_columns(pl.lit(transform_time).alias("transformed_at"))

    timestamp = datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    return write_parquet(cleaned, "silver", f"silver_orders_{timestamp}.parquet")


if __name__ == "__main__":
    transform()
