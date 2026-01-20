# 🚀 YOUR PYTHON BASED FULLY OPEN SOURCE DATA FACTORY

## 💥 THE DATA ENGINEERING NIGHTMARE (AND WHY IT MUST DIE)

Let's be brutally honest: Data engineering today is a complete disaster. Teams burn 6+ months building pipelines that fail spectacularly. Dependencies become spaghetti code nightmares. Data quality? Forget about it. It's like trying to build the Starship with Excel spreadsheets and prayers.

The problem isn't the tools. The problem is fundamental. We need to rethink data engineering from first principles.

Polster is a Python-based, open-source data factory that enforces medallion architecture at the framework level.

Key principles of enforcement:
- Bronze assets cannot depend on anything.
- Silver assets can only depend on bronze.
- Gold assets can only depend on silver.
- Quality checks are first-class, not optional.

This changes everything. Welcome to the data engineering revolution.

## ⚡ FROM ZERO TO DATA EMPIRE IN 5 MINUTES

The old world: Endless meetings about dependencies. Manual quality checks. Pipelines that break on day one.

The new world: Type a few commands. Get a factory that runs itself.

```bash
# 1. Get the revolution (30 seconds)
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e ".[dev]"
cd ..

# 2. Build your empire (2 minutes)
polster init {{PROJECT_NAME}}

# 3. Test the machinery (3 minutes)
cd {{PROJECT_NAME}}
python src/core/bronze_example.py   # Raw data flows in
python src/core/silver_example.py   # Quality transformation
python src/core/gold_example.py     # Business intelligence emerges

# 4. Launch automated domination!
python run_polster.py --ui  # 🚀 Your empire runs forever
```

BOOM. Open http://127.0.0.1:3000. Watch your medallion pipeline materialize automatically. Dependencies converge perfectly. Monitoring dashboard included. This used to take armies of engineers. Now it's 5 minutes.

## 🏗️ MEDALLION ARCHITECTURE: THE ONLY WAY THAT MAKES SENSE

Medallion architecture isn't theory. It's fundamental. Think of data like physical materials:

**BRONZE LAYER: RAW ORE** ⛰️
- Unprocessed, unfiltered, unapologetic data
- Direct from sources: APIs, databases, streams, files
- No dependencies (obviously)
- Fan-out: Multiple sources feed the beast

**SILVER LAYER: REFINED METAL** ⚙️
- Cleaned, transformed, validated, standardized
- Depends ONLY on bronze (enforced by physics)
- Business logic, quality gates, data contracts
- Convergence: Multiple bronzes become focused datasets

**GOLD LAYER: WEAPONS-GRADE ALLOY** 🏆
- Business-ready, decision-making, revenue-generating
- Depends ONLY on silver (no shortcuts to raw ore!)
- Analytics, ML features, executive dashboards
- Convergence: Silver becomes competitive advantage

**WHY THIS WORKS:** Dependencies MUST converge. You can't build rockets from raw ore. You need refining. Polster enforces this automatically because anything else is engineering suicide.

## 📦 YOUR PRODUCTION EMPIRE BLUEPRINT

```
{{PROJECT_NAME}}/
├── src/
│   ├── core/                    # Your transformation empire
│   │   ├── bronze_*.py         # Raw data conquest
│   │   ├── silver_*.py         # Quality domination
│   │   ├── gold_*.py           # Business supremacy
│   │   ├── storage.py          # Auto-scaling data vaults
│   │   ├── settings.py         # Empire configuration
│   │   └── paths.py            # Dynamic territory mapping
│   └── orchestration/          # Automation command center
│       ├── definitions.py      # Auto-discovering asset empire
│       ├── assets/             # Layered asset legions
│       │   ├── bronze/         # Bronze asset warriors
│       │   ├── silver/         # Silver asset commanders
│       │   └── gold/           # Gold asset emperors
│       └── utils.py            # Imperial utilities
├── run_polster.py              # Your command throne
├── workspace.yaml              # Battle strategy config
├── pyproject.toml              # Imperial dependencies
└── README.md                   # Your conquest manual
```

## 🚀 ASSET CONQUEST: INTELLIGENT DEPENDENCY DOMINATION

Forget manual dependency tracking. Polster's AI handles the empire-building:

