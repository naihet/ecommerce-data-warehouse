from src.logging.logger import logger
import pandas as pd
from sqlalchemy import text

from src.database.connection import get_engine

from src.common.dataframe import clean_dataframe

from src.common.validation import (
    validate_not_empty,
    validate_required_columns,
    validate_primary_key,
    validate_null_primary_key,
)

engine = get_engine()


def transform_table(table_name: str):

    logger.info(f"Processing {table_name}")

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

    # ======================
    # Load to Silver
    # ======================

    with engine.begin() as conn:
        conn.execute(
            text(f"TRUNCATE TABLE silver.{table_name};")
        )

    df.to_sql(
        table_name,
        engine,
        schema="silver",
        if_exists="append",
        index=False
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