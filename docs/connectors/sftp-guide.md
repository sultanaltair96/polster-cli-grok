# SFTP Connector Guide

This guide shows how to use Polster-CLI's SFTP connector template to ingest files from SFTP servers into your bronze layer. The connector supports secure file downloads with pattern matching and multiple formats.

## Prerequisites

1. Install required dependency:
   ```bash
   pip install paramiko
   ```

2. Set up environment variables in your project's `.env` file:
   ```env
   SFTP_HOST=your-sftp-server.com
   SFTP_USER=your-username
   SFTP_PASSWORD=your-password  # For password auth
   # OR for key-based auth:
   SFTP_KEY_PATH=/path/to/private/key  # Path to SSH private key
   SFTP_REMOTE_PATH=/remote/directory  # Remote directory to download from
   SFTP_LOCAL_PATH=./temp/sftp  # Local temp directory for downloads
   ```

## Setup

1. Copy the connector template to your project:
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   ```

2. Import the functions in your bronze asset file:
   ```python
   from core.connectors import download_sftp_files, load_sftp_data
   ```

## Example Asset

Create a bronze asset for SFTP file ingestion:

```python
# src/core/bronze_sftp_logs.py
import os
from dagster import asset
from core.connectors import download_sftp_files, load_sftp_data

@asset
def bronze_sftp_logs():
    """
    Ingest log files from SFTP server.
    """
    # Download files matching pattern
    downloaded_files = download_sftp_files(
        host=os.getenv('SFTP_HOST'),
        username=os.getenv('SFTP_USER'),
        password=os.getenv('SFTP_PASSWORD'),  # Or use key_path for key auth
        remote_path=os.getenv('SFTP_REMOTE_PATH', '/logs'),
        local_path=os.getenv('SFTP_LOCAL_PATH', './temp/sftp'),
        file_pattern='*.log'  # Optional: filter files
    )

    if not downloaded_files:
        # Return empty DataFrame if no files found
        return pl.DataFrame()

    # Load and combine files
    df = load_sftp_data(downloaded_files, format='csv')

    # Optional: Add processing timestamp
    df = df.with_columns(
        pl.lit(pl.datetime.now()).alias('ingested_at')
    )

    return df
```

## Authentication Methods

### Password Authentication

```python
downloaded_files = download_sftp_files(
    host='sftp.example.com',
    username='user',
    password=os.getenv('SFTP_PASSWORD'),
    remote_path='/data',
    local_path='./downloads'
)
```

### SSH Key Authentication

```python
downloaded_files = download_sftp_files(
    host='sftp.example.com',
    username='user',
    key_path='/home/user/.ssh/id_rsa',  # Path to private key
    remote_path='/data',
    local_path='./downloads'
)
```

## Supported File Formats

The `load_sftp_data` function supports:

- **CSV**: `format='csv'` - Automatic delimiter detection
- **JSON**: `format='json'` - Line-delimited or array format
- **Parquet**: `format='parquet'` - Efficient columnar storage

```python
# Load different formats
csv_data = load_sftp_data(files, format='csv')
json_data = load_sftp_data(files, format='json')
parquet_data = load_sftp_data(files, format='parquet')
```

## File Pattern Matching

Use glob patterns to selectively download files:

```python
# Download only CSV files from today
downloaded_files = download_sftp_files(
    # ... connection params ...
    file_pattern='*2024-01-22*.csv'  # Date-specific files
)

# Download all log files
downloaded_files = download_sftp_files(
    # ... connection params ...
    file_pattern='*.log'
)

# Download specific prefixes
downloaded_files = download_sftp_files(
    # ... connection params ...
    file_pattern='app_*.json'
)
```

## Integration with Polster-CLI

1. Generate the orchestration layer:
   ```bash
   polster add-asset --name sftp_logs --layer bronze
   ```

2. Update the generated file to use your custom bronze function.

## Handling Large Files

For large files or many files, consider chunking:

```python
@asset
def bronze_sftp_large_files():
    """
    Process large SFTP files in chunks.
    """
    downloaded_files = download_sftp_files(
        host=os.getenv('SFTP_HOST'),
        username=os.getenv('SFTP_USER'),
        password=os.getenv('SFTP_PASSWORD'),
        remote_path='/large-files',
        local_path='./temp/large',
        file_pattern='*.parquet'
    )

    # Process in batches
    batch_size = 10
    all_data = []

    for i in range(0, len(downloaded_files), batch_size):
        batch_files = downloaded_files[i:i + batch_size]
        batch_df = load_sftp_data(batch_files, format='parquet')
        all_data.append(batch_df)

    return pl.concat(all_data) if all_data else pl.DataFrame()
```

## Best Practices

- **Temporary Storage**: Use local temp directories; clean up after processing
- **File Validation**: Check file sizes and timestamps before processing
- **Incremental Loading**: Track processed files to avoid re-downloading
- **Security**: Use SSH keys over passwords when possible
- **Monitoring**: Log download counts and file sizes for observability

## Troubleshooting

- **Connection Refused**: Check hostname, port (default 22), and firewall rules
- **Authentication Failed**: Verify credentials or key file permissions
- **Permission Denied**: Ensure SFTP user has read access to remote directory
- **No Files Found**: Check remote path exists and pattern matches files
- **Large File Timeouts**: Increase connection timeouts or process in chunks

## Advanced Usage

- **Custom File Processing**: Extend `load_sftp_data` for specialized formats
- **Compression**: Add gzip/bzip2 support for compressed files
- **Directory Recursion**: Modify to download from subdirectories
- **Parallel Downloads**: Use threading for multiple file downloads
- **Checksum Validation**: Verify file integrity after download

See the template file for the complete SFTP functions and additional options.