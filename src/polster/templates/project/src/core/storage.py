"""Storage abstraction for local and ADLS backends."""

from __future__ import annotations

import io
import os
from typing import Literal
from urllib.parse import urlparse

import polars as pl

from .paths import DATA_DIR

StorageBackend = Literal["local", "adls"]


def _load_env(name: str, default: str | None = None) -> str | None:
    """Load environment variable with optional default."""
    value = os.getenv(name, default)
    return value


def get_storage_backend() -> StorageBackend:
    """Get the configured storage backend."""
    backend = (_load_env("STORAGE_BACKEND", "local") or "local").lower()
    if backend not in {"local", "adls"}:
        raise ValueError(f"Unsupported STORAGE_BACKEND: {backend}")
    return backend  # type: ignore[return-value]


def is_adls_configured() -> bool:
    """Check if ADLS is properly configured."""
    return all(
        [
            _load_env("ADLS_ACCOUNT_NAME"),
            _load_env("ADLS_ACCOUNT_KEY"),
            _load_env("ADLS_CONTAINER"),
        ]
    )


def _adls_base_path() -> str:
    """Get ADLS base path."""
    return (_load_env("ADLS_BASE_PATH", "polster/data") or "polster/data").strip("/")


def get_adls_base_path() -> str:
    """Get ADLS base path (public interface)."""
    return _adls_base_path()


def resolve_path(layer: str, filename: str) -> str:
    """Resolve file path for the configured storage backend."""
    backend = get_storage_backend()
    if backend == "local":
        return os.path.join(DATA_DIR, layer, filename)

    account_name = _load_env("ADLS_ACCOUNT_NAME")
    container = _load_env("ADLS_CONTAINER")
    if not account_name or not container:
        raise ValueError(
            "ADLS_ACCOUNT_NAME and ADLS_CONTAINER are required for ADLS storage"
        )
    base_path = _adls_base_path()
    return f"abfss://{container}@{account_name}.dfs.core.windows.net/{base_path}/{layer}/{filename}"


def write_parquet(df: pl.DataFrame, layer: str, filename: str) -> str:
    """Write a DataFrame to parquet storage."""
    backend = get_storage_backend()

    if backend == "local":
        output_path = resolve_path(layer, filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.write_parquet(output_path)
        return output_path

    output_uri = resolve_path(layer, filename)
    parsed = urlparse(output_uri)

    account_name = _load_env("ADLS_ACCOUNT_NAME")
    account_key = _load_env("ADLS_ACCOUNT_KEY")
    container = _load_env("ADLS_CONTAINER")

    if not account_name or not account_key or not container:
        return _write_parquet_local_fallback(df, layer, filename)

    output_path = parsed.path.lstrip("/")

    buffer = io.BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)

    try:
        from azure.storage.filedatalake import DataLakeServiceClient
    except ModuleNotFoundError:
        return _write_parquet_local_fallback(df, layer, filename)

    data_lake_service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key,
    )
    file_system_client = data_lake_service_client.get_file_system_client(container)
    file_client = file_system_client.get_file_client(output_path)
    file_client.upload_data(buffer.read(), overwrite=True)

    return output_uri


def _write_parquet_local_fallback(df: pl.DataFrame, layer: str, filename: str) -> str:
    """Fallback to local storage if ADLS is not configured."""
    output_path = os.path.join(DATA_DIR, layer, filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.write_parquet(output_path)
    return output_path


def read_parquet_latest(layer: str, prefix: str) -> pl.DataFrame:
    """Read the latest parquet file for a given prefix."""
    backend = get_storage_backend()
    if backend == "local" or not is_adls_configured():
        return _read_latest_local(layer, prefix)

    account_name = _load_env("ADLS_ACCOUNT_NAME")
    account_key = _load_env("ADLS_ACCOUNT_KEY")
    container = _load_env("ADLS_CONTAINER")
    base_path = _adls_base_path()

    if not account_name or not account_key or not container:
        return _read_latest_local(layer, prefix)

    try:
        from azure.storage.filedatalake import DataLakeServiceClient
    except ModuleNotFoundError:
        return _read_latest_local(layer, prefix)

    data_lake_service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key,
    )
    file_system_client = data_lake_service_client.get_file_system_client(container)

    directory_path = f"{base_path}/{layer}".strip("/")
    candidates = []
    for path_item in file_system_client.get_paths(path=directory_path):
        if path_item.is_directory:
            continue
        name = path_item.name.split("/")[-1]
        if name.startswith(prefix) and name.endswith(".parquet"):
            candidates.append(path_item.name)

    if not candidates:
        raise FileNotFoundError(
            f"No parquet files found in {directory_path} with prefix {prefix}"
        )

    latest_path = max(candidates)
    file_client = file_system_client.get_file_client(latest_path)
    data = file_client.download_file().readall()
    buffer = io.BytesIO(data)
    return pl.read_parquet(buffer)


def _read_latest_local(layer: str, prefix: str) -> pl.DataFrame:
    """Read the latest parquet file from local storage."""
    directory = os.path.join(DATA_DIR, layer)
    candidates = [
        filename
        for filename in os.listdir(directory)
        if filename.startswith(prefix) and filename.endswith(".parquet")
    ]
    if not candidates:
        raise FileNotFoundError(
            f"No parquet files found in {directory} with prefix {prefix}"
        )
    latest = max(candidates)
    return pl.read_parquet(os.path.join(directory, latest))
