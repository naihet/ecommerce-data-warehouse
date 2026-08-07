import uuid
import pandas as pd
from sqlalchemy import text

PRIMARY_KEYS = {
    "customers": "customer_id",
    "products": "product_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "payments": "payment_id",
}


def load_dataframe(
    df: pd.DataFrame,
    engine,
    table_name: str,
    schema: str,
):
    primary_key = PRIMARY_KEYS[table_name]

    staging_table = (
        f"staging_{table_name}_{uuid.uuid4().hex[:8]}"
    )

    try:

        # ==============================
        # 1. Create staging table
        # ==============================

        with engine.begin() as conn:

            conn.execute(
                text(
                    f"""
                    CREATE TABLE staging.{staging_table}
                    (LIKE {schema}.{table_name});
                    """
                )
            )

        # ==============================
        # 2. Load DataFrame
        # ==============================

        df.to_sql(
            staging_table,
            engine,
            schema="staging",
            if_exists="append",
            index=False,
        )

        # ==============================
        # 3. Insert new records
        # ==============================

        columns = ", ".join(
            f'"{column}"'
            for column in df.columns
        )

        query = text(
            f"""
            INSERT INTO {schema}.{table_name}
            ({columns})
            SELECT {columns}
            FROM staging.{staging_table}
            ON CONFLICT ({primary_key})
            DO NOTHING;
            """
        )

        with engine.begin() as conn:

            result = conn.execute(query)

        print(
            f"{table_name}: "
            f"Inserted {result.rowcount} new rows"
        )

    finally:

        # ==============================
        # 4. Remove staging table
        # ==============================

        with engine.begin() as conn:

            conn.execute(
                text(
                    f"""
                    DROP TABLE IF EXISTS
                    staging.{staging_table};
                    """
                )
            )