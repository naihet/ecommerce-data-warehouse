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
from src.common.audit import log_pipeline_run

engine = get_engine()


def transform_table(table_name: str):

    logger.info(f"Processing {table_name}")

    started_at = datetime.now()

    source_rows = 0
    processed_rows = 0

    try:

        silver_df = pd.read_sql(
            f"SELECT * FROM silver.{table_name}",
            engine
        )

        df = pd.read_sql(
            f"SELECT * FROM bronze.{table_name}",
            engine
        )

        source_rows = len(df)

        # ======================
        # Data Validation
        # ======================

        validate_not_empty(df)

        # --------------------------------
        # customers
        # --------------------------------

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

        # --------------------------------
        # Other tables
        # --------------------------------

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
        # Data Type Conversion
        # ======================

        if table_name == "customers":

            df["signup_date"] = pd.to_datetime(
                df["signup_date"],
                errors="coerce",
            ).dt.date

        # ======================
        # Incremental Detection
        # ======================

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

        processed_rows = len(df)

        logger.info(
            f"{processed_rows} new records detected."
        )

        # ======================
        # No New Records
        # ======================

        if df.empty:

            completed_at = datetime.now()

            log_pipeline_run(
                engine=engine,
                table_name=table_name,
                source_rows=source_rows,
                processed_rows=0,
                started_at=started_at,
                completed_at=completed_at,
                status="SUCCESS",
            )

            logger.info(
                f"{table_name}: No new records."
            )

            return

        # ======================
        # Metadata
        # ======================

        df["load_timestamp"] = datetime.now()

        # ======================
        # Load to Silver
        # ======================

        load_dataframe(
            df=df,
            engine=engine,
            table_name=table_name,
            schema="silver",
        )

        # ======================
        # SUCCESS AUDIT
        # ======================

        completed_at = datetime.now()

        log_pipeline_run(
            engine=engine,
            table_name=table_name,
            source_rows=source_rows,
            processed_rows=processed_rows,
            started_at=started_at,
            completed_at=completed_at,
            status="SUCCESS",
        )

        logger.info(
            f"Loaded {processed_rows} rows "
            f"into silver.{table_name}"
        )

    except Exception as e:

        # ======================
        # FAILED AUDIT
        # ======================

        completed_at = datetime.now()

        log_pipeline_run(
            engine=engine,
            table_name=table_name,
            source_rows=source_rows,
            processed_rows=processed_rows,
            started_at=started_at,
            completed_at=completed_at,
            status="FAILED",
            error_message=str(e),
        )

        logger.exception(
            f"{table_name} pipeline failed."
        )

        raise

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