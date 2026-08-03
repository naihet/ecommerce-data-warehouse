from pathlib import Path
import logging
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ==========================
# Logging
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================
# Database Connection
# ==========================
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================
# Data Directory
# ==========================
DATA_DIR = Path("data/raw")

# ==========================
# Load Function
# ==========================
def load_csv_to_bronze(file_name: str, table_name: str):
    csv_path = DATA_DIR / file_name

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
        logger.error(e)
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

    for csv_file, table in tables.items():
        load_csv_to_bronze(csv_file, table)

    logger.info("Bronze Pipeline Finished Successfully")