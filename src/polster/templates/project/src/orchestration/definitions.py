"""Dagster definitions for Polster data pipelines.

This module automatically loads all assets and configures scheduling for bronze
assets with eager materialization for silver and gold layers.
"""

from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    ScheduleDefinition,
    AssetSelection,
)

# Conditionally import asset modules
bronze_modules = []
silver_modules = []
gold_modules = []

try:
    from .assets.bronze import run_bronze_example

    bronze_modules.append(run_bronze_example)
except ImportError:
    pass

try:
    from .assets.silver import run_silver_example

    silver_modules.append(run_silver_example)
except ImportError:
    pass

try:
    from .assets.gold import run_gold_example

    gold_modules.append(run_gold_example)
except ImportError:
    pass

# Load assets from modules if they exist
bronze_assets = (
    load_assets_from_modules(bronze_modules, group_name="bronze")
    if bronze_modules
    else []
)
silver_assets = (
    load_assets_from_modules(silver_modules, group_name="silver")
    if silver_modules
    else []
)
gold_assets = (
    load_assets_from_modules(gold_modules, group_name="gold") if gold_modules else []
)

# Combine all assets
all_assets = bronze_assets + silver_assets + gold_assets

# Define jobs and schedules conditionally
jobs = []
schedules = []

if bronze_assets:
    bronze_job = define_asset_job(
        "bronze_job", selection=AssetSelection.groups("bronze")
    )
    jobs.append(bronze_job)
    bronze_schedule = ScheduleDefinition(
        job=bronze_job,
        cron_schedule="0 0 * * *",  # Daily at 12:00 AM
    )
    schedules.append(bronze_schedule)

defs = Definitions(assets=all_assets, jobs=jobs, schedules=schedules)
