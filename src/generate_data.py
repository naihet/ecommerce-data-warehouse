from faker import Faker
import pandas as pd
import random
import os

fake = Faker()

OUTPUT_DIR = "data/raw"

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

        f"{OUTPUT_DIR}/customers.csv",

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

        f"{OUTPUT_DIR}/products.csv",

        index=False

    )

#------------------------------------------------------------------

if __name__ == "__main__":

    generate_customers()

    print("Customers generated.")