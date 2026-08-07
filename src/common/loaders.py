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
        # 3. Build UPDATE columns
        # ==============================

        update_columns = [
            column
            for column in df.columns
            if column != primary_key
        ]

        update_clause = ", ".join(
            f'"{column}" = EXCLUDED."{column}"'
            for column in update_columns
        )

        columns = ", ".join(
            f'"{column}"'
            for column in df.columns
        )

        # ==============================
        # 4. UPSERT
        # ==============================

        query = text(
            f"""
            INSERT INTO {schema}.{table_name}
            ({columns})
            SELECT {columns}
            FROM staging.{staging_table}

            ON CONFLICT ({primary_key})
            DO UPDATE SET
                {update_clause};
            """
        )

        with engine.begin() as conn:
            result = conn.execute(query)

        print(
            f"{table_name}: "
            f"Upserted {result.rowcount} rows"
        )

    finally:

        # ==============================
        # 5. Remove staging
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