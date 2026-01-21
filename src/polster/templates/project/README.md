# Welcome to Your Polster Data Project

You've successfully created a **{{PROJECT_NAME}}** project using Polster CLI! This README will help you get started quickly and build your data pipeline.

**If you love dbt's workflow, you'll feel right at home with Polster** - same reliability principles, but with Python's full power. Like `dbt init` creates a dbt project, `polster init` gives you a production-ready Python data pipeline with enforced best practices.

## 🚀 Quick Start (5 Minutes to First Pipeline)

### 1. Explore Your Project Structure
```bash
cd {{PROJECT_NAME}}
ls -la
```

Your project includes:
- `src/core/` - Data transformation logic
- `src/orchestration/` - Dagster pipeline orchestration  
- `run_polster.py` - Main runner script

### 2. Test the Sample Pipeline
```bash
# Generate sample bronze data
python src/core/bronze_example.py

# Transform to silver (clean) data
python src/core/silver_example.py

# Create gold (business) insights
python src/core/gold_example.py
```

### 3. Launch the Pipeline Dashboard
```bash
python run_polster.py --ui
```

Open http://127.0.0.1:3000 to see your pipeline running with automatic scheduling and monitoring!

## 🏗️ Understanding Medallion Architecture

Polster enforces a **Medallion Architecture** to ensure data quality and maintainability:

### Bronze Layer: Raw Data
- **Purpose**: Ingest raw data as-is
- **Dependencies**: None
- **Example**: API responses, CSV files, database dumps

### Silver Layer: Clean Data
- **Purpose**: Validate, clean, and transform data
- **Dependencies**: Bronze assets only
- **Example**: Deduplicated records, type validation, business logic

### Gold Layer: Business Insights
- **Purpose**: Aggregate for business decisions
- **Dependencies**: Silver assets only
- **Example**: KPIs, ML features, executive reports

**Why this matters**: Prevents shortcuts that lead to data quality issues and makes debugging easier.

## ⚡ Building Your Pipeline with CLI

### Add Your First Bronze Asset
```bash
polster add-asset --layer bronze --name user_events
```

This creates:
- `src/core/bronze_user_events.py` - Your transformation code
- `src/orchestration/assets/bronze/bronze_user_events.py` - Dagster asset

Edit `src/core/bronze_user_events.py` to load your data:

```python
@asset
def bronze_user_events():
    """Load raw user events data"""
    return pl.read_csv("data/user_events.csv")
```

### Add a Silver Asset
```bash
polster add-asset --layer silver --name clean_users --dependencies bronze_user_events
```

Polster will show available Bronze assets to select from. Edit the generated file to clean your data:

```python
@asset
def silver_clean_users(bronze_user_events):
    """Clean and validate user data"""
    return (
        bronze_user_events
        .drop_nulls()
        .filter(pl.col("age") > 0)
    )
```

### Add a Gold Asset
```bash
polster add-asset --layer gold --name user_metrics --dependencies silver_clean_users
```

Create business insights:

```python
@asset
def gold_user_metrics(silver_clean_users):
    """Calculate user engagement metrics"""
    return (
        silver_clean_users
        .group_by("user_id")
        .agg([
            pl.col("events").count().alias("total_events"),
            pl.col("last_login").max().alias("last_active")
        ])
    )
```

### Remove Assets
If you need to remove assets from your pipeline, use the `polster remove-asset` command:

**Remove a specific asset:**
```bash
polster remove-asset --layer bronze --name user_events
```

**Interactive removal with safety checks:**
```bash
polster remove-asset
# Select layer, then choose from numbered list of assets
```

**Force removal (bypasses dependency checks):**
```bash
polster remove-asset --layer silver --name clean_users --force
```

**Safety Features:**
- Automatically detects and warns about downstream dependencies
- Requires confirmation for removals that would break the pipeline
- Use `--dry-run` to preview what would be removed without making changes
- High-impact removals (>3 assets) require typing "CONFIRM"

## 📊 Running & Monitoring Your Pipeline

### Development Mode
```bash
# Run everything and open dashboard
python run_polster.py --ui

# Run only the pipeline (no UI)
python run_polster.py

# Open dashboard without running
python run_polster.py --no-materialize --ui
```

