/****** Script for SelectTopNRows command ******/
SELECT seller_id,
       zip_code_prefix,
       city,
       state
FROM sellers
LIMIT 5

SELECT product_category,
       product_category_eng
FROM category_names_english
LIMIT 5


SELECT customer_id,
       customer_unique_id,
       zip_code_prefix,
       city,
       state
FROM customers
LIMIT 5


SELECT zip_code_prefix,
        latitude,
        longitude,
        city,
        state
FROM geolocation
LIMIT 5


SELECT order_id,
       item_id,
       product_id,
       seller_id,
       shipping_limit_date,
       price,
       freight_value
FROM order_items
LIMIT 5


SELECT order_id,
       payment_sequential,
       payment_type,
       payment_installments,
       payment_value
FROM order_payments
LIMIT 5


SELECT review_id,
       order_id,
       rating,
       review_title,
       review_content,
       creation_timestamp,
       answer_timestamp
FROM order_reviews
LIMIT 5


SELECT order_id,
       customer_id,
       status,
       purchase_timestamp,
       approval_timestamp,
       delivered_carrier_date,
       delivered_customer_date,
       estimated_delivery_date
FROM orders
LIMIT 5

SELECT product_id
       product_category,
       name_length,
       description_length,
       photos_quantity,
       weight_g,
       length_cm,
       height_cm,
       width_cm
FROM products
LIMIT 5


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- DATA CLEANING OF THE TABLES

-- SELLERS TABLE
select *
FROM sellers


--let's capitalize the seller city and rename it to its full form
UPDATE sellers
SET city= INITCAP(LOWER(city))


UPDATE sellers
SET state = 
CASE state
    WHEN 'AC' THEN 'Acre'
    WHEN 'AL' THEN 'Alagoas'
    WHEN 'AP' THEN 'Amapa'
    WHEN 'AM' THEN 'Amazonas'
    WHEN 'BA' THEN 'Bahia'
    WHEN 'CE' THEN 'Ceara'
    WHEN 'DF' THEN 'Distrito Federal'
    WHEN 'ES' THEN 'Espirito Santo'
    WHEN 'GO' THEN 'Goias'
    WHEN 'MA' THEN 'Maranhao'
    WHEN 'MT' THEN 'Mato Grosso'
    WHEN 'MS' THEN 'Mato Grosso do Sul'
    WHEN 'MG' THEN 'Minas Gerais'
    WHEN 'PA' THEN 'Para'
    WHEN 'PB' THEN 'Paraiba'
    WHEN 'PR' THEN 'Parana'
    WHEN 'PE' THEN 'Pernambuco'
    WHEN 'PI' THEN 'Piaui'
    WHEN 'RJ' THEN 'Rio de Janeiro'
    WHEN 'RN' THEN 'Rio Grande do Norte'
    WHEN 'RS' THEN 'Rio Grande do Sul'
    WHEN 'RO' THEN 'Rondonia'
    WHEN 'RR' THEN 'Roraima'
    WHEN 'SC' THEN 'Santa Catarina'
    WHEN 'SP' THEN 'Sao Paulo'
    WHEN 'SE' THEN 'Sergipe'
    WHEN 'TO' THEN 'Tocantins'
END;


----------------------------------------------------------------------------------------------------------------------------------------------------------------------
--- CUSTOMER TABLE CLEANING
SELECT *
FROM customers

-- changing the customer_city to a proper case
UPDATE customers
SET city= INITCAP(LOWER(city))


-- Replacing the abbreviated customer_state to its full name
UPDATE customers
SET state = 
CASE state
    WHEN 'AC' THEN 'Acre'
    WHEN 'AL' THEN 'Alagoas'
    WHEN 'AP' THEN 'Amapa'
    WHEN 'AM' THEN 'Amazonas'
    WHEN 'BA' THEN 'Bahia'
    WHEN 'CE' THEN 'Ceara'
    WHEN 'DF' THEN 'Distrito Federal'
    WHEN 'ES' THEN 'Espirito Santo'
    WHEN 'GO' THEN 'Goias'
    WHEN 'MA' THEN 'Maranhao'
    WHEN 'MT' THEN 'Mato Grosso'
    WHEN 'MS' THEN 'Mato Grosso do Sul'
    WHEN 'MG' THEN 'Minas Gerais'
    WHEN 'PA' THEN 'Para'
    WHEN 'PB' THEN 'Paraiba'
    WHEN 'PR' THEN 'Parana'
    WHEN 'PE' THEN 'Pernambuco'
    WHEN 'PI' THEN 'Piaui'
    WHEN 'RJ' THEN 'Rio de Janeiro'
    WHEN 'RN' THEN 'Rio Grande do Norte'
    WHEN 'RS' THEN 'Rio Grande do Sul'
    WHEN 'RO' THEN 'Rondonia'
    WHEN 'RR' THEN 'Roraima'
    WHEN 'SC' THEN 'Santa Catarina'
    WHEN 'SP' THEN 'Sao Paulo'
    WHEN 'SE' THEN 'Sergipe'
    WHEN 'TO' THEN 'Tocantins'
