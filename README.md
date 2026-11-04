================================================================================
OLIST E-COMMERCE ANALYTICS PROJECT
Data Profiling  >  Validation  >  Cleaning  >  PostgreSQL Database  >  Business Analysis
================================================================================


--------------------------------------------------------------------------------
1. PROJECT OVERVIEW
--------------------------------------------------------------------------------
This project takes the Brazilian Olist e-commerce dataset (9 CSV files) through
a complete analytics workflow:

  1. Profile and validate each raw dataset and write the findings to reports
  2. Clean the data and export "clean_*.csv" files
  3. Build a relational PostgreSQL database (tables, primary keys, foreign keys)
  4. Load the cleaned CSVs and verify the load with SQL integrity checks
  5. Standardise text fields (city and state names) directly in SQL
  6. Answer 15 business questions about revenue, orders, categories, payments,
     sellers, customers, reviews, profitability, geography and delivery
     performance

Tools used: Python (profiling / validation / cleaning, inferred from the
generated reports), PostgreSQL (schema, loading, cleaning, analysis), SQL
(CTEs, window functions, aggregations, joins, correlation).


--------------------------------------------------------------------------------
2. FILES IN THIS FOLDER
--------------------------------------------------------------------------------
SQL scripts
  schema_creation.sql      Creates the 9 tables with keys/constraints and loads
                           the cleaned CSVs using COPY
  validating_schema.sql    Post-load checks: row counts, orphan records, and a
                           sample top-10 category revenue query
  olist_Analytics.sql      Table previews, SQL data cleaning, and the 15
                           business-question queries

Quality / validation reports (generated during the Python stage)
  orders_validation_report.json
  order_items_validation_report.json
  payments_validation_report.json
  order_reviews_validation_report.json
  products_validation_report.json
  customers_validation_report.json
  customers_cleaning_report.json
  sellers_validation_report.json
  category_names_validation_report.json
  category_names_profiling_report.txt
  order_geolocation_report.json
  order_geolocation_validation_report.json
  cross_dataset_validation_report.json
  consolidated_quality_report.json
  consolidated_quality_summary.csv

Note: the Python scripts that produced the reports, the raw CSVs and the
"clean_*.csv" files were not part of the uploaded folder. Section 4 is
therefore based on what the reports show.


--------------------------------------------------------------------------------
3. DATASETS (9 TABLES)
--------------------------------------------------------------------------------
Dataset              Rows        Columns   Database table
-------------------  ----------  --------  -----------------------
orders                   99,441         8  orders
order_items             112,650         7  order_items
payments                103,886         5  order_payments
order_reviews            99,224         7  order_reviews
products                 32,951         9  products
customers                99,441         5  customers
sellers                   3,095         4  sellers
geolocation           1,000,163         5  geolocation
category_names               71         2  category_names_english

Relationships:
  orders        -> customers            (customer_id)
  order_items   -> orders               (order_id)
  order_items   -> products             (product_id)
  order_items   -> sellers              (seller_id)
  order_payments-> orders               (order_id)
  order_reviews -> orders               (order_id)
  products      -> category_names_english (product_category)


