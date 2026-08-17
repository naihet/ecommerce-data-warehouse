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


if __name__ == "__main__":

    transform_daily_sales()

    logger.info(
        "Gold pipeline finished successfully."
    )