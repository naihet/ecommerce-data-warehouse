CREATE TABLE warehouse.dim_customers (

    customer_key SERIAL PRIMARY KEY,

    customer_id VARCHAR(20),

    customer_name VARCHAR(100),

    gender VARCHAR(20),

    province VARCHAR(50),

    signup_date DATE

);



CREATE TABLE warehouse.dim_products (

    product_key SERIAL PRIMARY KEY,

    product_id VARCHAR(20),

    product_name VARCHAR(100),

    category VARCHAR(50),

    price NUMERIC(10,2)

);



CREATE TABLE warehouse.fact_orders (

    order_key SERIAL PRIMARY KEY,

    order_id VARCHAR(20),

    customer_key INT,

    order_date DATE,

    status VARCHAR(20),

    FOREIGN KEY(customer_key)

    REFERENCES warehouse.dim_customers(customer_key)

);



CREATE TABLE warehouse.fact_order_items (

    order_item_key SERIAL PRIMARY KEY,

    order_id VARCHAR(20),

    product_key INT,

    quantity INT,

    unit_price NUMERIC(10,2),

    total_price NUMERIC(10,2),

    FOREIGN KEY(product_key)

    REFERENCES warehouse.dim_products(product_key)

);



CREATE TABLE warehouse.fact_payments (

    payment_key SERIAL PRIMARY KEY,

    payment_id VARCHAR(20),

    order_id VARCHAR(20),

    payment_method VARCHAR(50),

    payment_status VARCHAR(20),

    payment_date DATE

);