import pandas as pd
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
REPORT_DIR = ROOT_DIR / "reports"

REPORT_DIR.mkdir(parents=True,exist_ok=True)

orders=pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
customers=pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
products=pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
sellers=pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
order_items=pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
categories=pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

print("=" * 65)
print("OLIST CROSS-DATASET VALIDATION")
print("=" * 65)

# Define reusable validation function
def check_foreign_key(child_df,child_column,parent_df,parent_column,relationship_name):
    """
    Check whether child-table IDs exist in the parent table.
    """
    child_values=child_df[child_column].dropna()
    parent_values=parent_df[parent_column].dropna()
    unmatched=~child_values.isin(parent_values)
    unmatched_count=int(unmatched.sum())

    print(f"\n{relationship_name}")
    print("-" * 50)
    print(f"Child records checked: {len(child_values)}")
    print(f"Unmatched records: {unmatched_count}")

    return {
        "relationship": relationship_name,
        "child_records_checked": int(len(child_values)),
        "unmatched_records": unmatched_count,
    }

# Validate relationships
results = []

# Orders -> Customers
results.append(
    check_foreign_key(
        orders,
        "customer_id",
        customers,
        "customer_id",
        "Orders -> Customers"
    )
)

# Order items -> Orders
results.append(
    check_foreign_key(
        order_items,
        "order_id",
        orders,
        "order_id",
        "Order Items -> Orders"
    )
)

# Order items -> Products
results.append(
    check_foreign_key(
        order_items,
        "product_id",
        products,
        "product_id",
        "Order Items -> Products"
    )
)

# Order items -> Sellers
results.append(
    check_foreign_key(
        order_items,
        "seller_id",
        sellers,
        "seller_id",
        "Order Items -> Sellers"
    )
)

# Products -> Category translation
results.append(
    check_foreign_key(
        products.dropna(subset=["product_category_name"]),
        "product_category_name",
        categories,
        "product_category_name",
        "Products -> Category Translation"
    )
)

# Check order-level coverage
print("\n" + "=" * 65)
print("ORDER COVERAGE")
print("=" * 65)

orders_with_items=order_items["order_id"].nunique()
orders_without_items=orders.loc[~orders["order_id"].isin(order_items["order_id"]),"order_id"].nunique()

print("Orders in orders dataset:", orders["order_id"].nunique())
print("Orders with item records:", orders_with_items)
print("Orders without item records:", orders_without_items)

# Orders without items may be cancelled or otherwise not fulfilled.

# Save validation report
report = {
    "relationships_checked": len(results),
    "relationship_results": results,
    "order_coverage": {
        "total_orders": int(orders["order_id"].nunique()),
        "orders_with_items": int(orders_with_items),
        "orders_without_items": int(orders_without_items),
    }
}

report_path=REPORT_DIR/"cross_dataset_validation_report.json"

with open(report_path,"w",encoding="utf-8") as file:
    json.dump(report,file,indent=4)
print("\nCross-dataset validation completed.")
print(f"Report saved to: {report_path}")