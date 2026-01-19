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
- Creates complete project structure with dedicated data directories
- Sets up virtual environment with all dependencies
- Configures automated Dagster orchestration with eager execution
- Includes working example pipelines ready to run

**Asset Scaffolding:**
- Generates data processing code for each layer with direct execution support
- Creates Dagster asset definitions with automated dependencies
- Includes comprehensive commented examples and clear implementation guidance
- Supports incremental development with immediate testing capabilities

**Direct Script Execution:**
- Run any core script directly for testing and debugging from any directory
- Flexible imports handle both Dagster orchestration and standalone execution
- Zero import errors across all execution contexts

**Automated Data Pipelines:**
- Bronze assets run daily at 12:01 AM via cron scheduling
- Silver and gold assets automatically trigger when upstream data completes
- Explicit dependencies ensure reliable data flow through medallion layers

**Storage Abstraction:**
- Local filesystem (development) with dedicated bronze/silver/gold directories
- Azure Data Lake Storage (production) with automatic fallbacks
- Robust I/O handling and cross-platform path resolution

## 📦 Installation

```bash
# Install from PyPI
pip install polster

# Or install from source
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"

# Or install from source
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
```

**Requirements:**
- Python 3.12+
- Internet connection for initial setup

## ⚡ Quick Start (5 minutes)

```bash
# 1. Create your first project
polster init my_data_project

# 2. Explore the generated project
cd ../my_data_project  # Note: created in parent directory

# 3. Test direct script execution (works from any directory!)
python src/core/bronze_example.py  # ✅ Generates sample data
python src/core/silver_example.py  # ✅ Transforms data
python src/core/gold_example.py    # ✅ Creates aggregations

# 4. Add custom data processing assets
polster add-asset --layer bronze --name customers
polster add-asset --layer silver --name processed_customers
polster add-asset --layer gold --name customer_summary

# 5. Test your custom assets directly
python src/core/bronze_customers.py  # ✅ Ready for testing
python src/core/silver_processed_customers.py  # ✅ Ready for testing
python src/core/gold_customer_summary.py  # ✅ Ready for testing

# 6. Run the full automated pipeline
dagster dev  # Launches UI with orchestrated data flow
```

**What you get:**
- ✅ Complete project structure with dedicated data directories
- ✅ Working virtual environment with all dependencies
- ✅ Automated pipeline orchestration (bronze → silver → gold)
- ✅ Direct script execution for testing and debugging
- ✅ Comprehensive examples with clear implementation guidance
- ✅ Production-ready storage abstraction (local + cloud)
- ✅ Dagster UI with automated scheduling and monitoring

## 📖 CLI Commands

### Initialize Projects
```bash
polster init <project_name> [OPTIONS]

# Examples
polster init my_project                    # Basic project (created in parent directory)
polster init my_project --git             # With git repo
polster init my_project --start-dagster   # Auto-start Dagster UI
polster init my_project --no-sample-assets # Minimal setup
```

**Note**: Projects are created in the parent directory (next to the current folder) to keep your workspace organized.

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
├── data/                        # 📊 Dedicated data directories
│   ├── bronze/                  # Raw data storage
│   ├── silver/                  # Cleaned data storage
│   └── gold/                    # Aggregated data storage
├── src/
│   ├── core/                    # 🧠 Business Logic
│   │   ├── bronze_example.py     # Working bronze example
│   │   ├── bronze_customers.py   # Your custom bronze assets
│   │   ├── silver_example.py     # Working silver example
│   │   ├── silver_customers.py   # Your custom silver assets
│   │   ├── gold_example.py       # Working gold example
│   │   ├── gold_summary.py       # Your custom gold assets
│   │   ├── storage.py           # Multi-backend storage abstraction
│   │   ├── paths.py             # Dynamic path resolution
│   │   └── settings.py          # Configuration
│   └── orchestration/           # 🎯 Dagster Orchestration
│       ├── definitions.py       # Automated pipeline definitions
│       └── assets/              # Dagster asset definitions
│           ├── bronze/          # Bronze layer orchestration
│           ├── silver/          # Silver layer orchestration
│           └── gold/            # Gold layer orchestration
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