END;


--------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Geolocation TABLE
SELECT * 
FROM geolocation


--Capitalizing the first letter of each word in the geolocation_city column
UPDATE geolocation
SET city= INITCAP(city)


-- renaming geolocation_state to its unabbreviated name
UPDATE geolocation
SET state = 
CASE state
    WHEN 'AC' THEN 'Acre'
    WHEN 'AL' THEN 'Alagoas'
    WHEN 'AP' THEN 'Amapa'
    WHEN 'AM' THEN 'Amazonas'
    WHEN 'BA' THEN 'Bahia'
    WHEN 'CE' THEN 'Ceara'
    WHEN 'DF' THEN 'Distrito Federal'
    WHEN 'ES' THEN 'Espirito Santo'
    WHEN 'GO' THEN 'Goias'
    WHEN 'MA' THEN 'Maranhao'
    WHEN 'MT' THEN 'Mato Grosso'
    WHEN 'MS' THEN 'Mato Grosso do Sul'
    WHEN 'MG' THEN 'Minas Gerais'
    WHEN 'PA' THEN 'Para'
    WHEN 'PB' THEN 'Paraiba'
    WHEN 'PR' THEN 'Parana'
    WHEN 'PE' THEN 'Pernambuco'
    WHEN 'PI' THEN 'Piaui'
    WHEN 'RJ' THEN 'Rio de Janeiro'
    WHEN 'RN' THEN 'Rio Grande do Norte'
    WHEN 'RS' THEN 'Rio Grande do Sul'
    WHEN 'RO' THEN 'Rondonia'
    WHEN 'RR' THEN 'Roraima'
    WHEN 'SC' THEN 'Santa Catarina'
    WHEN 'SP' THEN 'Sao Paulo'
    WHEN 'SE' THEN 'Sergipe'
    WHEN 'TO' THEN 'Tocantins'
END;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- SOLVING THE BUSINESS QUESTIONS


--1)  What is the total revenue generated by Olist?
-- Total revenue generated by Olist
SELECT ROUND(SUM(payment_value), 2) AS Total_Revenue
FROM orders o
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.status!='canceled' AND o.status!='unavailable';


-- How revenue changed overtime?
-- revenue by quarter
SELECT EXTRACT(YEAR FROM purchase_timestamp) AS year,
       EXTRACT(QUARTER FROM purchase_timestamp) AS quarter,
       ROUND(SUM(payment_value), 2) AS Total_Revenue
FROM orders o
JOIN order_payments op ON o.order_id=op.order_id
WHERE o.status!='canceled' AND o.status!='unavailable'
GROUP BY EXTRACT(YEAR FROM purchase_timestamp), EXTRACT(QUARTER FROM purchase_timestamp)
ORDER BY year, quarter;

-- revenue by month
SELECT EXTRACT(YEAR FROM purchase_timestamp) AS year,
       EXTRACT(MONTH FROM purchase_timestamp) AS month,
       ROUND(SUM(payment_value), 2) AS Total_Revenue
FROM orders o
JOIN order_payments op ON o.order_id=op.order_id
WHERE o.status!='canceled' AND o.status!='unavailable'
GROUP BY EXTRACT(YEAR FROM purchase_timestamp), EXTRACT(MONTH FROM purchase_timestamp)
ORDER BY year, month;


----------------------------------------------------------------------------------------------------------------------------------------------------------------------
--2) How many orders were placed on Olist, and how does this vary by month or season?
--How many orders were placed on Olist
SELECT COUNT(order_id) as genuine_orders
FROM orders
WHERE status!='canceled' AND status!='unavailable';

