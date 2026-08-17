CREATE SCHEMA IF NOT EXISTS gold;


DROP TABLE IF EXISTS gold.payment_summary CASCADE;
DROP TABLE IF EXISTS gold.customer_sales CASCADE;
DROP TABLE IF EXISTS gold.product_sales CASCADE;
DROP TABLE IF EXISTS gold.daily_sales CASCADE;


CREATE TABLE gold.daily_sales (
    sale_date DATE PRIMARY KEY,
    order_count INTEGER NOT NULL,
    item_count INTEGER NOT NULL,
    total_sales NUMERIC(14,2) NOT NULL,
    average_order_value NUMERIC(14,2) NOT NULL,
    load_timestamp TIMESTAMP NOT NULL
);


CREATE TABLE gold.product_sales (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    total_quantity INTEGER NOT NULL,
    total_sales NUMERIC(14,2) NOT NULL,
    order_count INTEGER NOT NULL,
    load_timestamp TIMESTAMP NOT NULL
);


CREATE TABLE gold.customer_sales (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    province VARCHAR(50),
    order_count INTEGER NOT NULL,
    total_items INTEGER NOT NULL,
    total_sales NUMERIC(14,2) NOT NULL,
    average_order_value NUMERIC(14,2) NOT NULL,
    load_timestamp TIMESTAMP NOT NULL
);


CREATE TABLE gold.payment_summary (
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    transaction_count INTEGER NOT NULL,
    total_amount NUMERIC(14,2) NOT NULL,
    load_timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (
        payment_method,
        payment_status
    )
);