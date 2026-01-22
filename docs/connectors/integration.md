# Connector Integration Guide

This guide explains how to integrate custom data connectors into your Polster-CLI projects using the provided templates and guides.

## Overview

Polster-CLI provides connector templates as starting points for common data sources. These are not included by default to keep the core lightweight, but they offer a modular, extensible approach for ingesting data from MySQL databases, REST APIs, and SFTP servers.

## Getting Started

1. **Copy the Template**:
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   ```

2. **Install Dependencies** (as needed):
   - MySQL: `pip install pymysql`
   - API: `pip install requests`
   - SFTP: `pip install paramiko`

3. **Set Environment Variables** in `.env`:
   ```env
   # MySQL
   MYSQL_HOST=localhost
   MYSQL_USER=user
   MYSQL_PASSWORD=password
   MYSQL_DATABASE=db

   # API
   API_BASE_URL=https://api.example.com
   API_TOKEN=token

   # SFTP
   SFTP_HOST=sftp.example.com
   SFTP_USER=user
   SFTP_PASSWORD=password
   SFTP_REMOTE_PATH=/data
   SFTP_LOCAL_PATH=./temp
   ```

## Connector Architecture

The template provides functional connectors with these patterns:

### Function-Based Design
- **Connection Functions**: Handle authentication and setup
- **Fetch/Load Functions**: Retrieve and process data
- **Helper Functions**: Validation, error handling, utilities

### Modular Sections
Each connector type is self-contained, making it easy to:
- Use only what you need
- Extend with custom logic
- Replace with your own implementations

## Creating Bronze Assets

### Step 1: Create Core Logic

Create files in `src/core/` for your data ingestion logic:

```python
# src/core/bronze_custom_source.py
from dagster import asset
from core.connectors import fetch_api_data  # Example import
import os

@asset
def bronze_custom_data():
    """
    Ingest data from custom source.
    """
    # Your connector logic here
    df = fetch_api_data(
        url=os.getenv('API_URL'),
        auth_method='bearer',
        auth_params={'token': os.getenv('API_TOKEN')}
    )

    # Optional transformations
    df = df.with_columns(
        pl.col('timestamp').str.strptime(pl.Datetime)
    )

    return df
```

### Step 2: Generate Orchestration

Use Polster-CLI to create the Dagster asset wrapper:

```bash
polster add-asset --name custom_data --layer bronze
```

This generates `src/orchestration/assets/bronze/run_bronze_custom_data.py`.

### Step 3: Connect Core to Orchestration

Update the generated file to import and use your core function:

```python
# src/orchestration/assets/bronze/run_bronze_custom_data.py
from core.bronze_custom_source import bronze_custom_data

# The asset is already defined in your core file
# This file just registers it with Dagster
```

## Extending Connectors

### Adding Custom Functions

Extend the template with your own functions:

```python
# In src/core/connectors.py
def connect_postgres(host, user, password, database):
    """Custom PostgreSQL connector."""
    import psycopg2
    return psycopg2.connect(
        host=host, user=user, password=password, dbname=database
    )

def fetch_postgres_data(connection, query):
    """Fetch data from PostgreSQL."""
    return pl.read_database(query, connection)
```

### Modifying Existing Functions

Copy and adapt functions for your needs:

```python
def fetch_api_data_custom(url, auth_method, auth_params, **kwargs):
    """Extended API fetcher with custom logic."""
    # Start with template function
    df = fetch_api_data(url, auth_method, auth_params, **kwargs)

    # Add custom processing
    df = df.filter(pl.col('status') == 'active')

    return df
```

## Best Practices

### Security
- Always use environment variables for credentials
- Validate connection parameters before use
- Use SSH keys over passwords for SFTP when possible

### Error Handling
```python
@asset
def bronze_robust_data():
    try:
        df = fetch_api_data(...)
        return df
    except Exception as e:
        # Log error and return empty DataFrame
        print(f"Ingestion failed: {e}")
        return pl.DataFrame()
```

### Performance
- Use connection pooling for databases
- Implement incremental loading for large datasets
- Cache static API responses when appropriate

### Testing
- Test connectors independently before integration
- Use mock data for unit tests
- Validate data schemas in silver layer

## Troubleshooting Common Issues

### Import Errors
- Ensure template is copied to correct location
- Check Python path includes `src/`
- Verify dependencies are installed

### Connection Failures
- Check environment variables are set
- Validate network connectivity
- Review authentication credentials

### Data Format Issues
- Inspect raw data before DataFrame conversion
- Handle missing or malformed fields gracefully
- Use schema validation in silver layer

## Advanced Patterns

### Multi-Source Assets
```python
@asset
def bronze_combined_data():
    """Combine data from multiple sources."""
    api_df = fetch_api_data(...)
    mysql_df = fetch_mysql_data(...)

    # Join or union as needed
    combined = pl.concat([api_df, mysql_df])
    return combined
```

### Scheduled Incremental Loads
```python
@asset
def bronze_incremental_data(context):
    """Load only new data since last run."""
    last_run = context.get_asset_partition_key()

    query = f"SELECT * FROM table WHERE updated_at > '{last_run}'"
    df = fetch_mysql_data(connection, query)

    return df
```

### Dependency Chains
Ensure bronze assets are upstream for silver processing:
```python
@asset(deps=[bronze_custom_data])
def silver_processed_data():
    """Process bronze data."""
    df = bronze_custom_data()
    # Clean and transform
    return df
```

## Contributing Back

If you create useful connector extensions:
- Consider sharing them as community guides
- Follow the template patterns for consistency
- Document setup and usage clearly

## Next Steps

After setting up connectors:
1. Test with sample data
2. Build silver layer transformations
3. Create gold layer aggregations
4. Set up scheduling and monitoring

See individual connector guides (mysql-guide.md, api-guide.md, sftp-guide.md) for detailed examples and advanced usage.