-- how does this vary by month and year
SELECT EXTRACT(YEAR FROM purchase_timestamp) AS YEAR, EXTRACT(MONTH FROM purchase_timestamp) AS month, COUNT(order_id) as order_count
FROM orders 
WHERE status='delivered'
GROUP BY EXTRACT(YEAR FROM purchase_timestamp), EXTRACT(MONTH FROM purchase_timestamp)
ORDER BY year, month;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--3)  What are the most popular product categories on Olist, and how do their sales volumes compare to each other?
SELECT product_category_eng AS product_category_eng_name, ROUND(SUM(payment_value), 2) AS total_sales_volume
FROM orders o
JOIN order_payments op ON o.order_id = op.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products ON products.product_id = oi.product_id
JOIN category_names_english ON category_names_english.product_category = products.product_category
WHERE o.status!='canceled' AND o.status!='unavailable'
GROUP BY product_category_eng_name
ORDER BY total_sales_volume DESC;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--4) What is the average order value (AOV) on Olist, and how does this vary by product category or payment method?
-- AOV on olist
SELECT ROUND(AVG(payment_value), 2) AS avg_order_value
FROM orders o
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.status!='canceled' AND o.status!='unavailable';

-- how AOV varies by payment type
SELECT payment_type, ROUND(AVG(payment_value)) AS avg_order_value
FROM orders o
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.status!='canceled' AND o.status!='unavailable'
GROUP BY payment_type
ORDER BY avg_order_value;

-- how AOV varies by product category
SELECT product_category_eng AS product_category_eng_name, ROUND(AVG(payment_value), 2) AS avg_order_value
FROM orders o
JOIN order_payments op ON o.order_id = op.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products ON products.product_id = oi.product_id
JOIN category_names_english ON category_names_english.product_category = products.product_category
WHERE o.status!='canceled' AND o.status!='unavailable'
GROUP BY product_category_eng_name
ORDER BY avg_order_value DESC;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 5) How many sellers are active on Olist, and how does this number change over time?
-- Number of active sellers by year
-- Overall count of seller additions or drops by year
with yearly_sellers AS(
    SELECT EXTRACT(year FROM purchase_timestamp) AS year, COUNT(DISTINCT seller_id) AS active_sellers
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status='delivered'
    GROUP BY EXTRACT(YEAR FROM purchase_timestamp))
SELECT
    year, active_sellers, LAG(active_sellers) OVER(ORDER BY year) AS previous_year,
    ROUND(active_sellers-LAG(active_sellers) OVER(ORDER BY year)) AS num_seller_added
FROM yearly_sellers
ORDER BY year;


-- Overall count of seller additions or drops by year
with monthly_sellers AS(
    SELECT EXTRACT(YEAR FROM purchase_timestamp) AS year, EXTRACT(MONTH FROM purchase_timestamp) AS month, COUNT(DISTINCT seller_id) AS active_sellers
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status='delivered'
    GROUP BY EXTRACT(YEAR FROM purchase_timestamp), EXTRACT(MONTH FROM purchase_timestamp)
)


SELECT
    year, month, active_sellers, LAG(active_sellers) OVER(ORDER BY month) AS previous_month,
    ROUND(active_sellers-LAG(active_sellers) OVER(ORDER BY month)) AS num_seller_added
FROM monthly_sellers
ORDER BY year, month;


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 6) What is the distribution of seller ratings on Olist, and how does this impact sales performance? 
-- Joining the order review dataset with the order payment dataset
SELECT oor.rating,
       COUNT(DISTINCT oor.order_id) AS num_orders,
       ROUND(SUM(op.payment_value), 2) AS total_revenue,
       ROUND(AVG(op.payment_value), 2) AS avg_revenue
FROM order_reviews oor
JOIN order_payments op ON oor.order_id = op.order_id
GROUP BY oor.rating
ORDER BY oor.rating DESC;


-- finding the relationship between rating and total revenue
-- we want to know find the correlation coefficient of rating and total revenue
SELECT 
    ROUND(CORR(rating, total_revenue)::numeric, 2) AS correlation_coefficient
FROM (
    SELECT
        oor.rating,
        ROUND(SUM(op.payment_value), 2) AS total_revenue
    FROM order_reviews oor
    JOIN order_payments op ON oor.order_id=op.order_id
    GROUP BY oor.rating
) AS data;


-- Finding order level of correlation cofficient of rating and total revenue
WITH order_revenue AS(
    SELECT order_id,
           ROUND(SUM(payment_value), 2) AS total_revenue
    FROM order_payments
    GROUP BY order_id
)