### Production Deployment
```bash
# Schedule with cron or your orchestrator
0 6 * * * cd /path/to/project && python run_polster.py
```

The dashboard shows:
- Asset dependencies and status
- Execution logs and errors
- Data previews and metadata
- Scheduling and sensors

## 💡 Common Patterns & Examples

### Ingesting Different Data Sources

**CSV Files:**
```python
@asset
def bronze_sales_data():
    return pl.read_csv("data/sales.csv")
```

**APIs:**
```python
@asset
def bronze_api_data():
    response = requests.get("https://api.example.com/data")
    return pl.json_normalize(response.json())
```

**Databases:**
```python
@asset
def bronze_db_data():
    return pl.read_database("SELECT * FROM users", connection_string)
```

### Data Quality & Validation

**Silver Layer Validation:**
```python
@asset
def silver_validated_sales(bronze_sales_data):
    df = bronze_sales_data

    # Check required columns exist
    required_cols = ["order_id", "amount", "date"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Validate data types
    df = df.with_columns([
        pl.col("amount").cast(pl.Float64),
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")
    ])

    # Business rules
    df = df.filter(pl.col("amount") > 0)

    return df
```

### Business Aggregations

**Gold Layer KPIs:**
```python
@asset
def gold_sales_kpis(silver_validated_sales):
    return (
        silver_validated_sales
        .group_by(pl.col("date").dt.month())
        .agg([
            pl.col("amount").sum().alias("monthly_revenue"),
            pl.col("order_id").n_unique().alias("monthly_orders"),
            (pl.col("amount").sum() / pl.col("order_id").n_unique()).alias("avg_order_value")
        ])
        .sort("date")
    )
```

## 🔧 Configuration & Storage

### Local Development
Default settings work out-of-the-box for local development.

### Cloud Storage (ADLS)
Create `.env` file:
```bash
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=your_storage_account
ADLS_CONTAINER=your_container
ADLS_BASE_PATH=data/{{PROJECT_NAME}}
ADLS_ACCOUNT_KEY=your_key_here
```

### Environment Variables
- `STORAGE_BACKEND`: `local` or `adls`
- `ADLS_*`: Azure Data Lake Storage settings

## 🐛 Troubleshooting

### Pipeline Won't Start
- Check `workspace.yaml` has correct `pythonpath`
- Run `pip install -e .` in project directory

### Assets Not Found
- Verify file names match asset definitions
- Check import statements in `definitions.py`

### Dependency Errors
- Silver can only depend on Bronze
- Gold can only depend on Silver
- Use `polster validate` to check

### Performance Issues
- Use Polars instead of pandas for large datasets
- Add `.persist()` for intermediate results
- Consider partitioning large files

## 📁 Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   ├── core/                    # Your transformation logic
│   │   ├── bronze_*.py         # Raw data ingestion
│   │   ├── silver_*.py         # Data cleaning/validation
│   │   ├── gold_*.py           # Business aggregations
│   │   ├── storage.py          # Storage abstraction
│   │   ├── settings.py         # Configuration
│   │   └── paths.py            # Path utilities
│   └── orchestration/          # Dagster setup
│       ├── definitions.py      # Asset definitions
│       ├── assets/             # Auto-generated assets
│       └── utils.py            # Helper functions
├── run_polster.py              # Main runner
├── workspace.yaml              # Dagster config
├── pyproject.toml              # Dependencies
└── README.md                   # This file
```

## 🎯 Next Steps

1. **Customize your assets** - Edit the generated files in `src/core/`
2. **Add more assets** - Use `polster add-asset` to expand your pipeline
3. **Remove assets if needed** - Use `polster remove-asset` to safely remove assets
4. **Set up scheduling** - Configure cron jobs or your orchestrator
4. **Add tests** - Test your transformations with `pytest`
5. **Deploy to production** - Set up cloud storage and monitoring

**Need help?** Check the main Polster CLI documentation or open an issue on GitHub.

Happy building! 🚀</content>
<parameter name="filePath">src/polster/templates/project/README.md