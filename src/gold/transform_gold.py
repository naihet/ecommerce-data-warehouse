from datetime import datetime

from sqlalchemy import text

from src.database.connection import get_engine
from src.logging.logger import logger


engine = get_engine()

def transform_daily_sales():

    logger.info("Processing gold.daily_sales")

    query = text(
        """
        INSERT INTO gold.daily_sales (
            sale_date,
            order_count,
            item_count,
            total_sales,
            average_order_value,
            load_timestamp
        )

        SELECT
            o.order_date AS sale_date,

            COUNT(DISTINCT o.order_id) AS order_count,

            COALESCE(
                SUM(oi.quantity),
                0
            ) AS item_count,

            COALESCE(
                SUM(oi.total_price),
                0
            ) AS total_sales,

            COALESCE(
                SUM(oi.total_price)
                / NULLIF(
                    COUNT(DISTINCT o.order_id),
                    0
                ),
                0
            ) AS average_order_value,

            :load_timestamp AS load_timestamp

        FROM silver.orders o

        INNER JOIN silver.order_items oi
            ON o.order_id = oi.order_id

        WHERE o.status != 'cancelled'

        GROUP BY
            o.order_date

        ORDER BY
            o.order_date

        ON CONFLICT (sale_date)
        DO UPDATE SET

            order_count = EXCLUDED.order_count,

            item_count = EXCLUDED.item_count,

            total_sales = EXCLUDED.total_sales,

            average_order_value =
                EXCLUDED.average_order_value,

            load_timestamp =
                EXCLUDED.load_timestamp;
        """
    )

    with engine.begin() as conn:

        result = conn.execute(
            query,
            {
                "load_timestamp": datetime.now()
            }
        )

    logger.info(
        "gold.daily_sales transformation completed."
    )

#==================================

def transform_product_sales():

    logger.info("Processing gold.product_sales")

    query = text(
        """
        INSERT INTO gold.product_sales (
            product_id,
            product_name,
            category,
            total_quantity,
            total_sales,
            order_count,
            load_timestamp
        )

        SELECT
            p.product_id,

            p.product_name,

            p.category,

            COALESCE(
                SUM(oi.quantity),
                0
            ) AS total_quantity,

            COALESCE(
                SUM(oi.total_price),
                0
            ) AS total_sales,

            COUNT(DISTINCT oi.order_id) AS order_count,

            :load_timestamp AS load_timestamp

        FROM silver.products p

        INNER JOIN silver.order_items oi
            ON p.product_id = oi.product_id

        INNER JOIN silver.orders o
            ON oi.order_id = o.order_id

        WHERE o.status != 'cancelled'

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        ON CONFLICT (product_id)
        DO UPDATE SET

            product_name =
                EXCLUDED.product_name,

            category =
                EXCLUDED.category,

            total_quantity =
                EXCLUDED.total_quantity,

            total_sales =
                EXCLUDED.total_sales,

            order_count =
                EXCLUDED.order_count,

            load_timestamp =
                EXCLUDED.load_timestamp;
        """
    )

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "load_timestamp": datetime.now()
            }
        )

    logger.info(
        "gold.product_sales transformation completed."
    )

#==================================

def transform_customer_sales():

    logger.info("Processing gold.customer_sales")

    query = text(
        """
        INSERT INTO gold.customer_sales (
            customer_id,
            customer_name,
            province,
            order_count,
            total_items,
            total_sales,
            average_order_value,
            load_timestamp
        )

        SELECT
            c.customer_id,

            c.customer_name,

            c.province,

            COUNT(DISTINCT o.order_id) AS order_count,

            COALESCE(
                SUM(oi.quantity),
                0
            ) AS total_items,

            COALESCE(
                SUM(oi.total_price),
                0
            ) AS total_sales,

            COALESCE(
                SUM(oi.total_price)
                / NULLIF(
                    COUNT(DISTINCT o.order_id),
                    0
                ),
                0
            ) AS average_order_value,

            :load_timestamp AS load_timestamp

        FROM silver.customers c

        INNER JOIN silver.orders o
            ON c.customer_id = o.customer_id

        INNER JOIN silver.order_items oi
            ON o.order_id = oi.order_id

        WHERE o.status != 'cancelled'

        GROUP BY
            c.customer_id,
            c.customer_name,
            c.province

        ON CONFLICT (customer_id)
        DO UPDATE SET

            customer_name =
                EXCLUDED.customer_name,

            province =
                EXCLUDED.province,

            order_count =
                EXCLUDED.order_count,

            total_items =
                EXCLUDED.total_items,

            total_sales =
                EXCLUDED.total_sales,

            average_order_value =
                EXCLUDED.average_order_value,

            load_timestamp =
                EXCLUDED.load_timestamp;
        """
    )

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "load_timestamp": datetime.now()
            }
        )

    logger.info(
        "gold.customer_sales transformation completed."
    )

#==================================

if __name__ == "__main__":

    transform_daily_sales()

    transform_product_sales()

    transform_customer_sales()
    
    logger.info(
        "Gold pipeline finished successfully."
    )