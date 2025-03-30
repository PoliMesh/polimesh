import csv
import sys
from datetime import datetime

REQUIRED_FIELDS = ["official_id", "date", "statement_text", "statement_type", "source_url", "support_stance", "president"]

def validate_row(row, line_num):
    errors = []
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            errors.append(f"Missing '{field}'")

    try:
        datetime.strptime(row["date"], "%Y-%m-%d")
    except ValueError:
        errors.append("Invalid date format (expected YYYY-MM-DD)")

    if row.get("support_stance") not in {"support", "oppose", "switch_to_support", "switch_to_oppose"}:
        errors.append("Invalid support_stance value")

    return errors

def validate_csv(file_path):
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            errors = validate_row(row, i)
            if errors:
                print(f"Line {i}: {'; '.join(errors)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_submission.py <csv_file>")
        sys.exit(1)

    validate_csv(sys.argv[1])
