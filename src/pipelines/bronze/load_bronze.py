from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


# ==========================
# Database Configuration
# ==========================

DB_USER = "admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce_dw"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ==========================
# Data Folder
# ==========================

DATA_DIR = Path("data/raw")


# ==========================
# Load Function
# ==========================

def load_csv_to_bronze(file_name: str, table_name: str):

    csv_path = DATA_DIR / file_name

    df = pd.read_csv(csv_path)

    print(f"Loading {file_name}...")

    df.to_sql(
        name=table_name,
        schema="bronze",
        con=engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df)} rows → bronze.{table_name}")


# ==========================
# Main
# ==========================

if __name__ == "__main__":

    load_csv_to_bronze("customers.csv", "customers")
    load_csv_to_bronze("products.csv", "products")
    load_csv_to_bronze("orders.csv", "orders")
    load_csv_to_bronze("order_items.csv", "order_items")
    load_csv_to_bronze("payments.csv", "payments")

    print("\nBronze layer loaded successfully!")