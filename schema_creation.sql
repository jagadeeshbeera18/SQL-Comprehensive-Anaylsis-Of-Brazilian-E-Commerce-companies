--- CREATE TABLES ----

-- Create table geolocation
DROP TABLE IF EXISTS geolocation;
CREATE TABLE IF NOT EXISTS geolocation (
	zip_code_prefix INTEGER NOT NULL,
	latitude NUMERIC,
	longitude NUMERIC,
	city TEXT,
	state TEXT
);
COPY geolocation FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_geolocation.csv' HEADER CSV DELIMITER ',';

-- Create table customers
DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers (
	customer_id TEXT PRIMARY KEY NOT NULL,
	customer_unique_id TEXT,
	zip_code_prefix INTEGER NOT NULL,
	city TEXT,
	state TEXT
);
COPY customers FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_customers.csv' HEADER CSV DELIMITER ',';

-- Create table sellers
DROP TABLE IF EXISTS sellers;
CREATE TABLE IF NOT EXISTS sellers (
	seller_id TEXT PRIMARY KEY NOT NULL,
	zip_code_prefix INTEGER,
	city TEXT,
	state TEXT
);
COPY sellers FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_sellers.csv' HEADER CSV DELIMITER ',';

-- Create table orders
DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders (
	order_id TEXT PRIMARY KEY NOT NULL,
	customer_id TEXT NOT NULL,
	status TEXT,
	purchase_timestamp TIMESTAMP,
	approval_timestamp TIMESTAMP,
	delivered_carrier_date TIMESTAMP,
	delivered_customer_date TIMESTAMP,
	estimated_delivery_date TIMESTAMP,
	delivery_date_quality_issue TEXT,
	carrier_date_quality_issue TEXT,
	CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
COPY orders FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_orders.csv' HEADER CSV DELIMITER ',';

-- Create table order_reviews
DROP TABLE IF EXISTS order_reviews;
CREATE TABLE IF NOT EXISTS order_reviews (
	review_id TEXT NOT NULL,
	order_id TEXT NOT NULL,
	rating INTEGER,
	review_title TEXT,
	review_content TEXT,
	creation_timestamp TIMESTAMP,
	answer_timestamp TIMESTAMP,
	CONSTRAINT fk_reviews FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
COPY order_reviews FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_reviews.csv' HEADER CSV DELIMITER ',';

-- Create table order_payments
DROP TABLE IF EXISTS order_payments;
CREATE TABLE IF NOT EXISTS order_payments (
	order_id TEXT NOT NULL,
	payment_sequential INTEGER,
	payment_type TEXT,
	payment_installments INTEGER,
	payment_value NUMERIC,
	CONSTRAINT fk_payments FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
COPY order_payments FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_payments.csv' HEADER CSV DELIMITER ',';

-- Create table category_names_english
DROP TABLE IF EXISTS category_names_english;
CREATE TABLE IF NOT EXISTS category_names_english (
	product_category TEXT PRIMARY KEY NOT NULL,
	product_category_eng TEXT
);
COPY category_names_english FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_category_names.csv' HEADER CSV DELIMITER ',';

-- Create table products
DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products (
	product_id TEXT PRIMARY KEY NOT NULL,
	product_category TEXT,
	name_length FLOAT,
	description_length FLOAT,
	photos_quantity FLOAT,
	weight_g FLOAT,
	length_cm FLOAT,
	height_cm FLOAT,
	width_cm FLoAT,
	CONSTRAINT fk_cateogry_eng FOREIGN KEY (product_category) REFERENCES category_names_english(product_category)
);
COPY products FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_products.csv' HEADER CSV DELIMITER ',';

-- Create table order_items
DROP TABLE IF EXISTS order_items;
CREATE TABLE IF NOT EXISTS order_items (
	order_id TEXT NOT NULL,
	item_id TEXT,
	product_id TEXT NOT NULL,
	seller_id TEXT NOT NULL,
	shipping_limit_date TIMESTAMP,
	price NUMERIC,
	freight_value NUMERIC,
	CONSTRAINT fk_products FOREIGN KEY (product_id) REFERENCES products(product_id),
	CONSTRAINT fk_orders FOREIGN KEY (order_id) REFERENCES orders(order_id),
	CONSTRAINT fk_sellers FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
COPY order_items FROM '/Users/jagadeesh/Olist E-Commerce Project/data/processed/clean_order_items.csv' HEADER CSV DELIMITER ',';