SELECT ROUND(SUM(orv.total_revenue)::NUMERIC, 2) AS total_revenue,
       ROUND(CORR(oor.rating::DOUBLE PRECISION, orv.total_revenue::DOUBLE PRECISION)::NUMERIC, 4) AS correlation
FROM order_reviews oor
JOIN order_revenue orv ON oor.order_id=orv.order_id;


-- it has a correlation coefficient of 0.75, when calculating total revenue across 5 ratings.
-- A correlation coefficient of 0.75 suggests a positive impact on revenue: as review scores increase, there is a tendency for higher total revenue. 
-- This finding indicates that seller's rating, as measured by review scores, likely has a positive influence on sales performance.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 7) How many customers have made repeated purchases on Olist, and what percentage of total sales do they account for?
WITH repeated_customers AS (
    SELECT c.customer_unique_id,
           COUNT(DISTINCT o.order_id) AS order_count,
           ROUND(SUM(payment_value), 2) AS total_spent
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN order_payments op ON o.order_id = op.order_id
    GROUP BY c.customer_unique_id
    HAVING COUNT(DISTINCT o.order_id)>1
)

SELECT COUNT(DISTINCT rep.customer_unique_id) AS num_repeated_customer,
       ROUND(SUM(rep.total_spent)/(SELECT SUM(payment_value) FROM order_payments), 2) * 100 AS repeated_customers_pct,
       COUNT(DISTINCT c.customer_unique_id) AS total_customers,
       COUNT(DISTINCT c.customer_unique_id) - COUNT(DISTINCT rep.customer_unique_id) AS num_non_rep_customers
FROM customers c
LEFT JOIN repeated_customers rep ON c.customer_unique_id=rep.customer_unique_id;


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--8)  What is the average customer rating for products sold on Olist, and how does this impact sales performance?
-- Calculate average customer rating
SELECT ROUND(AVG(rating), 2) AS avg_customer_rating
FROM order_reviews

SELECT products.product_category,
       rating,
       ROUND(AVG(rating), 2) as avgerage_rating,
       COUNT(DISTINCT orders.order_id) AS num_orders,
       ROUND(SUM(payment_value), 2) AS total_revenue,
       ROUND(SUM(payment_value) / COUNT(DISTINCT orders.order_id), 2) AS avg_revenue
FROM order_reviews oor
INNER JOIN orders ON orders.order_id = oor.order_id
INNER JOIN order_payments ON order_payments.order_id = orders.order_id
INNER JOIN order_items ON order_items.order_id = orders.order_id
INNER JOIN products ON products.product_id = order_items.product_id
WHERE orders.status = 'delivered'
GROUP BY products.product_category,rating
ORDER BY total_revenue DESC;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--9) What is the average order cancellation rate on Olist, and how does this impact seller performance?
-- Calculate overall cancellation rate and total canceled orders
with order_base AS(
    SELECT order_id,status,
           CASE WHEN status='canceled' THEN 1 ELSE 0 END AS is_canceled
    FROM orders
),
order_totals AS(
    SELECT order_id,SUM(payment_value) AS total_payment
    FROM order_payments
    GROUP BY order_id
),
order_sellers AS(
    SELECT DISTINCT order_id, seller_id
    FROM order_items
)

SELECT 
    ROUND(AVG(ob.is_canceled)::NUMERIC * 100, 2) AS avg_cancellation_rate,
    COUNT(DISTINCT ob.order_id) AS num_orders,
    ROUND(SUM(CASE WHEN ob.status='canceled' THEN ot.total_payment ELSE 0 END), 2) AS amount_lost,
    COUNT(DISTINCT os.seller_id) AS num_sellers
FROM order_base ob
LEFT JOIN order_totals ot ON ob.order_id=ot.order_id
LEFT JOIN order_sellers os ON ob.order_id=os.order_id;

--This shows the sellers with canceled orders, the rate, and the number of orders that they have had to cancel, showing their performance
with seller_items AS(
    SELECT DISTINCT order_id, seller_id, price+freight_value AS item_revenue
    FROM order_items
),
order_status AS(
    SELECT order_id,status
    FROM orders
),
seller_reviews AS(
    SELECT order_id,
           AVG(rating) AS rating
    FROM order_reviews
    GROUP BY order_id
),
sellers_data AS(
    SELECT si.seller_id,
           si.order_id,
           os.status,
           si.item_revenue,
           sr.rating
    FROM seller_items si
    JOIN order_status os ON si.order_id=os.order_id
    LEFT JOIN seller_reviews sr ON si.order_id=sr.order_id
)