--------------------------------------------------------------------------------
4. STAGE 1 - DATA PROFILING, VALIDATION AND CLEANING (PYTHON)
--------------------------------------------------------------------------------
Each dataset was checked for: missing values, duplicate rows, duplicate keys,
blank key values, invalid numeric values, negative measurements, invalid
state codes / zip codes, and date-logic problems. A consolidated report
combines the results for all 9 datasets (9 processed, 0 missing report files,
0 missing required columns, 0 fully duplicated rows in any dataset except
geolocation's own report).

KEY FINDINGS BY DATASET

Orders (99,441 rows)
  - Missing: order_approved_at 160, order_delivered_carrier_date 1,783,
    order_delivered_customer_date 2,965 (4,908 missing values in total)
  - No duplicate order IDs; no deliveries before purchase; no estimated
    delivery dates before purchase
  - The orders table in the database carries two extra columns,
    delivery_date_quality_issue and carrier_date_quality_issue, which flag
    date problems found during cleaning

Order items (112,650 rows)
  - No missing values, no duplicates, no invalid prices, freight values or
    shipping dates

Payments (103,886 rows)
  - No missing values or duplicates
  - 2 records with invalid payment installments
  - Payment types: credit_card 76,795 | boleto 19,784 | voucher 5,775 |
    debit_card 1,529 | not_defined 3

Order reviews (99,224 rows)
  - Missing review titles 87,656 and review messages 58,247 (optional fields)
  - 814 duplicated order IDs (an order can have more than one review)
  - Score distribution: 1 star 11,424 | 2 stars 3,151 | 3 stars 8,179 |
    4 stars 19,142 | 5 stars 57,328
  - No invalid scores or invalid date order

Products (32,951 rows)
  - 610 products have no category, name length, description length or photo
    count; 2 products have no weight/dimensions
  - No duplicates, no invalid or negative measurements
  - Top categories: cama_mesa_banho (3,029), esporte_lazer (2,867),
    moveis_decoracao (2,657), beleza_saude (2,444), utilidades_domesticas
    (2,335)

Customers (99,441 rows)
  - Validation found 23,995 invalid zip codes; the cleaning report afterwards
    shows 0 invalid zip prefixes and 0 missing values, 0 duplicate customer IDs
  - No invalid state codes

Sellers (3,095 rows)
  - Fully clean: no missing values, duplicates, invalid zips or invalid states

Category names (71 rows)
  - No missing values or duplicates in either the Portuguese or English labels

Geolocation (1,000,163 rows)
  - 261,831 duplicate rows and 245,733 invalid zip codes were detected
  - No missing values, blank values or invalid coordinates
  - Strong concentration in a few states: SP 404,268 | MG 126,336 |
    RJ 121,169 | RS 61,851 | PR 57,859

CROSS-DATASET (REFERENTIAL INTEGRITY) CHECKS - 5 relationships
  - Orders -> Customers: 0 unmatched
  - Order Items -> Orders / Products / Sellers: 0 unmatched
  - Products -> Category Translation: 13 unmatched products
  - Order coverage: 98,666 of 99,441 orders have items; 775 orders have none


--------------------------------------------------------------------------------
5. STAGE 2 - DATABASE DESIGN AND LOADING  (schema_creation.sql)
--------------------------------------------------------------------------------
A PostgreSQL schema was created with DROP TABLE IF EXISTS / CREATE TABLE and
loaded with COPY from the processed "clean_*.csv" files.

  Table                   Primary key         Foreign keys
  ----------------------  ------------------  ----------------------------------
  geolocation             (none)              -
  customers               customer_id         -
  sellers                 seller_id           -
  orders                  order_id            customer_id -> customers
  order_reviews           (none)              order_id -> orders
  order_payments          (none)              order_id -> orders
  category_names_english  product_category    -
  products                product_id          product_category -> category_names_english
  order_items             (none)              product_id -> products,
                                              order_id -> orders,
                                              seller_id -> sellers

Columns were renamed to short, consistent names (for example
order_status -> status, review_score -> rating, customer_zip_code_prefix ->
zip_code_prefix). Tables are created in dependency order so foreign keys
resolve correctly.

IMPORTANT: the COPY commands use an absolute local path
(/Users/jagadeesh/Olist E-Commerce Project/data/processed/...). Update this
path before running the script on another machine.


--------------------------------------------------------------------------------
6. STAGE 3 - LOAD VALIDATION  (validating_schema.sql)
--------------------------------------------------------------------------------
  1. Row-count check across all 9 tables (UNION ALL)
  2. Orphaned orders (orders with no matching customer)
  3. Orphaned items (order items with no matching product)
  4. Sample "top 10 categories by revenue" query using COALESCE to fall back to
     the Portuguese name, or 'Unknown', when no English translation exists


--------------------------------------------------------------------------------
7. STAGE 4 - DATA CLEANING IN SQL  (olist_Analytics.sql)
--------------------------------------------------------------------------------
After previewing each table with SELECT ... LIMIT 5:

  - sellers, customers, geolocation:
      * City names converted to proper case with INITCAP
      * State abbreviations replaced with full state names using a CASE
        statement covering all 27 Brazilian states (e.g. SP -> Sao Paulo,
        MG -> Minas Gerais, RJ -> Rio de Janeiro)


--------------------------------------------------------------------------------
8. STAGE 5 - BUSINESS QUESTIONS ANSWERED  (olist_Analytics.sql)
--------------------------------------------------------------------------------
Unless noted otherwise, "genuine" orders exclude statuses 'canceled' and
'unavailable'.

 Q1  Total revenue and revenue over time
     Total revenue from payments, plus revenue by quarter and by month.

 Q2  Order volume and seasonality
     Count of genuine orders and delivered orders by year and month.

 Q3  Most popular product categories
     Sales volume per English category name, ranked highest to lowest.

 Q4  Average order value (AOV)
     Overall AOV, and AOV broken down by payment type and by product category.

 Q5  Active sellers over time
     Distinct sellers with delivered orders per year and per month, with
     LAG() to show sellers added or lost versus the previous period.

 Q6  Seller ratings vs sales performance
     Orders, total revenue and average revenue per rating (1-5), plus the
     correlation (CORR) between rating and revenue, calculated both across the
     5 rating groups and at order level. A note in the script reports a
     correlation of about 0.75 across the 5 rating groups, suggesting higher
     ratings go with higher total revenue.

 Q7  Repeat customers
     Customers (by customer_unique_id) with more than one order, their share
     of total sales, and how many customers did not repeat.

 Q8  Average customer rating and its effect on sales
     Overall average rating, then average rating, orders and revenue by
     product category and rating for delivered orders.

 Q9  Cancellation rate and seller performance
     Overall cancellation rate, canceled order count and amount lost; then the
     top 20 sellers by cancellation rate with their canceled orders, sales
     volume and average customer satisfaction.

 Q10 Top-selling categories over time
     Sales (price + freight) per category per quarter, using RANK() to return
     the number-one category in each quarter.

 Q11 Payment method usage
     Orders per payment type, and payment type by product category and by
     customer state.

 Q12 Reviews and sales / product performance
     Ratings labelled Excellent / Very Good / Good / Bad / Very Bad, with the
     number of reviews, distinct products, total revenue and average revenue.

 Q13 Profit margin by category
     Revenue, shipping costs, payments received, a profit figure
     (payment value minus freight) and percentage margin per category.

 Q14 Customer density and retention by state
     Total customers, repeat customers and retention rate per state.

 Q15 Late delivery impact
     Orders split into Late / On-Time delivery, comparing average review
     score, customer repeat rate and average delay (days).

SQL techniques used: multi-table JOINs, CTEs (WITH), window functions (LAG,
RANK), CASE expressions, EXTRACT for date parts, CORR for correlation,
NULLIF to avoid division by zero, COALESCE, HAVING, and type casts.


--------------------------------------------------------------------------------
9. HOW TO RUN THE PROJECT
--------------------------------------------------------------------------------
  1. Create a PostgreSQL database.
  2. Place the cleaned CSV files in a folder and update the file paths in
     schema_creation.sql.
  3. Run schema_creation.sql to create the tables and load the data.
  4. Run validating_schema.sql and confirm the row counts and zero orphans.
  5. Run olist_Analytics.sql section by section: first the cleaning updates,
     then each business question.

Run the state-name UPDATE statements only once. Running them again will set
state to NULL because the CASE statement no longer matches full names.


--------------------------------------------------------------------------------
10. NOTES, LIMITATIONS AND SUGGESTED IMPROVEMENTS
--------------------------------------------------------------------------------
Data quality items to be aware of
  - 13 products have categories missing from the translation table, and
    products.product_category is a foreign key to category_names_english.
    Confirm these were handled in the clean file so the load does not fail.
  - 775 orders have no order items, and 3 payments are typed 'not_defined'.
  - The geolocation file still showed 261,831 duplicate rows and 245,733
    invalid zip codes in its report. If the geolocation table is used for
    mapping, de-duplicate it first (for example, average the coordinates per
    zip prefix).
  - Every validation report has "dataset": "olist_orders_dataset.csv" and some
    products/customers/payments reports use order-related key names (such as
    duplicate_order_ids). These look like template labels; consider
    correcting them in the validation script.

Query logic worth reviewing
  - Q3, Q4, Q12, Q13: joining order_items to order_payments repeats payment
    rows for orders with several items, which can inflate revenue, AOV and
    profit figures. Aggregating payments to order level in a CTE first is the
    safer approach. Also, Q4's AOV averages payment rows rather than orders.
  - Q13: "profit" is payment minus freight, so it is a margin on revenue after
    shipping, not true profit (product costs are not in the dataset).
  - Q5 (monthly): LAG is ordered by month only; ORDER BY year, month would be
    correct across multiple years.
  - Q7: the percentage uses ROUND(ratio, 2) * 100, which limits precision;
    its denominator also includes canceled orders.
  - Q10: unlike other questions, it does not exclude canceled orders.
  - Table-preview query for products is missing a comma after product_id.
  - Several statements are not separated by semicolons; add them if running
    the whole file at once.
  - Q6's correlation is computed over only 5 data points, so treat it as
    indicative rather than conclusive.


--------------------------------------------------------------------------------
11. SKILLS DEMONSTRATED
--------------------------------------------------------------------------------
  - Data profiling and validation reporting
  - Cross-table referential integrity checking
  - Relational schema design with primary and foreign keys
  - Bulk loading with PostgreSQL COPY
  - SQL data cleaning and standardisation
  - Advanced SQL analysis (CTEs, window functions, correlation)
  - Translating business questions into SQL

================================================================================
END OF README
================================================================================
