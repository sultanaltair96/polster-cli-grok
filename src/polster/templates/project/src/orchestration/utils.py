"""Shared utilities for Dagster orchestration."""

from dagster import Output, MetadataValue
import polars as pl


def df_to_markdown_table(df: pl.DataFrame) -> str:
    """Convert Polars DataFrame to markdown table format.

    Args:
        df: Polars DataFrame to convert

    Returns:
        Markdown-formatted table string
    """
    headers = df.columns
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---" for _ in headers]) + " |"

    data_rows = []
    for row in df.iter_rows():
        row_str = "| " + " | ".join([str(val) for val in row]) + " |"
        data_rows.append(row_str)

    return "\n".join([header_row, separator_row] + data_rows)


def create_output_with_metadata(file_path: str) -> Output:
    """Create Dagster Output with standard metadata for a parquet file.

    Args:
        file_path: Path to the parquet file

    Returns:
        Output object with metadata including row count, column count,
        column list, and data preview
    """
    df = pl.read_parquet(file_path)

    return Output(
        value=file_path,
        metadata={
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": MetadataValue.json(df.columns),
            "preview": MetadataValue.md(df_to_markdown_table(df.head(20))),
            "file_path": file_path,
        },
    )
