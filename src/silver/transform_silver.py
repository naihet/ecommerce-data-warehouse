from src.logging.logger import logger
import pandas as pd
from sqlalchemy import text

from src.database.connection import get_engine

engine = get_engine()


def transform_table(table_name: str):

    logger.info(f"Processing {table_name}")

    df = pd.read_sql(
        f"SELECT * FROM bronze.{table_name}",
        engine
    )

    # ======================
    # Data Cleaning
    # ======================

    df = df.drop_duplicates()

    df = df.dropna(how="all")

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