```bash
# Bronze conquest (pure, no dependencies)
polster add-asset --layer bronze --name enemy_intel

# Silver campaign (strategic dependency selection)
polster add-asset --layer silver --name battle_plans
# Polster: "Select bronze assets for conquest..."
# You: enemy_intel, supply_lines, troop_movements

# Gold supremacy (enforced silver-only dependencies)
polster add-asset --layer gold --name victory_metrics
# Polster: Only silver assets allowed - no raw data shortcuts!
```

**Automatic Empire Building:**
- `src/core/<layer>_<name>.py` - Your transformation logic
- `src/orchestration/assets/<layer>/run_<layer>_<name>.py` - Dagster asset definition
- Dependencies wired automatically in pipeline definitions

**Dependency Intelligence (Enforced by AI):**
- Bronze: No upstreams (sovereign territories)
- Silver: Multiple bronze conquests allowed
- Gold: Multiple silver victories allowed, bronze forbidden
- Convergence prevents empire collapse

## 🔧 CONFIGURATION & SCALING TO INTERSTELLAR LEVELS

### Storage Empires (Scale to Infinity)
Edit `.env`:
```bash
# Local development outposts
STORAGE_BACKEND=local

# Galactic cloud storage
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=your_imperial_account
ADLS_CONTAINER=your_vault
ADLS_BASE_PATH=polster/conquests
```

### Environment Conquest
- **Development:** Local testing grounds
- **Staging:** Cloud battle simulations
- **Production:** Multi-galaxy cloud empires with automated scheduling

Polster scales from laptop to interplanetary data centers.

## 🛠️ EMPIRE OPERATIONS & COMMAND CODES

```bash
# Core imperial operations
python run_polster.py --ui           # Launch throne room + auto-conquests
python run_polster.py                # Execute all campaigns
python run_polster.py --no-materialize --ui  # Throne room only

# Imperial development workflow
source .venv/bin/activate
pip install -e ".[dev]"
pytest                              # Test imperial defenses
ruff format . && ruff check .      # Maintain code supremacy
```

### Automated Imperial Scheduling
- Bronze campaigns: Daily midnight conquests (data ingestion)
- Silver/Gold: Triggered by upstream victories (converging dominance)

## 🎯 ADVANCED: EXPAND YOUR GALACTIC EMPIRE

### Custom Storage Conquests
Extend `storage.py` for new territories:
```python
def conquer_s3(df, layer, filename):
    # Your S3 domination strategy
    pass
```

### Specialized Asset Legions
Create ML, streaming, real-time asset warriors.

### Multi-Realm Deployments
Dev/Staging/Prod with realm-specific configurations.

### Imperial Monitoring & Alerts
Built-in pipeline surveillance with victory/failure notifications.

## 🏆 WHY POLSTER CONQUERS ALL

**SPEED:** 5 minutes vs 6+ months of traditional engineering hell
**QUALITY:** Mandatory medallion prevents data disasters
**SIMPLICITY:** AI handles dependencies, you focus on conquest
**SCALABILITY:** From prototype to galactic empire without rebuilding
**OPEN SOURCE:** Community-driven, transparent, infinitely extensible

Data engineering shouldn't be a death march. With Polster, it's your path to domination.

**Ready to conquer the data universe?** `polster init your_empire` and let's build something that changes everything.

🚀 MAKE DATA GREAT AGAIN 🚀

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

### Adding a New Asset with the Polster CLI

Use the `polster add-asset` command to add assets while maintaining Polster's structured Medallion architecture. For example:

```bash
# Add a new Bronze-layer asset
polster add-asset --layer bronze --name raw_data_ingestion

# Add a new Silver-layer asset
polster add-asset --layer silver --name cleaned_data --dependencies bronze_asset_1,bronze_asset_2

# Add a new Gold-layer asset
polster add-asset --layer gold --name analytics_dashboard --dependencies silver_asset_1,silver_asset_2
```

Polster will guide you interactively to ensure asset dependencies follow the Medallion principles. This process automatically generates two files:
- `src/core/<layer>_<name>.py`: The transformation logic.
- `src/orchestration/assets/<layer>/<layer>_<name>.py`: The corresponding Dagster asset definition.

### Dependency Management

Polster strictly enforces Medallion architecture principles:
- Bronze assets serve as the data ingestion layer and cannot depend on anything else.
- Silver assets consolidate and clean data from one or more Bronze assets.
- Gold assets aggregate and refine insights, relying only on Silver-layer outputs.

This ensures a clear, predictable data lineage while maintaining data quality at each stage.

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