**Automated Scheduling & Execution:**
- **Bronze Layer**: Runs daily at 12:01 AM via cron scheduling
- **Silver Layer**: Automatically triggers when bronze assets complete (eager execution)
- **Gold Layer**: Automatically triggers when silver assets complete (eager execution)
- **Dependencies**: Explicit asset relationships ensure reliable data flow

**Development Workflow:**
```bash
# 1. Direct script testing (works from any directory)
python src/core/bronze_customers.py  # Test individual components
python src/core/silver_customers.py  # Test transformations
python src/core/gold_summary.py      # Test aggregations

# 2. Full pipeline orchestration
dagster dev  # Launch automated pipeline

# 3. Manual execution when needed
dagster asset materialize --select run_bronze_customers
dagster asset materialize --select "*bronze*"  # Run all bronze assets
```

**Benefits:**
- ✅ Production-ready scheduling
- ✅ Dependency management
- ✅ Web-based monitoring
- ✅ Asset lineage tracking

## 🔧 Direct Script Execution

**Run any core script directly for testing and debugging:**

```bash
# From project root (recommended)
cd my_data_project
python src/core/bronze_example.py   # ✅ Generates sample data
python src/core/silver_example.py   # ✅ Transforms data
python src/core/gold_example.py     # ✅ Creates aggregations

# From anywhere in the project
python /path/to/project/src/core/bronze_customers.py  # ✅ Works!

# Scripts automatically handle imports for both:
# - Dagster orchestration (relative imports)
# - Direct execution (absolute imports with path resolution)
```

**Benefits:**
- ✅ **Immediate testing**: Run scripts at any development stage
- ✅ **Zero import errors**: Automatic path resolution from any directory
- ✅ **Incremental development**: Test components before full pipeline integration
- ✅ **Debugging support**: Isolate and fix issues in individual scripts
- ✅ **Flexible workflow**: No need to navigate to specific directories

**How it works**: Scripts use flexible import logic to automatically detect execution context and adjust import paths accordingly.

## 🧪 Testing & Quality

**Comprehensive Testing:**
- ✅ Direct script execution validated across all contexts
- ✅ Automated pipeline orchestration verified
- ✅ Multi-storage backend functionality tested
- ✅ Asset scaffolding with commented examples confirmed
- ✅ Cross-platform compatibility verified
- See `test.md` for complete test results

**Key Improvements:**
- **Direct Execution**: 100% of core scripts runnable from any directory
- **Import Resolution**: Zero import errors across execution contexts
- **Pipeline Automation**: Complete bronze→silver→gold flow with eager triggering
- **Storage Flexibility**: Seamless local/cloud backend switching
- **Developer Experience**: Clear guidance and immediate testing capabilities

**Code Quality:**
- Type hints and modern Python practices
- Ruff for linting/formatting
- Cross-platform compatibility
- Comprehensive error handling

## 🚀 Development Workflow

**Complete development cycle with Polster:**

### **Phase 1: Project Setup**
```bash
polster init my_project  # Creates project in parent directory
cd ../my_project         # Navigate to new project
```

### **Phase 2: Explore Examples**
```bash
# Test the working examples
python src/core/bronze_example.py  # See sample data generation
python src/core/silver_example.py  # See data transformation
python src/core/gold_example.py    # See data aggregation

# View generated data
ls -la data/bronze/  # Bronze layer data
ls -la data/silver/  # Silver layer data
ls -la data/gold/    # Gold layer data
```

### **Phase 3: Add Custom Assets**
```bash
# Create your own assets
polster add-asset --layer bronze --name customers
polster add-asset --layer silver --name processed_customers
polster add-asset --layer gold --name customer_analytics
```

### **Phase 4: Develop Incrementally**
```bash
# Edit and test individual scripts
# Uncomment TODO examples and customize for your data
python src/core/bronze_customers.py  # Test data ingestion
python src/core/silver_processed_customers.py  # Test transformations
python src/core/gold_customer_analytics.py  # Test aggregations
```

