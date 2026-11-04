from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/product_category_name_translation.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_category_names(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"category names translation dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_category_names(df:pd.DataFrame):
    required_columns=["product_category_name","product_category_name_english"]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")

    
    missing_value_count=(df[required_columns].isna().sum().to_dict())
    duplicate_categories=int(df['product_category_name'].duplicated().sum())
    duplicate_categories_eng=int(df['product_category_name_english'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_values={}
    for column in ["product_category_name","product_category_name_english"]:
        blank_values[column]=int((df[column].astype("string").isna()|df[column].astype("string").str.strip().eq("")).sum())
    
    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_value_count.items()
        },
        "duplicate_categories": duplicate_categories,
        "duplicate_categories_eng": duplicate_categories_eng,
        "duplicate_full_rows": duplicate_rows,
        "blank_values": blank_values,
        
    }
    return report

def main():
    category_names=load_category_names(DATA_FILE)
    report=validate_category_names(category_names)
    report_path=REPORT_DIR/"category_names_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nCategory_names Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()