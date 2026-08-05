DROP TABLE IF EXISTS silver.payments CASCADE;
DROP TABLE IF EXISTS silver.order_items CASCADE;
DROP TABLE IF EXISTS silver.orders CASCADE;
DROP TABLE IF EXISTS silver.products CASCADE;
DROP TABLE IF EXISTS silver.customers CASCADE;

CREATE TABLE silver.customers (
    LIKE bronze.customers INCLUDING ALL,
    load_timestamp TIMESTAMP
);

CREATE TABLE silver.products (
    LIKE bronze.products INCLUDING ALL,
    load_timestamp TIMESTAMP
);

CREATE TABLE silver.orders (
    LIKE bronze.orders INCLUDING ALL,
    load_timestamp TIMESTAMP
);

CREATE TABLE silver.order_items (
    LIKE bronze.order_items INCLUDING ALL,
    load_timestamp TIMESTAMP
);

CREATE TABLE silver.payments (
    LIKE bronze.payments INCLUDING ALL,
    load_timestamp TIMESTAMP
);