import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parent
RAW_DIR=ROOT_DIR/"data"/"raw"
PROCESSED_DIR=ROOT_DIR/"data"/"processed"
PROCESSED_DIR.mkdir(parents=True,exist_ok=True)

products=pd.read_csv(RAW_DIR/"olist_products_dataset.csv")
categories=pd.read_csv(RAW_DIR/"product_category_name_translation.csv")

product_categories=set(products['product_category_name'].dropna().unique())
translated_categories=set(categories['product_category_name'].dropna().unique())
unmatched=product_categories-translated_categories

print("Unmatched category count:",len(unmatched))
print("Unmatched category names:")
for category in sorted(unmatched):
    count=(products['product_category_name']==category).sum()
    print(f"{category}:{count} products")

# Manually verified category translations
manual_mappings={"pc_gamer":"gaming_pc","portateis_cozinha_e_preparadores_de_alimentos":"kitchen_appliances"}

# Add missing mappings to the translation dataset
manual_df=pd.DataFrame(manual_mappings.items(),columns=["product_category_name","product_category_name_english"])
updated_categories=pd.concat([categories, manual_df],ignore_index=True)

print("Original mappings:",len(categories))
print("Updated mappings:",len(updated_categories))
print("\nMissing categories after mapping:")

remaining=(set(products["product_category_name"].dropna().unique())- set(updated_categories["product_category_name"].dropna().unique()))
print(remaining)

output_path=PROCESSED_DIR/"clean_category_names.csv"
updated_categories.to_csv(output_path,index=False)
print("\n category mapping saved successfully!")
print("output:",output_path)
print("Total category mappings:",len(updated_categories))

print("=" * 60)
# ---- Identify orders without item records ----

orders=pd.read_csv(RAW_DIR/"olist_orders_dataset.csv")
order_items=pd.read_csv(RAW_DIR/"olist_order_items_dataset.csv")
orders_without_items=orders[~orders['order_id'].isin(order_items['order_id'])].copy()

print("\n Total orders without items:",len(orders_without_items))
print("\n order status distribution:")
print(orders_without_items["order_status"].value_counts(dropna=False))
print("\nPercentage by order status:")
print(orders_without_items['order_status'].value_counts(normalize=True).mul(100).round(2))

# investigating the unusual order status
unusual_status=['created','invoiced','shipped']
unusual_orders=orders_without_items[orders_without_items['order_status'].isin(unusual_status)]

print("\n unusal orders without item records:")
print(unusual_orders[['order_id','customer_id','order_status','order_purchase_timestamp',
                     'order_delivered_carrier_date','order_delivered_customer_date']].to_string(index=False))
print("\n Total unusual orders:",len(unusual_orders))
