# Polster CLI 🏗️

**The fastest way to bootstrap Polster data orchestration projects**

Polster CLI generates complete, production-ready data pipelines with just one command. Built on the Polster framework - a lightweight, Python-native alternative to heavy Spark-based architectures for small-to-medium data workloads.

## 🚀 Why Polster?

**Traditional Data Engineering Problems:**
- Complex setup and configuration
- Heavy dependencies on big data tools
- Steep learning curves
- Overkill for small-to-medium datasets

**Polster Solution:**
- **Lightweight**: Pure Python with Polars - no JVM overhead
- **Local-first**: Works great locally, scales to cloud
- **Medallion Architecture**: Bronze → Silver → Gold layers built-in
- **Dagster Integration**: Production-ready orchestration
- **5-minute setup**: From zero to working pipeline instantly

**Perfect for:**
- Data engineers wanting faster iteration
- Teams building data products
- ML engineers needing clean data pipelines
- Startups with limited infrastructure

## 🛠️ What Polster CLI Does

**Project Generation:**
- Creates complete project structure
- Sets up virtual environment with all dependencies
- Configures Dagster orchestration
- Includes example pipelines ready to run

**Asset Scaffolding:**
- Generates data processing code for each layer
- Creates Dagster asset definitions
- Includes commented examples and best practices
- Maintains consistent project structure

**Storage Abstraction:**
- Local filesystem (development)
- Azure Data Lake Storage (production)
- Automatic fallback and error handling

## 📦 Installation

```bash
# Install from PyPI (coming soon)
pip install polster

# Or install from source
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
```

**Requirements:**
- Python 3.13+
- Internet connection for initial setup

## ⚡ Quick Start (5 minutes)

```bash
# 1. Create your first project
polster init my_data_project

# 2. Start exploring (optional: auto-start Dagster)
polster init my_data_project --start-dagster

# 3. Add data processing assets
cd my_data_project
polster add-asset --layer bronze --name customers
polster add-asset --layer silver --name processed_customers
polster add-asset --layer gold --name customer_summary

# 4. Run your pipeline
dagster dev
```

**What you get:**
- ✅ Complete project structure
- ✅ Working virtual environment
- ✅ Sample data pipelines
- ✅ Dagster UI running
- ✅ Ready to customize and extend

## 📖 CLI Commands

### Initialize Projects
```bash
polster init <project_name> [OPTIONS]

# Examples
polster init my_project                    # Basic project
polster init my_project --git             # With git repo
polster init my_project --start-dagster   # Auto-start Dagster UI
polster init my_project --no-sample-assets # Minimal setup
```

### Add Assets
```bash
polster add-asset [OPTIONS]

# Examples
polster add-asset --layer bronze --name users        # Non-interactive
polster add-asset                                     # Interactive mode
```

**Options:**
- `--layer`: `bronze` | `silver` | `gold`
- `--name`: Asset name (snake_case)
- `--dry-run`: Preview without creating files

## 🏛️ Project Architecture

```
my_project/
├── src/
│   ├── core/                    # 🧠 Business Logic
│   │   ├── bronze_customers.py   # Raw data ingestion
│   │   ├── silver_customers.py   # Data cleaning/validation
│   │   ├── gold_customers.py     # Aggregations/analytics
│   │   ├── storage.py           # Local/ADLS abstraction
│   │   └── settings.py          # Configuration
│   └── orchestration/           # 🎯 Dagster Orchestration
│       ├── definitions.py       # Pipeline definitions
│       └── assets/              # Dagster assets
│           ├── bronze/          # Raw data layer
│           ├── silver/          # Clean data layer
│           └── gold/            # Analytics layer
├── .env.example                 # 🔧 Configuration template
├── run_dagster.py              # 🚀 Dagster launcher
└── pyproject.toml              # 📦 Package config
```

**Layer Explanations:**
- **Bronze**: Raw data ingestion from sources
- **Silver**: Data cleaning, validation, transformation
- **Gold**: Business analytics, aggregations, reporting

## 💾 Storage Backends

**Local Development (Default):**
```bash
STORAGE_BACKEND=local
# Data stored in ./data/ directory
```

**Azure Data Lake Storage (Production):**
```bash
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=your_storage_account
ADLS_CONTAINER=your_container
ADLS_BASE_PATH=polster/data
ADLS_ACCOUNT_KEY=your_account_key
```

**Automatic Features:**
- ✅ Fallback to local if ADLS credentials missing
- ✅ Timestamped files prevent overwrites
- ✅ Cross-platform path handling

## 🎯 Dagster Orchestration

**Automatic Scheduling:**
- Bronze assets run daily at midnight
- Silver/gold assets trigger on upstream completion
- Configurable via `src/orchestration/definitions.py`

**Manual Execution:**
```bash
# Start Dagster UI
dagster dev

# Run specific assets
dagster asset materialize --select run_bronze_customers

# Run entire layers
dagster asset materialize --select "*bronze*"
```

**Benefits:**
- ✅ Production-ready scheduling
- ✅ Dependency management
- ✅ Web-based monitoring
- ✅ Asset lineage tracking

## 🧪 Testing & Quality

**Comprehensive Testing:**
- 50/50 tests passing across all features
- CLI functionality fully validated
- Project generation tested end-to-end
- Asset scaffolding verified
- See `test.md` for complete test results

**Code Quality:**
- Type hints and modern Python practices
- Ruff for linting/formatting
- Cross-platform compatibility
- Comprehensive error handling

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .
ruff check .
```

## 🤝 Contributing

**Issues & Features:**
- Bug reports: [GitHub Issues](https://github.com/sultanaltair96/polster-cli-grok/issues)
- Feature requests: GitHub Discussions
- Code contributions: Pull Requests

**Development Guidelines:**
- Python 3.13+ required
- Tests required for new features
- Ruff for code formatting
- Comprehensive documentation

## 📚 Resources

- **GitHub**: [polster-cli](https://github.com/sultanaltair96/polster-cli-grok)
- **Test Results**: [test.md](test.md) - Complete testing documentation
- **Issues**: [Report Bugs](https://github.com/sultanaltair96/polster-cli-grok/issues)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for data engineers who want to focus on data, not infrastructure.**