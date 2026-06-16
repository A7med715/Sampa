

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,

    customer_id VARCHAR(50) NOT NULL,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state CHAR(2),

    valid_from DATETIME NOT NULL,
    valid_to DATETIME NOT NULL,
    current BOOLEAN NOT NULL DEFAULT TRUE
);



CREATE TABLE dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,

    product_id VARCHAR(50) NOT NULL,
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100),

    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,

    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2)
);



CREATE TABLE dim_seller (
    seller_key INT AUTO_INCREMENT PRIMARY KEY,

    seller_id VARCHAR(50) NOT NULL,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state CHAR(2)
);

CREATE TABLE dim_date (
    date_key INT ,

    date DATE NOT NULL,

    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20),

    week INT NOT NULL,
    week_day INT NOT NULL,

    day VARCHAR(20),

    is_weekend BOOLEAN NOT NULL
);


CREATE TABLE fact_orders (
    order_item_key INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,

    shipping_limit_date DATETIME,

    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),

    order_status VARCHAR(30),

    order_purchase_timestamp DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,

    delivery_days DECIMAL(10,2),

    total_price DECIMAL(10,2),
    common_type VARCHAR(30),

    review_id VARCHAR(50),
    review_score INT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    date DATETIME,
    date_key INT,

    CONSTRAINT fk_fact_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_fact_product
        FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    CONSTRAINT fk_fact_seller
        FOREIGN KEY (seller_key)
        REFERENCES dim_seller(seller_key)
);