SELECT  
    seller_id,
    COUNT(DISTINCT CASE WHEN status='canceled' THEN order_id END) AS num_cancelled_orders,
    ROUND(SUM(item_revenue)::NUMERIC, 2) AS total_sales_volume,
    ROUND(AVG(rating)::NUMERIC, 2) AS customer_satisfaction,
    ROUND((COUNT(DISTINCT CASE WHEN status='canceled' THEN order_id END)::NUMERIC / NULLIF(COUNT(DISTINCT order_id),0)) * 100,2) AS cancellation_rate
FROM sellers_data
GROUP BY seller_id
ORDER BY cancellation_rate DESC LIMIT 20;


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 10) What are the top-selling products on Olist, and how have their sales trends changed over time?
WITH category_data AS (
    SELECT products.product_category,
           EXTRACT(QUARTER FROM orders.purchase_timestamp) AS order_quarter,
           EXTRACT(YEAR FROM orders.purchase_timestamp) AS order_year,
           ROUND(SUM(order_items.price+order_items.freight_value), 2) AS total_sales
    FROM orders 
    JOIN order_items ON order_items.order_id = orders.order_id
    JOIN products ON products.product_id = order_items.product_id
    GROUP BY products.product_category,
    EXTRACT(QUARTER FROM orders.purchase_timestamp),
    EXTRACT(YEAR FROM orders.purchase_timestamp)
),
ranked_categories AS(
    SELECT 
        product_category,
        order_quarter,
        order_year,
        ROUND(total_sales::NUMERIC, 2) AS total_sales,
        RANK() OVER(PARTITION BY order_year,order_quarter ORDER BY total_sales DESC) AS category_rank
    FROM category_data
)

SELECT product_category,
       order_quarter,
       order_year,
       total_sales
FROM ranked_categories
WHERE category_rank=1
ORDER BY order_year DESC, order_quarter DESC;


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 11) Which payment methods are most commonly used by Olist customers, and how does this vary by product category or geographic region?
-- total number of orders placed with each payment type

SELECT payment_type, COUNT(DISTINCT order_id) AS num_orders
FROM order_payments
GROUP BY payment_type
ORDER BY num_orders DESC;

-- by product type
SELECT order_payments.payment_type,
       COUNT(DISTINCT customers.customer_id) AS num_customers,
       products.product_category,
       customers.state
FROM orders
INNER JOIN order_payments ON order_payments.order_id = orders.order_id
INNER JOIN order_items ON order_items.order_id = orders.order_id
INNER JOIN customers ON customers.customer_id = orders.customer_id
INNER JOIN products ON products.product_id = order_items.product_id
GROUP BY order_payments.payment_type,
         products.product_category,
         customers.state
ORDER BY num_customers DESC;

--by geolocation
SELECT order_payments.payment_type,
       COUNT(*) AS num_orders,
       customers.state
FROM orders
INNER JOIN order_payments ON order_payments.order_id = orders.order_id
INNER JOIN customers ON customers.customer_id = orders.customer_id
GROUP BY order_payments.payment_type,customers.state
ORDER BY num_orders;


------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--12) How do customer reviews and ratings affect sales and product performance on Olist?
SELECT CASE
        WHEN order_reviews.rating=5 THEN 'Excellent'
        WHEN order_reviews.rating=4 THEN 'Very Good'
        WHEN order_reviews.rating=3 THEN 'Good'
        WHEN order_reviews.rating=2 THEN 'Bad'
        WHEN order_reviews.rating=1 THEN 'Very Bad'
    END AS rating,
    COUNT(DISTINCT order_reviews.review_id) AS no_review,
    COUNT(DISTINCT products.product_id) AS no_products,
    ROUND(SUM(order_payments.payment_value), 2) AS total_revenue,
    ROUND(AVG(order_payments.payment_value), 2) AS avg_revenue
FROM order_reviews
INNER JOIN orders ON orders.order_id = order_reviews.order_id
INNER JOIN order_items ON order_items.order_id = orders.order_id
INNER JOIN order_payments ON order_payments.order_id = orders.order_id
INNER JOIN products ON products.product_id = order_items.product_id
WHERE orders.status!='canceled' AND orders.status!='unavailable' AND orders.approval_timestamp IS NOT NULL
GROUP BY order_reviews.rating
ORDER BY total_revenue DESC;


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 13) Which product categories have the highest profit margins on Olist, and how can the company increase profitability across different categories? 
 
