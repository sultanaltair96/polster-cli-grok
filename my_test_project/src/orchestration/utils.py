"""Utilities for Dagster orchestration."""

from typing import Any, Dict


def create_output_with_metadata(path: str, extra_metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Create output with metadata for Dagster assets.

    Args:
        path: Path to the output file
        extra_metadata: Additional metadata to include

    Returns:
        Dictionary with path and metadata
    """
    metadata = {
        "path": path,
        "description": f"Data written to {path}",
    }

    if extra_metadata:
        metadata.update(extra_metadata)

    return {
        "result": path,
        "metadata": metadata,
    }