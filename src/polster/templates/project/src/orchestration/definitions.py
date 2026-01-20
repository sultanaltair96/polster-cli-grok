"""Dagster definitions for Polster data pipelines.

This module automatically loads all assets and configures scheduling for bronze
assets with eager materialization for silver and gold layers.
"""

from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

# Load all assets from asset packages dynamically
try:
    from .assets import bronze, gold, silver

    all_assets = load_assets_from_modules([bronze, silver, gold])
except ImportError:
    all_assets = []

# Define jobs and schedules conditionally
jobs = []
schedules = []

# Bronze scheduling (silver/gold use eager conditions)
bronze_assets = [a for a in all_assets if getattr(a, "group_name", None) == "bronze"]
if bronze_assets:
    bronze_job = define_asset_job(
        "bronze_job", selection=AssetSelection.groups("bronze")
    )
    jobs.append(bronze_job)
    bronze_schedule = ScheduleDefinition(
        job=bronze_job,
        cron_schedule="1 0 * * *",  # Daily at 12:01 AM
    )
    schedules.append(bronze_schedule)

defs = Definitions(assets=all_assets, jobs=jobs, schedules=schedules)
