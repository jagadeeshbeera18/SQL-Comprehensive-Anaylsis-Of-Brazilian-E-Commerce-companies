import subprocess
import sys
from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[2]

# All nine validation scripts
validation_scripts=[
    "validate_orders.py",
    "validate_products.py",
    "validate_customers.py",
    "validate_order_items.py",
    "validate_payments.py",
    "validate_sellers.py",
    "validate_order_reviews.py",
    "validate_geolocation.py",
    "validate_category_names.py",
]

 
print("=" * 65)
print("RETAIL INTELLIGENCE & DEMAND PLANNING PLATFORM")
print("DATA QUALITY VALIDATION PLATFORM")
print("=" * 65)

successful_scripts = []
failed_scripts = []

for script in validation_scripts:
    script_path = ROOT_DIR / "src" / "data_quality" / script

    print(f"\nRunning: {script}")
    print("-" * 45)

    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        failed_scripts.append(script)
        continue

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode == 0:
        successful_scripts.append(script)
        print("STATUS: SUCCESS")
    else:
        failed_scripts.append(script)
        print("STATUS: FAILED")
        if result.stderr:
            print(result.stderr)

print("\n" + "=" * 65)
print("DATA QUALITY PIPELINE SUMMARY")
print("=" * 65)

print(f"Total scripts: {len(validation_scripts)}")
print(f"Successful: {len(successful_scripts)}")
print(f"Failed: {len(failed_scripts)}")

if failed_scripts:
    print("\nFailed scripts:")
    for script in failed_scripts:
        print(f"- {script}")
    print("\nPlease fix the errors and run the pipeline again.")
    sys.exit(1)
else:
    print("\nAll nine validation scripts executed successfully!")
    print("Review the JSON reports in the reports/ directory.")
if not failed_scripts:
    print("\nGenerating consolidated quality summary...")
    summary_script=(ROOT_DIR/ "src"/ "data_quality"/ "generate_quality_summary.py")
    result = subprocess.run(
        [sys.executable, str(summary_script)],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Failed to generate consolidated quality summary.")
        print(result.stderr)
        sys.exit(1)
else:
    print("\nSummary generation skipped because some validations failed.")
sys.exit(0)

