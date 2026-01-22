# MySQL Connector Guide

This guide shows how to use Polster-CLI's MySQL connector template to ingest data from MySQL databases into your bronze layer.

## Prerequisites

1. Install required dependency:
   ```bash
   pip install pymysql
   ```

2. Set up environment variables in your project's `.env` file:
   ```env
   MYSQL_HOST=your-mysql-host.com
   MYSQL_USER=your-username
   MYSQL_PASSWORD=your-password
   MYSQL_DATABASE=your-database-name
   MYSQL_PORT=3306  # Optional, defaults to 3306
   ```

## Setup

1. Copy the connector template to your project:
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   ```

2. Import the functions in your bronze asset file (e.g., `src/core/bronze_mysql_data.py`):
   ```python
   from core.connectors import connect_mysql, fetch_mysql_data
   ```

## Example Asset

Create a new bronze asset for MySQL data:

```python
# src/core/bronze_mysql_data.py
import os
from dagster import asset
from core.connectors import connect_mysql, fetch_mysql_data

@asset
def bronze_mysql_users():
    """
    Ingest user data from MySQL database.
    """
    # Establish connection
    conn = connect_mysql(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        port=int(os.getenv('MYSQL_PORT', 3306))
    )

    try:
        # Execute query
        query = """
        SELECT
            id,
            username,
            email,
            created_at,
            updated_at
        FROM users
        WHERE created_at >= '2023-01-01'
        """
        df = fetch_mysql_data(conn, query)

        # Optional: Add metadata or transformations
        df = df.with_columns(
            pl.col('created_at').str.strptime(pl.Datetime, '%Y-%m-%d %H:%M:%S'),
            pl.col('updated_at').str.strptime(pl.Datetime, '%Y-%m-%d %H:%M:%S')
        )

        return df

    finally:
        # Always close connection
        conn.close()
```

## Integration with Polster-CLI

1. Generate the orchestration layer:
   ```bash
   polster add-asset --name mysql_users --layer bronze
   ```

2. This creates `src/orchestration/assets/bronze/run_bronze_mysql_users.py` with the asset definition.

3. Update the generated file to use your custom logic:
   ```python
   from core.bronze_mysql_data import bronze_mysql_users

   # The asset is already imported and defined
   ```

## Best Practices

- **Connection Management**: Always use `try/finally` to close connections
- **Query Optimization**: Use appropriate WHERE clauses to limit data volume
- **Security**: Never hardcode credentials; use environment variables
- **Error Handling**: Add try/catch blocks for production resilience
- **Data Types**: Polars will infer column types; validate them in silver layer

## Troubleshooting

- **Connection Errors**: Check firewall settings and MySQL user permissions
- **Import Errors**: Ensure `pymysql` is installed and import path is correct
- **Query Errors**: Test queries directly in MySQL client first
- **Performance**: For large datasets, consider chunking or incremental loading

## Advanced Usage

For more complex scenarios, modify the connector functions:

- Add connection pooling for multiple queries
- Implement retry logic for transient failures
- Support for stored procedures or dynamic queries
- Batch processing for very large tables

See the template file for additional helper functions and examples.