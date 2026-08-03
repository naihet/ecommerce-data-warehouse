CREATE TABLE silver.customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    province VARCHAR(100),
    signup_date DATE
);

CREATE TABLE silver.products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    price NUMERIC(10,2)
);

CREATE TABLE silver.orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    order_date DATE,
    status VARCHAR(50)
);

CREATE TABLE silver.order_items (
    order_item_id VARCHAR(10) PRIMARY KEY,
    order_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INTEGER,
    unit_price NUMERIC(10,2)
);

CREATE TABLE silver.payments (
    payment_id VARCHAR(10) PRIMARY KEY,
    order_id VARCHAR(10),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    payment_date DATE
);