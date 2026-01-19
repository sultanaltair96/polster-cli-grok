"""Silver layer example - Data transformation.

This file demonstrates how to transform bronze data and write it to the silver layer.
"""

from __future__ import annotations

from datetime import datetime, timezone

import polars as pl

from .storage import read_parquet_latest, write_parquet


def transform() -> str:
    """Transform bronze data and write to silver layer.

    Returns:
        str: Path to the written parquet file.
    """
    orders_df = read_parquet_latest("bronze", "bronze_orders_")
    payments_df = read_parquet_latest("bronze", "bronze_payments_")

    joined = orders_df.join(payments_df, on="order_id", how="left")

    cleaned = joined.with_columns(
        [
            pl.col("order_date").cast(pl.Datetime),
            pl.col("total_amount").cast(pl.Float64).round(2),
            pl.col("paid_amount").cast(pl.Float64).fill_null(0.0).round(2),
            (pl.col("payment_status") == "paid").alias("is_paid"),
        ]
    ).with_columns(pl.col("order_date").dt.date().alias("order_day"))

    transform_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cleaned = cleaned.with_columns(pl.lit(transform_time).alias("transformed_at"))

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return write_parquet(cleaned, "silver", f"silver_orders_{timestamp}.parquet")


if __name__ == "__main__":
    transform()
