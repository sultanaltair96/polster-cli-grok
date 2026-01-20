# Polster: A Professional Framework for Data Engineering

Polster is an open-source, Python-based framework designed to simplify ETL processes and data pipeline orchestration. With an opinionated approach grounded in the Medallion Architecture, Polster provides teams with a structured, reproducible, and reliable way to build scalable data workflows.

## Why Polster?

Data engineering is complex and prone to issues like:
- **Broken dependency graphs**, leading to unmaintainable pipelines.
- **Invisible data coupling**, making debugging and enhancements challenging.
- **Late-stage data quality checks**, delaying error detection to production.
- **Ad-hoc workflows**, creating inconsistency across pipelines.

Polster solves these challenges by enforcing simple, predictable, and repeatable patterns for data workflows. It is ideal for teams looking to:
- **Reduce maintenance overhead**: Enforced dependency rules keep systems clean.
- **Standardize best practices**: Automatic alignment with Medallion Architecture principles.
- **Accelerate delivery**: Easy-to-use CLI tools reduce onboarding friction.
- **Enhance data quality**: Integrated validation ensures clean data at every stage.

---

## Key Features

- **Medallion Architecture**: Organizes data transformation into Bronze, Silver, and Gold layers to improve consistency and quality.
- **Dependency Management**: Automatically enforces best practices for pipeline dependencies.
- **Command-Line Simplicity**: A robust CLI lets you manage projects, assets, and pipelines effortlessly.
- **Production-First Design**: Designed for scalable, reproducible pipelines that work seamlessly in production environments.

---

## Understanding Medallion Architecture

### Bronze Layer: Raw Data
- **Purpose**: Stores unprocessed, raw data.
- **Examples**: Data from APIs, databases, logs, and files.
- **Role**: Source of truth and audit trail.

### Silver Layer: Cleaned Data
- **Purpose**: Applies validation, deduplication, and transformations.
- **Examples**: Clean, schema-validated datasets ready for analysis.
- **Role**: Normalizes and refines data from the Bronze layer.

### Gold Layer: Business-Ready Data
- **Purpose**: Aggregates and enriches data into actionable insights.
- **Examples**: Metrics dashboards, machine learning features, and key reports.
- **Role**: Generates insights that drive decision-making.

Medallion Architecture ensures a clear lineage and promotes maintainability. Polster enforces rules to prevent common architectural pitfalls, such as misaligned dependencies.

---

## Getting Started

### Installation

Install Polster using pip:

```bash
pip install polster
```

Alternatively, for the latest development version:

```bash
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e "[dev]"
```

### Create a New Project

Set up a new Polster project with one command:

```bash
polster init my_project
```

This will scaffold a project that adheres to Medallion Architecture.

### Add Assets to Your Project

Define new assets for different layers using the `polster add-asset` command:

```bash
# Add a Bronze asset for raw data ingestion
polster add-asset --layer bronze --name ingest_logs

# Add a Silver asset, dependent on Bronze
polster add-asset --layer silver --name clean_logs --dependencies ingest_logs

# Add a Gold asset, dependent on Silver
polster add-asset --layer gold --name reports --dependencies clean_logs
```

Polster ensures compliance with Medallion rules, prompting you to align dependencies correctly.

### Run Data Pipelines

Explore how Medallion Architecture works by running sample transformations:

```bash
cd my_project

# Bronze: Ingest raw data
python src/core/bronze_example.py

# Silver: Clean and validate data
python src/core/silver_example.py

# Gold: Aggregate and summarize data
python src/core/gold_example.py
```

### Launch the Polster Dashboard

Monitor and orchestrate your data pipelines with the built-in dashboard:

```bash
python run_polster.py --ui
```

The dashboard provides visibility into the state of your pipelines, offering insights into execution and dependencies.

---

## What Polster Is Not

While powerful, Polster is focused and opinionated. It is not:
- **A low-code or no-code tool**: Polster is Python-first and tailored for engineers.
- **A generic orchestrator**: It enforces Medallion Architecture principles rigorously.
- **A general-purpose analytics platform**: It focuses on building pipelines, not visualizations.
- **Notebook-first**: Designed for production-quality data workflows, not experimentation.

---

## Contributing

We welcome community contributions to improve Polster further. Whether it’s reporting a bug, suggesting features, or contributing code, visit our [GitHub repository](https://github.com/sultanaltair96/polster-cli-grok) to get involved.

## License

Polster is available under the MIT License. See the [LICENSE](LICENSE) file for more information.