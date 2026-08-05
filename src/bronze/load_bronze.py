import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import text
from src.logging.logger import logger
from src.config.settings import RAW_DIR
from src.database.connection import get_engine

# ==========================
# Database Connection
# ==========================

engine = get_engine()

# ==========================
# Data Directory
# ==========================

data_dir = RAW_DIR

# ==========================
# Load Function
# ==========================
def load_csv_to_bronze(file_name: str, table_name: str):
    csv_path = data_dir / file_name

    try:
        logger.info(f"Loading {file_name}")

        df = pd.read_csv(csv_path)

        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE bronze.{table_name};"))

        df.to_sql(
            name=table_name,
            schema="bronze",
            con=engine,
            if_exists="append",
            index=False,
        )

        logger.info(
            f"Loaded {len(df)} rows into bronze.{table_name}"
        )

    except Exception as e:
        logger.exception(
            f"Failed loading {table_name}"
        )
        raise


# ==========================
# Main
# ==========================
if __name__ == "__main__":

    tables = {
        "customers.csv": "customers",
        "products.csv": "products",
        "orders.csv": "orders",
        "order_items.csv": "order_items",
        "payments.csv": "payments",
    }
    
    logger.info("Starting Bronze Pipeline")

    for csv_file, table in tables.items():
        load_csv_to_bronze(csv_file, table)

    logger.info("Bronze Pipeline Finished Successfully")