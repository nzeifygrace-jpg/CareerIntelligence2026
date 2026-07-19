"""
clean.py — CareerIntelligence2026
Cleans all_jobs_raw.csv: removes duplicates, calculates avg_salary,
labels estimated vs employer-stated salaries, fills missing location text.
"""

import pandas as pd
from pathlib import Path

CLEANED_DIR = Path(__file__).resolve().parent.parent / "data" / "cleaned"
INPUT_PATH = CLEANED_DIR / "all_jobs_raw.csv"
OUTPUT_PATH = CLEANED_DIR / "jobs_clean.csv"


def main():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} rows from {INPUT_PATH.name}")

    # 1. Remove duplicate job postings (same job_id appearing more than once)
    before = len(df)
    df = df.drop_duplicates(subset="job_id", keep="first")
    print(f"Removed {before - len(df)} duplicate rows (same job_id).")

    # 2. Rename salary_is_predicted -> is_estimated, as True/False
    df["is_estimated"] = df["salary_is_predicted"].map({1: True, 0: False})
    df = df.drop(columns=["salary_is_predicted"])

    # 3. Calculate avg_salary only where both min and max exist
    df["avg_salary"] = df[["min_salary", "max_salary"]].mean(axis=1)

    # 4. Fill missing city/state with a clear label instead of blank
    df["city"] = df["city"].fillna("Not specified")
    df["state"] = df["state"].fillna("Not specified")

    # 5. Clean the date to just YYYY-MM-DD
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce").dt.date

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nFinal cleaned dataset: {len(df)} rows")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"\nJobs with estimated salary: {df['is_estimated'].sum()}")
    print(f"Jobs with employer-stated salary: {(~df['is_estimated']).sum()}")
    print(f"Jobs with NO salary data at all: {df['avg_salary'].isna().sum()}")


if __name__ == "__main__":
    main()