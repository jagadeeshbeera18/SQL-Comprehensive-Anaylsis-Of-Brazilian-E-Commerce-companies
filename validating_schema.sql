--- Row Count Check ---
SELECT 'geolocation' AS table_name, COUNT(*) FROM geolocation
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL
SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL
SELECT 'category_names_english', COUNT(*) FROM category_names_english
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;

--- Foreign key & Integrity Checks ---
SELECT COUNT(*) AS orphaned_orders
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orphaned_items
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

--- Data Sample & Quality Check ---
SELECT 
    COALESCE(c.product_category_eng, p.product_category, 'Unknown') AS category_eng,
    COUNT(oi.order_id) AS total_items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_names_english c ON p.product_category = c.product_category
GROUP BY category_eng
ORDER BY total_revenue DESC
LIMIT 10;