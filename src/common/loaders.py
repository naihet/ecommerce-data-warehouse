import uuid
import pandas as pd
from sqlalchemy import text

def load_dataframe(
    df: pd.DataFrame,
    engine,
    table_name: str,
    schema: str,
):
    existing = pd.read_sql(
        f"SELECT * FROM {schema}.{table_name}",
        engine,
    )

    primary_keys = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id",
    }

    pk = primary_keys[table_name]

    new_rows = df[
        ~df[pk].isin(existing[pk])
    ]

    if new_rows.empty:
        print(f"{table_name}: No new records")
        return

    new_rows.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False,
    )

    print(f"{table_name}: Inserted {len(new_rows)} new rows")