from src.database.connection import get_engine
from src.logging.logger import logger

from sqlalchemy import text


engine = get_engine()


def validate_daily_sales():

    logger.info("Validating gold.daily_sales")

    query = text(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(*) FILTER (
                WHERE sale_date IS NULL
            ) AS null_dates,
            COUNT(*) FILTER (
                WHERE total_sales < 0
            ) AS negative_sales
        FROM gold.daily_sales;
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query).mappings().one()

    if result["row_count"] == 0:

        raise ValueError(
            "gold.daily_sales is empty"
        )

    if result["null_dates"] > 0:

        raise ValueError(
            "gold.daily_sales contains NULL sale_date"
        )

    if result["negative_sales"] > 0:

        raise ValueError(
            "gold.daily_sales contains negative sales"
        )

    logger.info(
        f"daily_sales validation passed: "
        f"{result['row_count']} rows"
    )


def validate_product_sales():

    logger.info("Validating gold.product_sales")

    query = text(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(*) FILTER (
                WHERE product_id IS NULL
            ) AS null_product_ids,
            COUNT(*) FILTER (
                WHERE total_sales < 0
            ) AS negative_sales,
            COUNT(*) FILTER (
                WHERE total_quantity < 0
            ) AS negative_quantity
        FROM gold.product_sales;
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query).mappings().one()

    if result["row_count"] == 0:

        raise ValueError(
            "gold.product_sales is empty"
        )

    if result["null_product_ids"] > 0:

        raise ValueError(
            "gold.product_sales contains NULL product_id"
        )

    if result["negative_sales"] > 0:

        raise ValueError(
            "gold.product_sales contains negative sales"
        )

    if result["negative_quantity"] > 0:

        raise ValueError(
            "gold.product_sales contains negative quantity"
        )

    logger.info(
        f"product_sales validation passed: "
        f"{result['row_count']} rows"
    )


def validate_customer_sales():

    logger.info("Validating gold.customer_sales")

    query = text(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(*) FILTER (
                WHERE customer_id IS NULL
            ) AS null_customer_ids,
            COUNT(*) FILTER (
                WHERE total_sales < 0
            ) AS negative_sales,
            COUNT(*) FILTER (
                WHERE total_items < 0
            ) AS negative_items
        FROM gold.customer_sales;
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query).mappings().one()

    if result["row_count"] == 0:

        raise ValueError(
            "gold.customer_sales is empty"
        )

    if result["null_customer_ids"] > 0:

        raise ValueError(
            "gold.customer_sales contains NULL customer_id"
        )

    if result["negative_sales"] > 0:

        raise ValueError(
            "gold.customer_sales contains negative sales"
        )

    if result["negative_items"] > 0:

        raise ValueError(
            "gold.customer_sales contains negative items"
        )

    logger.info(
        f"customer_sales validation passed: "
        f"{result['row_count']} rows"
    )


def validate_payment_summary():

    logger.info("Validating gold.payment_summary")

    query = text(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(*) FILTER (
                WHERE payment_method IS NULL
            ) AS null_methods,
            COUNT(*) FILTER (
                WHERE payment_status IS NULL
            ) AS null_status,
            COUNT(*) FILTER (
                WHERE transaction_count < 0
            ) AS negative_transactions,
            COUNT(*) FILTER (
                WHERE total_amount < 0
            ) AS negative_amount
        FROM gold.payment_summary;
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query).mappings().one()

    if result["row_count"] == 0:

        raise ValueError(
            "gold.payment_summary is empty"
        )

    if result["null_methods"] > 0:

        raise ValueError(
            "gold.payment_summary contains NULL payment_method"
        )

    if result["null_status"] > 0:

        raise ValueError(
            "gold.payment_summary contains NULL payment_status"
        )

    if result["negative_transactions"] > 0:

        raise ValueError(
            "gold.payment_summary contains negative transactions"
        )

    if result["negative_amount"] > 0:

        raise ValueError(
            "gold.payment_summary contains negative amount"
        )

    logger.info(
        f"payment_summary validation passed: "
        f"{result['row_count']} rows"
    )


def validate_gold():

    logger.info("Starting Gold validation")

    validate_daily_sales()

    validate_product_sales()

    validate_customer_sales()

    validate_payment_summary()

    logger.info(
        "Gold validation completed successfully."
    )


if __name__ == "__main__":

    validate_gold()