import pandas as pd
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]

DATA_FILE=ROOT_DIR/"data"/"raw"/"olist_products_dataset.csv"
df=pd.read_csv(DATA_FILE)

print("PRODUCT DATASET PROFILE")
print("="*60)

print('\n--- FIRST FIVE ROWS ---')
print(df.head())
print("\n--- DATASET SHAPE ---")
print(f"ROWS:{df.shape[0]}")
print(f"COLUMNS:{df.shape[1]}")
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())
print("\n--- DATASET INFORMATION ---")
print(df.info())

missing_report=pd.DataFrame({"missing_count":df.isna().sum(),"missing_percentage":(df.isna().mean()*100).round(2)})
print("\nMissing-value report:")
print(missing_report[missing_report["missing_count"]>0].sort_values("missing_count",ascending=False))

print("\nDuplicate Rows:",int(df.duplicated().sum()))
print("Duplicate product IDs:",int(df['product_id'].duplicated().sum()))

numerical_columns=["product_weight_g","product_length_cm","product_height_cm","product_width_cm"]
print('\nNumerical summary:')
print(df[numerical_columns].describe().T)

print("\nTop 15 products")
print(df['product_category_name'].value_counts(dropna=False).head(15))

# Investigate products missing catalog attributes
catalog_columns=['product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty']
missing_catalog=df[catalog_columns].isna()
print("\n Missing catalog attribute investigation")
print("="*60)

missing_all=missing_catalog.all(axis=1).sum()
print("products missing all four cataglog attributes:",int(missing_all))

missing_any=missing_catalog.any(axis=1).sum()
print("products missing atleast one catalog attribute",int(missing_any))

affected_products=df.loc[missing_catalog.any(axis=1),['product_id']+catalog_columns]
print('\nSample affected products:')
print(affected_products.head(10).to_string(index=False))

# check products missing physical measurements
measurements_column=["product_weight_g","product_length_cm","product_height_cm","product_width_cm"]
missing_measurements=df[df[measurements_column].isna().any(axis=1)]
print("\nproducts missing physical measurements:")
print(missing_measurements[['product_id']+measurements_column].to_string(index=False))

# Check whether products with missing catalog attributes appear in the order-items dataset
ORDER_ITEMS_FILE=ROOT_DIR/"data"/"raw"/"olist_order_items_dataset.csv"
order_items=pd.read_csv(ORDER_ITEMS_FILE)

# Identify products missing all four catalog attributes
missing_catalog_mask=df[['product_category_name','product_name_lenght','product_description_lenght', 
                         'product_photos_qty']].isna().all(axis=1)
incomplete_product_ids=set(df.loc[missing_catalog_mask,'product_id'])
ordered_products_ids=set(order_items['product_id'].dropna())
ordered_incomplete_ids=incomplete_product_ids&ordered_products_ids
unordered_incomplete_ids=incomplete_product_ids-ordered_products_ids
print('\nIncomplete product order inventigation')
print("="*60)
print("products missing all four attributes:",len(incomplete_product_ids))
print("Incomplete products appearing in order items:",len(ordered_incomplete_ids))
print("Incomplete products not appearing in order items:",len(unordered_incomplete_ids))

# Calculate how many order-item records involve incomplement products 
affected_order_items=order_items[order_items['product_id'].isin(incomplete_product_ids)]
print("order-item records involving incomplete products:",len(affected_order_items))
print("Total item price associated with these records:",round(affected_order_items["price"].sum(),2))

