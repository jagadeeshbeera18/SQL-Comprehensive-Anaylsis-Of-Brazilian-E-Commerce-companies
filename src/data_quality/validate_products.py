from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_products_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_products(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Products dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_products(df:pd.DataFrame):
    required_columns=["product_id","product_category_name","product_name_lenght","product_description_lenght",
                      "product_photos_qty","product_weight_g","product_length_cm",
                      "product_height_cm","product_width_cm"
                      ]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    missing_value_count=(df[required_columns].isna().sum().to_dict())
    duplicate_product_id=int(df['product_id'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_product_ids=int(df['product_id'].astype("string").str.strip().eq("").sum())

    numerical_columns=["product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g",
                       "product_length_cm","product_height_cm","product_width_cm"
                       ]
    invalid_numeric_values = {}
    for column in numerical_columns:
        if column in df.columns:
            original_not_null = df[column].notna()
            numeric_series = pd.to_numeric(df[column], errors="coerce")
            invalid_count = int((original_not_null & numeric_series.isna()).sum())
            invalid_numeric_values[column] = invalid_count
        

    measurements_columns=["product_description_lenght","product_photos_qty","product_weight_g",
                          "product_length_cm","product_height_cm","product_width_cm"
                          ]
    negative_values={}
    for column in measurements_columns:
        values=pd.to_numeric(df[column],errors="coerce")
        negative_values[column]=int((values<0).sum())

    category_count=(df["product_category_name"].fillna("missing").value_counts().head(10).to_dict())

    
    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_value_count.items()
        },
        "duplicate_order_ids": duplicate_product_id,
        "duplicate_full_rows": duplicate_rows,
        "blank_order_ids": blank_product_ids,
        "invalid_numeric_values": invalid_numeric_values,
        "negative_measurements": negative_values,
        "top_10_categories": {key:int(value) for key,value in category_count.items()},
    }
    return report

def main():
    products=load_products(DATA_FILE)
    report=validate_products(products)
    report_path=REPORT_DIR/"products_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nProducts Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()