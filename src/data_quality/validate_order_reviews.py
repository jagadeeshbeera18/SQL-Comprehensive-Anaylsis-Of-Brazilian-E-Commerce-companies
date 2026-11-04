from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT=Path(__file__).resolve().parents[2]
DATA_FILE=(PROJECT_ROOT/"data/raw/olist_order_reviews_dataset.csv")
REPORT_DIR=PROJECT_ROOT/"reports" 
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def load_order_reviews(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Order_reviews dataset not found:{file_path}")
    return pd.read_csv(file_path)


def validate_order_reviews(df:pd.DataFrame):
    required_columns=["review_id","order_id","review_score","review_comment_title","review_comment_message",
                      "review_creation_date","review_answer_timestamp"
                      ]
    missing_columns=[column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns{missing_columns}")
    missing_values={column:int(count) for column,count in df.isnull().sum().items()}
    duplicate_review_id=int(df['review_id'].duplicated().sum())
    duplicate_rows=int(df.duplicated().sum())
    blank_identifiers={}
    for column in ["review_id","order_id"]:
        blank_identifiers[column]=int(df[column].astype("string").str.strip().eq("").sum())

    df['review_score']=pd.to_numeric(df['review_score'])
    invalid_review_score=int((df['review_score'].isna()|~df['review_score'].between(1,5)|(df['review_score']%1!=0)).sum())

    date_columns=["review_creation_date","review_answer_timestamp"]
    invalid_dates={}
    for column in date_columns:
        parsed_dates=pd.to_datetime(df[column],errors="coerce")
        invalid_dates[column]=int(parsed_dates.isna().sum())

    creation_dates=pd.to_datetime(df['review_creation_date'],errors="coerce")
    anwers_dates=pd.to_datetime(df['review_answer_timestamp'],errors="coerce")
    invalid_date_order=int((creation_dates.notna()&anwers_dates.notna()&(anwers_dates<creation_dates)).sum())

    score_distribution={str(int(key)):int(value) for key,value in df['review_score'].value_counts().sort_index().items() if pd.notna(key)}

    report = {
        "dataset": "olist_orders_dataset.csv",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": {
            key: int(value)
            for key, value in missing_values.items()
        },
        "duplicate_order_ids": duplicate_review_id,
        "duplicate_full_rows": duplicate_rows,
        "blank_values": blank_identifiers,
        "invalid_review_score": invalid_review_score,
        "invalid_date_order": invalid_date_order,
        "score_distribution": score_distribution
    }
    return report

def main():
    order_reviews=load_order_reviews(DATA_FILE)
    report=validate_order_reviews(order_reviews)
    report_path=REPORT_DIR/"order_reviews_validation_report.json"
    with report_path.open('w',encoding="utf-8") as file:
        json.dump(report,file,indent=4)
    print("\nOrder Reviwes Data Validation")
    print("="*50)
    print(json.dumps(report,indent=4))
    print(f"\nReport saved to {report_path}")

if __name__=="__main__":
    main()