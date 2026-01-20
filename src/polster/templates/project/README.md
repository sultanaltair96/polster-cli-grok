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

Use the Polster CLI to add new assets:

```bash
# Add a new bronze asset
polster add-asset
# Follow the prompts for layer and name
```

This creates two files:
- `src/core/<layer>_<name>.py` - Your data processing logic
- `src/orchestration/assets/<layer>/run_<layer>_<name>.py` - Dagster asset definition

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