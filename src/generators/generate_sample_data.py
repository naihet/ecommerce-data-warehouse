from faker import Faker
import pandas as pd
import random
import os
from pathlib import Path

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_customers(n=500):

    provinces = [
        "Bangkok",
        "Chiang Mai",
        "Phuket",
        "Khon Kaen",
        "Ayutthaya",
        "Chonburi"
    ]

    rows = []

    for i in range(1, n + 1):

        rows.append({

            "customer_id": f"C{i:05}",

            "customer_name": fake.name(),

            "gender": random.choice([
                "Male",
                "Female"
            ]),

            "province": random.choice(provinces),

            "signup_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            )

        })

    pd.DataFrame(rows).to_csv(

        OUTPUT_DIR / "customers.csv",

        index=False

    )

def generate_products(n=100):

    categories = [
        "Electronics",
        "Fashion",
        "Home",
        "Beauty",
        "Sports"
    ]

    rows = []

    for i in range(1, n + 1):

        rows.append({

            "product_id": f"P{i:05}",

            "product_name": fake.word().title()
            + " Product",

            "category": random.choice(categories),

            "price": round(
                random.uniform(10, 500),
                2
            )

        })


    pd.DataFrame(rows).to_csv(

        OUTPUT_DIR / "products.csv",

        index=False

    )

def generate_orders(n=2000):

    rows = []

    for i in range(1, n + 1):

        rows.append({

            "order_id": f"O{i:06}",

            "customer_id":
                f"C{random.randint(1,500):05}",

            "order_date":
                fake.date_between(
                    start_date="-2y",
                    end_date="today"
                ),

            "status":
                random.choice([
                    "Completed",
                    "Pending",
                    "Cancelled"
                ])

        })


    pd.DataFrame(rows).to_csv(

        OUTPUT_DIR / "orders.csv",

        index=False

    )

def generate_order_items(n=5000):

    rows = []

    for i in range(1, n + 1):

        quantity = random.randint(1,5)

        price = round(
            random.uniform(10,500),
            2
        )

        rows.append({

            "order_item_id":
                f"OI{i:06}",

            "order_id":
                f"O{random.randint(1,2000):06}",

            "product_id":
                f"P{random.randint(1,100):05}",

            "quantity":
                quantity,

            "unit_price":
                price,

            "total_price":
                round(
                    quantity * price,
                    2
                )

        })


    pd.DataFrame(rows).to_csv(

        OUTPUT_DIR / "order_items.csv",

        index=False

    )

def generate_payments(n=2000):

    rows = []

    for i in range(1, n + 1):

        rows.append({

            "payment_id":
                f"PAY{i:06}",

            "order_id":
                f"O{i:06}",

            "payment_method":
                random.choice([
                    "Credit Card",
                    "Bank Transfer",
                    "PromptPay",
                    "Cash"
                ]),

            "payment_status":
                random.choice([
                    "Paid",
                    "Pending",
                    "Failed"
                ]),

            "payment_date":
                fake.date_between(
                    start_date="-2y",
                    end_date="today"
                )

        })


    pd.DataFrame(rows).to_csv(

        OUTPUT_DIR / "payments.csv",

        index=False

    )

#------------------------------------------------------------------

if __name__ == "__main__":

    generate_customers()

    generate_products()

    generate_orders()

    generate_order_items()

    generate_payments()


    print("All data generated.")