### **Phase 5: Full Pipeline Integration**
```bash
# Launch orchestrated pipeline
dagster dev

# Monitor automated execution in Dagster UI
# Bronze runs at 12:01 AM, others trigger automatically
```

### **Phase 6: Production Deployment**
```bash
# Configure storage backend
echo "STORAGE_BACKEND=adls" >> .env
echo "ADLS_ACCOUNT_NAME=your_account" >> .env
# Add other ADLS credentials...

# Deploy to production environment
# Pipeline automatically uses cloud storage
```

**Key Benefits:**
- ✅ **Start immediately**: Working examples show the complete flow
- ✅ **Test continuously**: Direct execution at every development stage
- ✅ **Scale seamlessly**: Same code works locally and in production
- ✅ **Debug easily**: Isolate issues in individual components
- ✅ **Deploy confidently**: Automated pipelines with monitoring

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

## 🔍 Troubleshooting

### **Direct Script Execution Issues**

**Problem**: `ImportError` when running scripts directly
```bash
python src/core/bronze_customers.py
# ImportError: attempted relative import with no known parent package
```

**Solution**: Scripts must be run from within the project directory structure. The dynamic path resolution needs to find the `src` folder.

**Correct usage**:
```bash
# From project root (recommended)
cd my_data_project
python src/core/bronze_customers.py  # ✅ Works

# From anywhere (with full path)
python /full/path/to/my_data_project/src/core/bronze_customers.py  # ✅ Works
```

### **Dagster Import Errors**

**Problem**: Dagster fails to load with import errors

**Solution**: Ensure you're in the correct directory and virtual environment is activated:
```bash
cd my_data_project
source .venv/bin/activate
dagster dev  # ✅ Should work
```

### **Storage Backend Issues**

**Problem**: ADLS storage not working, falls back to local

**Solution**: Check environment variables:
```bash
# Required for ADLS
export STORAGE_BACKEND=adls
export ADLS_ACCOUNT_NAME=your_account
export ADLS_ACCOUNT_KEY=your_key
export ADLS_CONTAINER=your_container
```

**Missing credentials**: Automatically falls back to local storage with a warning.

### **Project Creation in Wrong Location**

**Problem**: Project created in current directory instead of parent

**Solution**: This is the new default behavior. Projects are created in the parent directory to keep your workspace organized. The old behavior was creating projects inside the current directory.

### **Asset Template Issues**

**Problem**: New assets don't have the expected structure

**Solution**: Ensure you're using the latest version. New assets include:
- Comprehensive commented examples
- `if __name__ == "__main__":` blocks for direct execution
- Clear TODO guidance for implementation

### **Virtual Environment Issues**

**Problem**: Scripts fail with missing dependencies

**Solution**: Always activate the project's virtual environment:
```bash
source my_data_project/.venv/bin/activate  # On macOS/Linux
# my_data_project\.venv\Scripts\activate    # On Windows
```

## 🤝 Contributing

**Issues & Features:**
- Bug reports: [GitHub Issues](https://github.com/sultanaltair96/polster-cli-grok/issues)
- Feature requests: GitHub Discussions
- Code contributions: Pull Requests

**Development Guidelines:**
- Python 3.12+ required
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

## 🎉 Key Features Summary

- **🚀 Direct Script Execution**: Run any core script from anywhere for testing
- **⚡ Automated Pipelines**: Bronze→Silver→Gold with eager triggering
- **☁️ Multi-Storage Support**: Local + Azure Data Lake with fallbacks
- **🔧 Zero-Friction Development**: Immediate testing at every stage
- **📊 Production Ready**: Cron scheduling, monitoring, and lineage tracking
- **🛠️ Exceptional DX**: Comprehensive examples with clear implementation guidance

**Built with ❤️ for data engineers who want to focus on data, not infrastructure.**

---

*Polster CLI v0.1.0 - Production-Ready Data Engineering Made Simple* ✨