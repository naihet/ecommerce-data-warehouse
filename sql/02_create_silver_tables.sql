DROP TABLE IF EXISTS silver.payments CASCADE;
DROP TABLE IF EXISTS silver.order_items CASCADE;
DROP TABLE IF EXISTS silver.orders CASCADE;
DROP TABLE IF EXISTS silver.products CASCADE;
DROP TABLE IF EXISTS silver.customers CASCADE;

CREATE TABLE silver.customers (
    LIKE bronze.customers INCLUDING ALL
);

CREATE TABLE silver.products (
    LIKE bronze.products INCLUDING ALL
);

CREATE TABLE silver.orders (
    LIKE bronze.orders INCLUDING ALL
);

CREATE TABLE silver.order_items (
    LIKE bronze.order_items INCLUDING ALL
);

CREATE TABLE silver.payments (
    LIKE bronze.payments INCLUDING ALL
);