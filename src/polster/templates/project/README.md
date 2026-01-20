# {{PROJECT_NAME}}

A Polster data orchestration project.

## Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Start Dagster UI (materializes assets automatically)
python run_polster.py --ui
```

## Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   ├── core/                    # Data processing logic
│   │   ├── bronze_example.py     # Bronze layer example
│   │   ├── silver_example.py     # Silver layer example
│   │   ├── gold_example.py       # Gold layer example
│   │   ├── storage.py            # Storage abstraction (local/ADLS)
│   │   ├── settings.py           # Configuration
│   │   └── paths.py              # Path utilities
│   └── orchestration/            # Dagster orchestration
│       ├── definitions.py        # Asset definitions and scheduling
│       ├── utils.py              # Helper functions
│       └── assets/               # Dagster assets
│           ├── bronze/
│           ├── silver/
│           └── gold/
 ├── .env.example                  # Environment variables template
 ├── run_polster.py               # Polster runner script
 └── README.md
```

## Adding New Assets

Use the Polster CLI to add new assets with automatic dependency management:

```bash
# Add a new bronze asset (no dependencies)
polster add-asset --layer bronze --name customers

# Add a new silver asset (interactive dependency selection from bronze)
polster add-asset --layer silver --name customers_cleaned

# Add a new gold asset (interactive dependency selection from silver)
polster add-asset --layer gold --name customer_summary

# Or use interactive mode
polster add-asset
```

This creates two files:
- `src/core/<layer>_<name>.py` - Your data processing logic
- `src/orchestration/assets/<layer>/run_<layer>_<name>.py` - Dagster asset definition

**Dependency Management:** Polster enforces medallion architecture principles:
- **Bronze assets:** No upstream dependencies
- **Silver assets:** Can depend on multiple bronze assets
- **Gold assets:** Can depend on multiple silver assets (not bronze)

When creating silver/gold assets, you'll be prompted to select upstream dependencies from the appropriate layer.

## Architecture & Dependencies

Polster implements the **medallion architecture** for data transformation, ensuring **converging dependencies** that create clean, maintainable data pipelines:

### Data Flow & Convergence Structure
```
Bronze Layer: [raw_data_1, raw_data_2, raw_data_3]  ← Multiple sources, no dependencies
     ↓ (fan-out: raw ingestion)
Silver Layer: [cleaned_data_1, cleaned_data_2]      ← Can depend on multiple bronze assets
     ↓ (converge: data quality & transformation)
Gold Layer: [business_summary]                       ← Can depend on multiple silver assets
```

### Layer Responsibilities

#### Bronze Layer
- **Purpose:** Raw, unprocessed data ingestion
- **Dependencies:** None (direct from sources)
- **Value:** Preserves original data fidelity

#### Silver Layer
- **Purpose:** Cleaned and transformed data
- **Dependencies:** Multiple bronze assets allowed
- **Value:** Data quality gates, business logic, standardization
- **Convergence:** Combines multiple raw sources into focused datasets

#### Gold Layer
- **Purpose:** Business-ready aggregated data
- **Dependencies:** Multiple silver assets allowed (not bronze)
- **Value:** Analytics, reporting, decision-making datasets
- **Convergence:** Business-level aggregations from processed data

### Dependency Enforcement & Benefits

**Architectural Guarantees:**
- Prevents gold assets from bypassing silver transformations
- Ensures data quality through mandatory cleaning steps
- Maintains clear lineage and governance
- Guides users toward best practices automatically

**Convergence Advantages:**
- **Data Consolidation:** Natural aggregation points prevent data sprawl
- **Quality Assurance:** Each layer adds validation and transformation
- **Performance:** Reduces redundant processing in downstream layers
- **Maintainability:** Clear separation of concerns and dependencies

When adding silver/gold assets, you'll be prompted to select upstream dependencies from the immediate upstream layer only, ensuring proper convergence flow.

## Storage Configuration

Edit `.env` to configure storage:

```bash
# Local storage (default)
STORAGE_BACKEND=local

# ADLS storage
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=your_storage_account
ADLS_CONTAINER=your_container
ADLS_BASE_PATH=polster/data
ADLS_ACCOUNT_KEY=your_account_key
```

## Development

```bash
# Install dependencies
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .
ruff check .
```

## Dagster Commands

```bash
# Start UI (recommended - includes automatic materialization)
python run_polster.py --ui

# Materialize all assets only
python run_polster.py

# Start UI without materialization
python run_polster.py --no-materialize --ui

# Alternative: Materialize specific assets manually
# (Use run_polster.py for most operations)
```