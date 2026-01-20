# Polster: Opinionated Framework for Data Engineering

Polster is an open-source framework designed to simplify ETL processes and data orchestration. By enforcing a structured approach based on Medallion Architecture principles, it helps teams build reliable, scalable, and maintainable data pipelines.

## The Challenges in Data Engineering

Many data platforms face challenges due to architecture drift and lack of standards:
- **Broken dependency graphs** leading to fragile systems.
- **Invisible coupling** causing untraceable issues.
- **Late-stage data quality checks**, resulting in errors surfacing in production.
- **Pipelines that are difficult to debug or extend.**

Polster helps address these challenges by combining flexibility with a disciplined approach to organization and pipeline management.

---

## Why Polster?

Unlike generic orchestrators, Polster is opinionated and provides tools that:
- **Enforce structure:** Bronze → Silver → Gold layers ensure clean dependencies.
- **Streamline workflows:** The CLI simplifies common pipeline operations.
- **Improve maintainability:** Guided practices reduce cognitive load.
- **Enhance quality:** Early and automated checks prevent downstream errors.

## Key Features

- **Medallion Architecture Enforcement**: Built-in enforcement of the Bronze, Silver, and Gold data layers.
- **Dependency Management**: Intelligent handling of asset dependencies ensures consistency.
- **CLI Tools for Simplicity**: Commands are designed to reduce manual effort and guide best practices.
- **Production-Ready by Default**: Focused on creating pipelines that are robust and production-quality from the start.

---

## Understanding Medallion Architecture

Medallion Architecture is central to Polster’s design. It structures data processing into three layers:

### Bronze Layer: Raw Data
- **Purpose:** Ingest and store raw data without transformation.
- **Sources:** APIs, databases, files, streams.
- **Role:** Act as the foundation for downstream transformations, preserving original fidelity for auditing.

### Silver Layer: Cleaned and Validated Data
- **Purpose:** Apply quality checks such as schema validation and deduplication, and standardize formats.
- **Dependencies:** Multiple bronze sources.
- **Role:** Act as a convergence point to produce trusted datasets for analysis.

### Gold Layer: Aggregated and Enriched Data
- **Purpose:** Aggregate data into business-level metrics, analytics, and dashboards.
- **Dependencies:** Multiple silver sources.
- **Role:** Generate insights ready for decision-making workflows.

Polster ensures these layers are followed, preventing architecture drift and guaranteeing lineage clarity.

---

## Getting Started with Polster

### Installation

Install Polster via pip:

```bash
pip install polster
```

Or clone the repository to work with the latest version:

```bash
git clone https://github.com/sultanaltair96/polster-cli-grok
cd polster-cli-grok
pip install -e "[dev]"
```

### Initialize a New Project

Create a new data project with a single command:

```bash
polster init my_project
```

### Example Pipeline Workflow

Navigate to your project folder and execute the following examples to explore each Medallion layer:

```bash
cd my_project

# Ingest raw data into the Bronze layer
python src/core/bronze_example.py

# Apply transformations and validations for the Silver layer
python src/core/silver_example.py

# Aggregate data for business intelligence in the Gold layer
python src/core/gold_example.py
```

### Launch the Polster Dashboard

Polster comes with a built-in monitoring and orchestration dashboard:

```bash
python run_polster.py --ui
```

---

## What Polster Is Not

Polster is not:
- **A low-code tool**: It’s designed for Python users who need full control over transformation logic.
- **A generic orchestrator**: It enforces Medallion Architecture principles.
- **Notebook-first**: Focus is on production-ready scripts rather than experimentation.
- **An all-in-one analytics tool**: It specializes in building data pipelines, leaving analysis to other layers.

Polster focuses on being a reliable framework for creating structured, maintainable data workflows.

---

## Contributing

We welcome contributions! Whether it’s reporting a bug, requesting a feature, or improving documentation, please check out our [GitHub repository](https://github.com/sultanaltair96/polster-cli-grok) to get involved.

---

## License

Polster is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