WITH profit_margin AS(
    SELECT products.product_category AS category_name,
           ROUND(SUM(order_items.price), 2) AS total_revenue,
           ROUND(SUM(order_items.freight_value), 2) AS total_shipping_costs,
           ROUND(SUM(order_payments.payment_value), 2) AS total_payments_received,
           ROUND(SUM(order_payments.payment_value - order_items.freight_value), 2) AS total_profit,
           ROUND(((SUM(order_payments.payment_value - order_items.freight_value)) / SUM(order_items.price)) * 100,2) AS pct_profit_margin
    FROM orders
    JOIN order_items ON order_items.order_id = orders.order_id
    JOIN order_payments ON order_payments.order_id = orders.order_id
    JOIN products ON products.product_id = order_items.product_id
    JOIN sellers ON sellers.seller_id = order_items.seller_id
    GROUP BY products.product_category
)

SELECT
    category_name,
    total_revenue,
    total_shipping_costs,
    total_payments_received,
    total_profit,
    pct_profit_margin
FROM
    profit_margin
ORDER BY
    pct_profit_margin DESC;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 14) Geolocation having high customer density. Calculate customer retention rate according to geolocations

WITH customer_order AS(
    SELECT
        customers.customer_unique_id,
        customers.state,
        COUNT(orders.order_id) AS total_orders
    FROM customers
    JOIN orders ON orders.customer_id = customers.customer_id
    GROUP BY customers.customer_unique_id, customers.state
),

geolocation_retention AS(
    SELECT state,
           COUNT(DISTINCT customer_unique_id) AS total_customers,
           COUNT(DISTINCT CASE WHEN total_orders>1 THEN customer_unique_id END) AS repeated_customers
    FROM customer_order
    GROUP BY state
)

SELECT 
    state,
    total_customers,
    repeated_customers,
    ROUND((repeated_customers::NUMERIC / NULLIF(total_customers, 0)) * 100, 2) AS retention_rate_pct
FROM geolocation_retention
ORDER BY total_customers DESC, retention_rate_pct DESC;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 15) How severely do late deliveries impact customer review scores (rating) and repurchase rates? 

WITH order_performance AS (
    SELECT 
        o.order_id,
        c.customer_unique_id,
        o.estimated_delivery_date,
        o.delivered_customer_date,
        CASE 
            WHEN o.delivered_customer_date > o.estimated_delivery_date THEN 'Late Delivery'
            WHEN o.delivered_customer_date <= o.estimated_delivery_date THEN 'On-Time Delivery'
            ELSE 'Not Delivered / Missing Data'
        END AS delivery_status,
        EXTRACT(DAY FROM (o.delivered_customer_date - o.estimated_delivery_date)) AS days_late
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'delivered' 
      AND o.delivered_customer_date IS NOT NULL 
      AND o.estimated_delivery_date IS NOT NULL
),
customer_repeat_orders AS (
    -- Pre-calculate total orders per unique customer to track retention
    SELECT 
        customer_unique_id,
        COUNT(order_id) AS total_customer_orders
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY customer_unique_id
),
order_ratings AS (
    SELECT 
        order_id,
        AVG(rating) AS avg_rating
    FROM order_reviews
    GROUP BY order_id
)
SELECT 
    op.delivery_status,
    COUNT(DISTINCT op.order_id) AS total_orders,
    ROUND(AVG(orv.avg_rating)::NUMERIC, 2) AS average_review_score,
    ROUND(
        (COUNT(DISTINCT CASE WHEN cro.total_customer_orders > 1 THEN op.customer_unique_id END)::NUMERIC
         / NULLIF(COUNT(DISTINCT op.customer_unique_id), 0)) * 100, 
        2
    ) AS customer_repeat_rate_pct,
    ROUND(AVG(CASE WHEN op.days_late > 0 THEN op.days_late END)::NUMERIC, 1) AS avg_delay_duration_days
FROM order_performance op
LEFT JOIN order_ratings orv ON op.order_id = orv.order_id
LEFT JOIN customer_repeat_orders cro ON op.customer_unique_id = cro.customer_unique_id
GROUP BY op.delivery_status;


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------