# 🚀 Your Python Based Fully Open Source Data Factory

## 💥 The Data Engineering Crisis (And Why It Must End)

Data engineering today is broken. Teams waste months wrestling with dependency hell, data quality disasters spiral out of control, and pipelines crumble under their own complexity. It's like trying to colonize Mars with duct tape and optimism - ambitious but fundamentally flawed.

Polster is data engineering reimagined from first principles. We enforce medallion architecture because it's the only logical way to transform data: Bronze (raw chaos) → Silver (refined quality) → Gold (business value). Dependencies converge naturally, quality gates are mandatory, and you get production pipelines that actually work.

This isn't incremental improvement. This is the data engineering revolution - built in Python, fully open source, and ready to scale to Mars-level data volumes.

## ⚡ From Zero to Data Factory in 5 Minutes (Seriously)

The old way: 6+ months of engineering time, endless dependency debates, quality disasters. The Polster way: 5 minutes to a production-ready data factory.

```bash
# Step 1: Get the blueprint (30 seconds)
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
cd ..

# Step 2: Build your factory (2 minutes)
polster init {{PROJECT_NAME}}

# Step 3: Test the production line (3 minutes)
cd {{PROJECT_NAME}}
python src/core/bronze_example.py   # Generate sample data
python src/core/silver_example.py   # Clean & transform
python src/core/gold_example.py     # Create business reports

# Step 4: Launch automated production!
python run_polster.py --ui  # 🚀 Your factory runs itself
```

Open http://127.0.0.1:3000 - watch your medallion pipeline materialize automatically, dependencies converge beautifully, and you get a monitoring dashboard that actually works.

## 🏗️ The Medallion Architecture Revolution

Medallion architecture isn't a buzzword - it's fundamental physics for data. Think of it like refining ore:

**Bronze Layer: Raw Ore** 📦
- Direct ingestion from sources (APIs, databases, files)
- No dependencies - pure, unfiltered data
- Preserves original fidelity for auditability
- Fan-out: Multiple sources feed the system

**Silver Layer: Refined Metal** ⚙️
- Cleaned, transformed, validated data
- Depends on bronze assets (enforced automatically)
- Business logic, data quality rules, standardization
- Convergence: Multiple bronzes consolidate into focused datasets

**Gold Layer: Finished Product** 📊
- Business-ready aggregations and analytics
- Depends on silver assets only (no shortcuts!)
- Decision-making datasets, reports, ML features
- Convergence: Silver transformations become business value

**Why This Matters:** Dependencies must converge. Gold can't depend on raw bronze - you need the refining process. Polster enforces this automatically because anything else is engineering malpractice.

## 📦 Your Production-Ready Factory Structure

```
{{PROJECT_NAME}}/
├── src/
│   ├── core/                    # Your data processing logic
│   │   ├── bronze_*.py         # Raw data extraction & ingestion
│   │   ├── silver_*.py         # Data cleaning & transformation
│   │   ├── gold_*.py           # Business aggregations & analytics
│   │   ├── storage.py          # Auto-scaling storage (local/cloud)
│   │   ├── settings.py         # Configuration management
│   │   └── paths.py            # Dynamic path resolution
│   └── orchestration/          # Dagster automation layer
│       ├── definitions.py      # Auto-discovering asset definitions
│       ├── assets/             # Layered asset organization
│       │   ├── bronze/         # Bronze asset definitions
│       │   ├── silver/         # Silver asset definitions
│       │   └── gold/           # Gold asset definitions
│       └── utils.py            # Helper functions
├── run_polster.py              # Your factory control panel
├── workspace.yaml              # Dagster configuration
├── pyproject.toml              # Dependencies & metadata
└── README.md                   # This guide
```

## 🚀 Adding Assets: The Future of Dependency Management

Stop manually tracking dependencies. Polster's intelligent system handles it for you:

```bash
# Bronze asset (simple, no dependencies)
polster add-asset --layer bronze --name customer_events

# Silver asset (interactive dependency selection)
polster add-asset --layer silver --name customer_profiles
# Polster prompts: "Select upstream bronze assets..."
# You choose: customer_events, order_history, etc.

# Gold asset (enforced silver-only dependencies)
polster add-asset --layer gold --name customer_lifetime_value
# Polster ensures you only select from silver assets
```

**What Gets Created:**
- `src/core/<layer>_<name>.py` - Your transformation logic
- `src/orchestration/assets/<layer>/run_<layer>_<name>.py` - Dagster asset definition
- Automatic dependency configuration in pipeline definitions

**Dependency Intelligence:**
- Bronze: No upstreams (ingestion only)
- Silver: Multiple bronze sources allowed
- Gold: Multiple silver sources allowed, bronze forbidden
- Converging flow prevents architectural violations

## 🔧 Configuration & Scaling

### Storage (Auto-Scaling to Any Size)
Edit `.env`:
```bash
# Local development
STORAGE_BACKEND=local

# Production cloud storage
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=your_storage_account
ADLS_CONTAINER=your_container
ADLS_BASE_PATH=polster/data
```

### Environment Scaling
- **Development:** Local storage, manual testing
- **Staging:** Cloud storage, automated testing
- **Production:** Multi-region cloud storage, scheduled pipelines

Polster scales from laptop to data center automatically.

## 🛠️ Factory Operations & Commands

```bash
# Core operations
python run_polster.py --ui           # Launch UI + auto-materialize
python run_polster.py                # Materialize all assets
python run_polster.py --no-materialize --ui  # UI only

# Development workflow
source .venv/bin/activate
pip install -e ".[dev]"
pytest                              # Run all tests
ruff format . && ruff check .      # Code quality
```

### Automated Scheduling
Polster sets up cron schedules automatically:
- Bronze assets: Daily at midnight (data ingestion)
- Silver/Gold: Triggered by upstream completion (converging flow)

## 🎯 Advanced: Extend Your Data Empire

### Custom Storage Backends
Add new storage systems by extending `storage.py`:
```python
def write_s3(df, layer, filename):
    # Your S3 implementation
    pass
```

### Custom Asset Types
Create specialized assets for ML, streaming, etc.

### Multi-Environment Deployments
Polster supports dev/staging/prod with environment-specific configs.

### Monitoring & Alerting
Built-in pipeline monitoring with failure notifications.

## 🏆 Why Polster Wins

**Speed:** 5 minutes vs 6+ months for traditional pipelines
**Quality:** Mandatory medallion layers prevent data disasters
**Simplicity:** No dependency management headaches
**Scalability:** From prototype to production without rewrites
**Open Source:** Community-driven, transparent, extensible

Data engineering shouldn't be a nightmare. With Polster, it's your competitive advantage.

**Ready to build the future of data?** `polster init your_project` and let's make history. 🚀

## Step 2: Explore your new factory
```bash
cd sales_analytics
```

## Step 3: Test the sample production line
```bash
python src/core/bronze_example.py   # 📦 Generate sample sales data
python src/core/silver_example.py   # ⚙️ Clean and transform the data
python src/core/gold_example.py     # 📊 Create business-ready reports
```

## Step 4: Launch automated production!
```bash
python run_polster.py --ui  # 🚀 Factory runs with automated production and monitoring dashboard
```

**Watch your data flow:** Open http://127.0.0.1:3000 to see your medallion pipeline in action - assets materialize automatically, dependencies converge beautifully, and you get a production-ready monitoring dashboard!

**Ready to customize?** Add your own assets with `polster add-asset` and let Polster handle the architectural heavy lifting.

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