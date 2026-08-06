from src.logging.logger import logger
import pandas as pd
from sqlalchemy import text
from datetime import datetime

from src.database.connection import get_engine

from src.common.dataframe import clean_dataframe
from src.common.incremental import get_new_records
from src.common.validation import (
    validate_not_empty,
    validate_required_columns,
    validate_primary_key,
    validate_null_primary_key,
)

from src.common.loaders import load_dataframe

engine = get_engine()


def transform_table(table_name: str):

    logger.info(f"Processing {table_name}")

    silver_df = pd.read_sql(
        f"SELECT * FROM silver.{table_name}",
        engine
    )

    df = pd.read_sql(
        f"SELECT * FROM bronze.{table_name}",
        engine
    )

    # ======================
    # Data Validation
    # ======================

    validate_not_empty(df)

    if table_name == "customers":

        validate_required_columns(
            df,
            [
                "customer_id",
                "customer_name",
                "gender",
                "province",
                "signup_date",
            ],
        )

        validate_primary_key(
            df,
            "customer_id",
        )

        validate_null_primary_key(
            df,
            "customer_id",
        )

    if table_name == "products":

        validate_primary_key(
            df,
            "product_id",
        )

    if table_name == "orders":

        validate_primary_key(
            df,
            "order_id",
        )

    if table_name == "order_items":

        validate_primary_key(
            df,
            "order_item_id",
        )

    if table_name == "payments":

        validate_primary_key(
            df,
            "payment_id",
        )

    logger.info(
        f"{table_name} validation passed."
    )

    # ======================
    # Data Cleaning
    # ======================

    df = clean_dataframe(df)

    pk_map = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id",
    }

    primary_key = pk_map[table_name]

    df = get_new_records(
        df,
        silver_df,
        primary_key,
    )

    logger.info(
        f"{len(df)} new records detected."
    )

    # ======================
    # Metadata
    # ======================

    df["load_timestamp"] = datetime.now()

    # ======================
    # Load to Silver
    # ======================

    with engine.begin() as conn:
        conn.execute(
            text(f"TRUNCATE TABLE silver.{table_name};")
        )

    load_dataframe(
        df=df,
        engine=engine,
        table_name=table_name,
        schema="silver",
    )

    logger.info(
        f"Loaded {len(df)} rows into silver.{table_name}"
    )


if __name__ == "__main__":

    tables = [
        "customers",
        "products",
        "orders",
        "order_items",
        "payments",
    ]

    for table in tables:
        transform_table(table)

    logger.info("Silver Pipeline Finished Successfully")