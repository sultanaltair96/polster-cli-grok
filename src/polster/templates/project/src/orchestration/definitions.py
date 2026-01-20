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

# Import asset modules
from .assets import bronze, gold, silver

# Automatically load all assets from each layer
bronze_assets = load_assets_from_modules([bronze])
silver_assets = load_assets_from_modules([silver])
gold_assets = load_assets_from_modules([gold])

print(f"DEBUG: bronze_assets: {len(bronze_assets)}")
print(f"DEBUG: silver_assets: {len(silver_assets)}")
print(f"DEBUG: gold_assets: {len(gold_assets)}")

# Combine all assets
all_assets = [*bronze_assets, *silver_assets, *gold_assets]

print(f"DEBUG: total assets: {len(all_assets)}")

# Define a job for all bronze assets
bronze_job = define_asset_job("bronze_job", selection=AssetSelection.groups("bronze"))

# Schedule for bronze assets (runs daily at midnight)
bronze_schedule = ScheduleDefinition(
    job=bronze_job,
    cron_schedule="0 0 * * *",  # Daily at 12:00 AM
)

defs = Definitions(assets=all_assets, jobs=[bronze_job], schedules=[bronze_schedule])
