"""Bronze layer example - Data extraction.

This file demonstrates how to extract data and write it to the bronze layer.
Uncomment the example code below to test quickly.
"""

from __future__ import annotations

from datetime import datetime

import polars as pl

from .storage import write_parquet


def extract() -> str:
    """Extract data and write to bronze layer.

    Returns:
        str: Path to the written parquet file.

    Example:
        # Create a simple DataFrame for testing
        df = pl.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [10.5, 20.3, 15.7],
            "created_at": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })

        # Add metadata
        df = df.with_columns(
            pl.lit(datetime.utcnow().isoformat()).alias("fetched_at")
        )

        # Write with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        return write_parquet(df, "bronze", f"bronze_example_{timestamp}.parquet")
    """
    # TODO: Implement your data extraction logic here

    # Example code - uncomment to test:
    # df = pl.DataFrame({
    #     "id": [1, 2, 3],
    #     "name": ["Alice", "Bob", "Charlie"],
    #     "value": [10.5, 20.3, 15.7],
    #     "created_at": ["2024-01-01", "2024-01-02", "2024-01-03"]
    # })
    #
    # df = df.with_columns(
    #     pl.lit(datetime.utcnow().isoformat()).alias("fetched_at")
    # )
    #
    # timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # return write_parquet(df, "bronze", f"bronze_example_{timestamp}.parquet")

    raise NotImplementedError("Implement the extract() function")
