CREATE TABLE staging.customers (

    customer_id VARCHAR(20),

    customer_name VARCHAR(100),

    gender VARCHAR(20),

    province VARCHAR(50),

    signup_date DATE

);



CREATE TABLE staging.products (

    product_id VARCHAR(20),

    product_name VARCHAR(100),

    category VARCHAR(50),

    price NUMERIC(10,2)

);



CREATE TABLE staging.orders (

    order_id VARCHAR(20),

    customer_id VARCHAR(20),

    order_date DATE,

    status VARCHAR(20)

);



CREATE TABLE staging.order_items (

    order_item_id VARCHAR(20),

    order_id VARCHAR(20),

    product_id VARCHAR(20),

    quantity INT,

    unit_price NUMERIC(10,2),

    total_price NUMERIC(10,2)

);



CREATE TABLE staging.payments (

    payment_id VARCHAR(20),

    order_id VARCHAR(20),

    payment_method VARCHAR(50),

    payment_status VARCHAR(20),

    payment_date DATE

);