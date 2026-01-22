# API Connector Guide

This guide shows how to use Polster-CLI's API connector template to ingest data from REST APIs into your bronze layer.

## Prerequisites

1. Install required dependency:
   ```bash
   pip install requests
   ```

2. Set up environment variables in your project's `.env` file (varies by API):
   ```env
   API_BASE_URL=https://api.example.com
   API_TOKEN=your-api-token  # For Bearer auth
   API_KEY=your-api-key      # For API key auth
   API_USERNAME=your-username  # For Basic auth
   API_PASSWORD=your-password  # For Basic auth
   ```

## Setup

1. Copy the connector template to your project:
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   ```

2. Import the function in your bronze asset file:
   ```python
   from core.connectors import fetch_api_data
   ```

## Example Assets

### Bearer Token Authentication

```python
# src/core/bronze_api_orders.py
import os
from dagster import asset
from core.connectors import fetch_api_data

@asset
def bronze_api_orders():
    """
    Ingest order data from REST API with Bearer token auth.
    """
    df = fetch_api_data(
        url=f"{os.getenv('API_BASE_URL')}/orders",
        method='GET',
        auth_method='bearer',
        auth_params={'token': os.getenv('API_TOKEN')},
        params={'status': 'completed', 'limit': 1000}
    )

    # Optional: Transform data
    df = df.with_columns(
        pl.col('order_date').str.strptime(pl.Datetime, '%Y-%m-%dT%H:%M:%SZ')
    )

    return df
```

### API Key Authentication

```python
# src/core/bronze_api_products.py
import os
from dagster import asset
from core.connectors import fetch_api_data

@asset
def bronze_api_products():
    """
    Ingest product data from REST API with API key auth.
    """
    df = fetch_api_data(
        url=f"{os.getenv('API_BASE_URL')}/products",
        method='GET',
        auth_method='api_key',
        auth_params={
            'key': os.getenv('API_KEY'),
            'header': 'X-API-Key'  # Customize header name if needed
        },
        headers={'Accept': 'application/json'}
    )

    return df
```

### Basic Authentication

```python
# src/core/bronze_api_inventory.py
import os
from dagster import asset
from core.connectors import fetch_api_data

@asset
def bronze_api_inventory():
    """
    Ingest inventory data from REST API with Basic auth.
    """
    df = fetch_api_data(
        url=f"{os.getenv('API_BASE_URL')}/inventory",
        method='GET',
        auth_method='basic',
        auth_params={
            'username': os.getenv('API_USERNAME'),
            'password': os.getenv('API_PASSWORD')
        }
    )

    return df
```

## Integration with Polster-CLI

1. Generate the orchestration layer for each asset:
   ```bash
   polster add-asset --name api_orders --layer bronze
   polster add-asset --name api_products --layer bronze
   polster add-asset --name api_inventory --layer bronze
   ```

2. Update the generated orchestration files to use your custom bronze functions.

## Handling Pagination

For APIs with pagination, modify the connector function or create a custom version:

```python
def fetch_paginated_api_data(base_url, auth_method, auth_params, max_pages=10):
    """
    Fetch paginated API data.
    """
    all_data = []
    page = 1

    while page <= max_pages:
        df = fetch_api_data(
            url=base_url,
            params={'page': page, 'per_page': 100},
            auth_method=auth_method,
            auth_params=auth_params
        )

        if df.is_empty():
            break

        all_data.append(df)
        page += 1

    return pl.concat(all_data) if all_data else pl.DataFrame()
```

## Best Practices

- **Rate Limiting**: Add delays between requests if API has rate limits
- **Error Handling**: Wrap API calls in try/catch for resilience
- **Data Validation**: Check response structure before DataFrame conversion
- **Caching**: For static data, consider local caching to reduce API calls
- **Authentication**: Use the most secure method available (Bearer > API Key > Basic)

## Troubleshooting

- **401 Unauthorized**: Check authentication credentials and method
- **403 Forbidden**: Verify API permissions and rate limits
- **500 Server Error**: API may be down; add retry logic
- **Timeout Errors**: Increase timeout parameter or check network connectivity
- **JSON Parsing**: Ensure API returns expected JSON structure

## Advanced Usage

- **Custom Headers**: Add API version, user agent, or other headers
- **POST Requests**: For APIs requiring data submission
- **File Uploads**: Modify for APIs accepting file uploads
- **OAuth2**: Extend auth_method for OAuth2 flows if needed
- **Async Processing**: For high-volume API calls, consider async versions

See the template file for the complete `fetch_api_data` function and additional examples.