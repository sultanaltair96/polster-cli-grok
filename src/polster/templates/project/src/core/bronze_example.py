"""Bronze layer example - Data extraction.

This file demonstrates how to extract data and write it to the bronze layer.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone

import polars as pl
from faker import Faker

from .storage import write_parquet


fake = Faker()


def extract() -> str:
    """Extract data and write to bronze layer.

    Returns:
        str: Path to the written parquet file.
    """
    customer_ids = list(range(1, 201))
    fetch_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # Generate orders data
    orders = []
    for idx in range(500):
        order_date = fake.date_time_between(start_date="-120d", end_date="now")
        total_amount = round(random.uniform(25.0, 520.0), 2)
        orders.append(
            {
                "order_id": 10000 + idx,
                "customer_id": random.choice(customer_ids),
                "order_date": order_date,
                "status": random.choice(
                    ["placed", "shipped", "delivered", "cancelled", "returned"]
                ),
                "total_amount": total_amount,
            }
        )

    # Generate payments data
    payments = []
    for order in orders:
        # Not all orders have payments
        if random.random() < 0.85:  # 85% of orders have payments
            payment_date = fake.date_time_between(
                start_date=order["order_date"], end_date="now"
            )
            paid_amount = (
                order["total_amount"]
                if random.random() < 0.95
                else round(order["total_amount"] * random.uniform(0.5, 1.0), 2)
            )
            payments.append(
                {
                    "order_id": order["order_id"],
                    "paid_amount": paid_amount,
                    "payment_date": payment_date,
                    "payment_status": "paid"
                    if paid_amount >= order["total_amount"] * 0.9
                    else "partial",
                }
            )

    # Save orders
    orders_df = pl.DataFrame(orders).with_columns(
        pl.lit(fetch_time).alias("fetched_at")
    )
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    orders_path = write_parquet(
        orders_df, "bronze", f"bronze_orders_{timestamp}.parquet"
    )

    # Save payments
    if payments:
        payments_df = pl.DataFrame(payments).with_columns(
            pl.lit(fetch_time).alias("fetched_at")
        )
        payments_path = write_parquet(
            payments_df, "bronze", f"bronze_payments_{timestamp}.parquet"
        )

    return orders_path


if __name__ == "__main__":
    extract()
