"""Silver layer example - Data transformation.

This file demonstrates how to transform bronze data and write it to the silver layer.
Uncomment the example code below to test quickly.
"""

from __future__ import annotations

from datetime import datetime

import polars as pl

from .storage import read_parquet_latest, write_parquet


def transform() -> str:
    """Transform bronze data and write to silver layer.

    Returns:
        str: Path to the written parquet file.

    Example:
        # Read latest bronze data
        df = read_parquet_latest("bronze", "bronze_example")

        # Apply one transformation (example: convert created_at to date)
        df = df.with_columns(
            pl.col("created_at").str.to_date("%Y-%m-%d").alias("date")
        )

        # Add transformation metadata
        df = df.with_columns(
            pl.lit(datetime.utcnow().isoformat()).alias("transformed_at")
        )

        # Write with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        return write_parquet(df, "silver", f"silver_example_{timestamp}.parquet")
    """
    # TODO: Implement your data transformation logic here

    # Example code - uncomment to test (requires bronze data):
    # df = read_parquet_latest("bronze", "bronze_example")
    #
    # df = df.with_columns(
    #     pl.col("created_at").str.to_date("%Y-%m-%d").alias("date")
    # )
    #
    # df = df.with_columns(
    #     pl.lit(datetime.utcnow().isoformat()).alias("transformed_at")
    # )
    #
    # timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # return write_parquet(df, "silver", f"silver_example_{timestamp}.parquet")

    raise NotImplementedError("Implement the transform() function")
