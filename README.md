# Polster

[![PyPI version](https://badge.fury.io/py/polster.svg)](https://pypi.org/project/polster/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/sultanaltair96/polster-cli-grok/actions/workflows/ci.yml/badge.svg)](https://github.com/sultanaltair96/polster-cli-grok/actions)

**Build reliable data pipelines with enforced Medallion Architecture**

Polster is a CLI tool that generates production-ready Dagster projects following the Medallion Architecture pattern. It helps data engineers create scalable, maintainable ETL pipelines with proper data layering and dependency management.

Whether you're new to data engineering or a seasoned architect, Polster provides the structure and tooling to build data workflows that scale.

## Background

Polster was born from experimenting with modern Python data tools like Polars and Dagster. These libraries represent the cutting edge of data engineering, and Polster combines their strengths into a batteries-included platform.

**Polars** excels with its lightning-fast, memory-efficient DataFrame operations. Built in Rust, it delivers:
- **Speed**: Multi-threaded processing that's 5-10x faster than Pandas
- **Scalability**: Handles millions of rows effortlessly with lazy evaluation
- **Expressiveness**: Familiar API that feels like Pandas but optimized for performance

**Dagster** revolutionizes pipeline orchestration with data-aware workflows:
- **Asset Modeling**: Treats data as first-class citizens with automatic lineage tracking
- **Visibility**: Built-in dashboards and monitoring for production pipelines
- **Flexibility**: Extensible framework that integrates with modern tools and platforms

**Polster picks up these strengths** and adds:
- **Enforced Architecture**: Automatic Medallion layers prevent common mistakes
- **CLI Simplicity**: One-command project generation and asset management
- **Production Templates**: Ready-to-deploy code with storage, monitoring, and error handling
- **Batteries Included**: Everything you need to go from idea to production pipeline

## Table of Contents

- [Background](#background)
- [Why Polster?](#why-polster)
- [Key Features](#key-features)
- [Medallion Architecture](#medallion-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
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
   polster init my_first_pipeline
   cd my_first_pipeline
   ```

2. **Add a Bronze Asset** (raw data)
   ```bash
   polster add-asset --layer bronze --name ingest_sales
   ```

3. **Add a Silver Asset** (clean data)
   ```bash
   polster add-asset --layer silver --name clean_sales --dependencies ingest_sales
   ```

4. **Add a Gold Asset** (business metrics)  
   ```bash
   polster add-asset --layer gold --name sales_metrics --dependencies clean_sales
   ```

5. **Run Your Pipeline**
   ```bash
   python run_polster.py --ui
   ```

That's it! You now have a complete data pipeline following best practices.

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

## API Reference

### Global Options
- `--help`: Show help message
- `--version`: Show version information
- `--verbose`: Enable verbose output

### `polster init <project_name>`
Create a new Polster project with standard directory structure.

**Options:**
- `--template <template>`: Use specific template (default: standard)

**Example:**
```bash
polster init my_project
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