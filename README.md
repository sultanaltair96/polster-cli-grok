# Polster

[![PyPI version](https://badge.fury.io/py/polster.svg)](https://pypi.org/project/polster/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/sultanaltair96/polster-cli-grok/actions/workflows/ci.yml/badge.svg)](https://github.com/sultanaltair96/polster-cli-grok/actions)

**Build reliable data pipelines with enforced Medallion Architecture**

Polster is a CLI tool that generates production-ready Dagster projects following the Medallion Architecture pattern. It helps data engineers create scalable, maintainable ETL pipelines with proper data layering and dependency management.

Whether you're new to data engineering or a seasoned architect, Polster provides the structure and tooling to build data workflows that scale.

## Background

Polster was inspired by the same philosophy that made dbt revolutionary: **making data engineering accessible and enjoyable**. While dbt pioneered treating data transformations as code with SQL, Polster brings this approach to Python's ecosystem.

**What dbt Got Right:**
- **Easy Getting Started**: Simple `dbt init` creates a full project instantly
- **Transformation as Code**: Version-controlled, testable data models
- **Built-in Best Practices**: Guides users toward reliable patterns
- **Documentation Culture**: Auto-generated lineage and model documentation

**Polster adapts these principles for Python:**
- **Polars** delivers unmatched speed and efficiency in data processing
- **Dagster** provides intelligent pipeline orchestration with asset modeling
- **Python-First**: Full Python ecosystem instead of SQL constraints

**The Result**: dbt's ease of use meets Python's power - a batteries-included platform that feels familiar to dbt users but unlocks Python's full potential.

| dbt Concept | Polster Equivalent | Python Advantage |
|-------------|-------------------|------------------|
| `dbt init` | `polster init` | Full Python project with virtual environment |
| SQL Models | Python Assets | Any Python library, complex logic, ML models |
| dbt Tests | Medallion Layers | Built-in data quality with flexible validation |
| dbt Docs | Dagster UI | Interactive pipeline monitoring and debugging |
| Materializations | Storage Backends | Native Python integrations (APIs, databases, etc.) |

## Table of Contents

- [Background](#background)
- [Why Polster?](#why-polster)
- [Key Features](#key-features)
- [Medallion Architecture](#medallion-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Data Connectors](#data-connectors)
- [CI/CD Integration](#cicd-integration)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Why Polster?

Data engineering projects often start simple but grow complex. Without structure, pipelines become:

- **Hard to debug**: Unclear dependencies make tracing issues difficult
- **Brittle**: Changes in one part break others unexpectedly  
- **Inconsistent**: Different engineers follow different patterns
- **Unmaintainable**: Code becomes a tangled mess over time

Polster solves this by enforcing the Medallion Architecture - a proven pattern that organizes data transformation into logical layers. This creates:

- **Clear data lineage**: Know exactly where data comes from and goes
- **Predictable patterns**: Consistent structure across all projects
- **Easier testing**: Isolated layers can be tested independently
- **Better collaboration**: Everyone understands the project structure

It's like having a blueprint for your data house - you know where the foundation, walls, and roof go before you start building.

## Key Features

- **🛡️ Enforced Architecture**: Automatically creates Bronze → Silver → Gold layers with proper dependencies
- **⚡ Quick Start**: Generate complete projects in seconds with `polster init`
- **🔗 Smart Dependencies**: Interactive prompts help you connect assets correctly
- **🐍 Python Native**: Uses familiar Python patterns with Dagster orchestration
- **📊 Production Ready**: Includes monitoring, scheduling, and error handling
- **🧪 Testable**: Each layer can be unit tested independently
- **📚 Well Documented**: Clear examples and comprehensive guides
- **🔌 Data Connectors**: Pre-built templates for MySQL, REST APIs, and SFTP
- **🚀 CI/CD Ready**: Automated pipeline generation for major platforms

## Medallion Architecture

Polster enforces the Medallion Architecture, organizing your data pipeline into three layers. Think of it like refining ore: raw material → purified metal → finished jewelry.

### Bronze Layer: Raw Data Ingestion
**Purpose**: Capture raw data exactly as received
- **Examples**: API responses, database dumps, log files, CSV exports
- **Characteristics**: Unchanged, timestamped, auditable
- **Tools**: Polars for fast data loading, minimal transformations

```python
# Bronze asset example
@asset
def bronze_user_events():
    """Load raw user event data from API"""
    return pl.read_csv("raw_events.csv")
```

### Silver Layer: Clean & Validated Data  
**Purpose**: Clean, validate, and standardize data
- **Examples**: Deduplicated records, type-validated columns, normalized formats
- **Characteristics**: High quality, ready for analysis, business logic applied
- **Dependencies**: Can only depend on Bronze assets

```python
# Silver asset example  
@asset
def silver_clean_users(bronze_user_events):
    """Clean and validate user data"""
    return (
        bronze_user_events
        .drop_nulls()
        .with_columns(pl.col("email").str.to_lowercase())
    )
```

### Gold Layer: Business Insights
**Purpose**: Aggregate and enrich data for business decisions
- **Examples**: KPI dashboards, ML features, executive reports
- **Characteristics**: Curated, aggregated, business-value focused
- **Dependencies**: Can only depend on Silver assets

```python
# Gold asset example
@asset  
def gold_user_metrics(silver_clean_users):
    """Calculate user engagement metrics"""
    return (
        silver_clean_users
        .group_by("user_id")
        .agg([
            pl.col("events").count().alias("total_events"),
            pl.col("last_login").max().alias("latest_activity")
        ])
    )
```

This layered approach ensures data quality improves at each stage and makes debugging much easier - you know exactly which layer might have issues.

## Installation

### Requirements
- Python 3.12 or higher
- pip package manager

### Install from PyPI (Recommended)
```bash
pip install polster
```

### Install from Source (Development)
```bash
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
```

### Verify Installation
```bash
polster --version
```

You should see the version number if installed correctly.

## Quick Start

Let's create your first Polster project in 5 minutes:

1. **Create Project**
   ```bash
   polster init my_first_pipeline --cicd github-actions  # Optional: add CI/CD pipeline
   cd my_first_pipeline
   ```

2. **Add Data Connectors** (optional)
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   # Edit connectors.py to add your data source credentials
   ```

3. **Add a Bronze Asset** (raw data)
   ```bash
   polster add-asset --layer bronze --name ingest_sales
   ```

4. **Add a Silver Asset** (clean data)
   ```bash
   polster add-asset --layer silver --name clean_sales --dependencies ingest_sales
   ```

5. **Add a Gold Asset** (business metrics)
   ```bash
   polster add-asset --layer gold --name sales_metrics --dependencies clean_sales
   ```

6. **Run Your Pipeline**
   ```bash
   python run_polster.py --ui
   ```

That's it! You now have a complete data pipeline following best practices.

## Data Connectors

Polster provides modular connector templates for common data sources, following a "batteries included" philosophy through extensible guides rather than bundled dependencies.

### Available Connectors

- **MySQL**: Ingest data from MySQL databases with secure connection handling
- **REST APIs**: Fetch data from REST APIs with support for Bearer tokens, API keys, and Basic auth
- **SFTP**: Download files from SFTP servers (ingestion-only, maintaining data lake architecture)

### Getting Started with Connectors

1. **Copy the template**:
   ```bash
   cp docs/connectors/connectors.py.template src/core/connectors.py
   ```

2. **Install dependencies** as needed:
   ```bash
   pip install pymysql requests paramiko  # Install only what you need
   ```

3. **Follow the guides**:
   - [MySQL Connector Guide](docs/connectors/mysql-guide.md)
   - [API Connector Guide](docs/connectors/api-guide.md)
   - [SFTP Connector Guide](docs/connectors/sftp-guide.md)
   - [Integration Guide](docs/connectors/integration.md)

### Why Templates Instead of Built-ins?

- **Lightweight**: No forced dependencies on unused connectors
- **Flexible**: Adapt templates to your specific requirements
- **Secure**: You control authentication and connection methods
- **Extensible**: Easy to add new connector types following the same patterns

### Example: MySQL Connector

```python
# src/core/bronze_mysql_users.py
import os
from dagster import asset
from core.connectors import connect_mysql, fetch_mysql_data

@asset
def bronze_mysql_users():
    conn = connect_mysql(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

    df = fetch_mysql_data(conn, "SELECT * FROM users")
    conn.close()
    return df
```

See the [Integration Guide](docs/connectors/integration.md) for complete examples and best practices.

## Examples

### Complete E-commerce Pipeline

Let's build a realistic e-commerce analytics pipeline:

```bash
# Create project
polster init ecommerce_analytics

cd ecommerce_analytics

# Bronze: Ingest raw order data
polster add-asset --layer bronze --name raw_orders

# Silver: Clean and validate orders  
polster add-asset --layer silver --name validated_orders --dependencies raw_orders

# Bronze: Ingest customer data
polster add-asset --layer bronze --name raw_customers

# Silver: Clean customer data
polster add-asset --layer silver --name clean_customers --dependencies raw_customers

# Gold: Customer lifetime value
polster add-asset --layer gold --name customer_ltv --dependencies validated_orders,clean_customers

# Gold: Product performance
polster add-asset --layer gold --name product_analytics --dependencies validated_orders
```

### Interactive Dependency Selection

When adding assets, Polster guides you:

```bash
$ polster add-asset --layer silver --name user_profiles

Available Bronze assets to depend on:
1. raw_user_events
2. raw_user_logs  
3. raw_signups

Select dependencies (comma-separated numbers): 1,3
```

This ensures you can't accidentally create invalid dependencies (like Gold depending on Bronze).

### Running & Monitoring

```bash
# Start Dagster UI
python run_polster.py --ui

# Or run specific assets
python run_polster.py --asset bronze_raw_orders

# Check pipeline status
python run_polster.py --status
```

## CI/CD Integration

Automate your data pipelines with one-command CI/CD setup for major platforms.

### Supported Platforms

Polster generates ready-to-use pipelines for:

- **Azure DevOps**: `azure-pipelines.yml` with your proven automation logic
- **GitHub Actions**: `.github/workflows/polster.yml` for seamless integration
- **GitLab CI**: `.gitlab-ci.yml` for comprehensive pipeline control

### Quick Setup

Generate a project with automated CI/CD:

```bash
# Direct platform specification
polster init my_project --cicd github-actions

# Interactive selection
polster init my_project  # Choose platform when prompted
```

### Pipeline Features

Each generated pipeline includes:

- **Scheduled Runs**: Daily automated data materialization (UTC midnight)
- **Push Triggers**: Automatic runs on code changes to master/main
- **Python Environment**: uv-based dependency management
- **Data Persistence**: Commits generated data and artifacts back to repository
- **Error Handling**: Robust failure management and logging

### Example: Azure DevOps Pipeline

The generated `azure-pipelines.yml` includes:

```yaml
# Trigger on master branch pushes and daily schedules
trigger:
  branches:
    include:
      - master

schedules:
- cron: "0 0 * * *"
  displayName: Daily data materialization

steps:
- script: |
    source .venv/bin/activate
    python run_polster.py  # Your data pipeline
- script: |
    git add data/ .dagster/
    git commit -m "Automated data materialization"
    git push
```

### Advanced Configuration

- **Environment Variables**: Secure credential storage via platform secrets
- **Multi-Environment**: Configure dev/staging/prod deployments
- **Custom Scheduling**: Modify cron expressions for different frequencies
- **Parallel Jobs**: Split pipelines for large-scale processing

### Platform-Specific Setup

**Azure DevOps:**
- Store secrets in Variable Groups or Key Vaults
- Configure agent pools for your infrastructure

**GitHub Actions:**
- Use repository secrets for sensitive data
- Leverage GitHub's free tiers for small projects

**GitLab CI:**
- Utilize CI/CD variables and protected environments
- Integrate with GitLab's advanced pipeline features

See the generated pipeline files for complete, working examples tailored to your chosen platform.

## API Reference

### Global Options
- `--help`: Show help message
- `--version`: Show version information
- `--verbose`: Enable verbose output

### `polster init <project_name>`
Create a new Polster project with standard directory structure.

**Options:**
- `--cicd <platform>`: Generate CI/CD pipeline for specified platform (azure-devops, github-actions, gitlab-ci)
- `--git/--no-git`: Initialize git repository (prompts if not specified)
- `--sample-assets/--no-sample-assets`: Create sample stub assets
- `--install-uv/--no-install-uv`: Install uv package manager
- `--dry-run`: Show what would be created without creating
- `--start-dagster`: Start Dagster UI after project creation

**Examples:**
```bash
polster init my_project
polster init my_project --cicd github-actions
polster init my_project --cicd azure-devops --no-sample-assets
```

### `polster add-asset`
Add a new asset to your project.

**Required Options:**
- `--layer <bronze|silver|gold>`: Which layer to add asset to
- `--name <asset_name>`: Asset name (snake_case recommended)

**Optional Options:**
- `--dependencies <asset1,asset2>`: Comma-separated list of dependencies
- `--description "Description"`: Asset description
- `--template <template>`: Asset template to use

**Examples:**
```bash
# Add Bronze asset
polster add-asset --layer bronze --name raw_logs

# Add Silver asset with dependencies
polster add-asset --layer silver --name clean_logs --dependencies raw_logs

# Add Gold asset
polster add-asset --layer gold --name log_metrics --dependencies clean_logs
```

### `polster list-assets`
List all assets in the current project.

**Options:**
- `--layer <layer>`: Filter by layer
- `--format <table|json>`: Output format

### `polster remove-asset`
Remove an asset from the current Polster project.

**Required Options (one of):**
- `--layer <bronze|silver|gold>` and `--name <asset_name>`: Direct removal
- Interactive mode: Run without flags for guided selection

**Optional Options:**
- `--dry-run`: Preview what would be removed without deleting
- `--force`: Skip confirmations and dependency checks

**Safety Features:**
- Blocks removal if other assets depend on the target asset
- High-impact removals (>3 assets) require typing "CONFIRM"
- "All" selections require typing "REMOVE_ALL_ASSETS"

**Examples:**
```bash
# Interactive removal (recommended)
polster remove-asset

# Direct removal
polster remove-asset --layer bronze --name user_events

# Force removal (bypasses safety checks)
polster remove-asset --layer silver --name clean_data --force

# Preview removal
polster remove-asset --layer gold --name metrics --dry-run
```

### `polster validate`
Validate project structure and dependencies.

**Checks:**
- Asset naming conventions
- Dependency rules compliance
- Import path correctness
- Required files presence

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure you're in the project directory
- Run `pip install -e .` to install the project in development mode

**Assets not appearing in Dagster UI:**
- Check `workspace.yaml` has correct pythonpath
- Restart the Dagster daemon: `dagster-daemon restart`

**Dependency conflicts:**
- Silver assets can only depend on Bronze
- Gold assets can only depend on Silver
- Use `polster validate` to check compliance

**Performance issues:**
- Use Polars for large datasets instead of pandas
- Consider partitioning large Bronze assets
- Add caching to expensive transformations

## Contributing

We welcome contributions! Polster is built by the community for the community.

### Development Setup
```bash
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest
```

### Code Style
- Use Black for formatting
- Follow PEP 8 conventions
- Add type hints where possible
- Write comprehensive docstrings

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

Polster is available under the MIT License. See [LICENSE](LICENSE) for details.

---

**Ready to build better data pipelines?** Get started with `polster init your_project` today!</content>
<parameter name="filePath">README.md