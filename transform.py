"""
transform.py — CareerIntelligence2026
Combines all raw JSON files in data/raw into one flat CSV.
"""

import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
CLEANED_DIR = Path(__file__).resolve().parent.parent / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = CLEANED_DIR / "all_jobs_raw.csv"


def extract_fields(job: dict) -> dict:
    """Pull out only the fields we care about from one raw Adzuna job record."""
    location = job.get("location", {}) or {}
    location_area = location.get("area", [])

    # Adzuna nests city/state inside a list like ["US", "California", "San Francisco"]
    state = location_area[1] if len(location_area) > 1 else None
    city = location_area[2] if len(location_area) > 2 else None

    company = job.get("company", {}) or {}
    category = job.get("category", {}) or {}

    return {
        "job_id": job.get("id"),
        "job_title": job.get("title"),
        "company": company.get("display_name"),
        "industry": job.get("_industry"),
        "search_role": job.get("_search_role"),
        "city": city,
        "state": state,
        "min_salary": job.get("salary_min"),
        "max_salary": job.get("salary_max"),
        "salary_is_predicted": job.get("salary_is_predicted"),
        "contract_type": job.get("contract_type"),
        "contract_time": job.get("contract_time"),
        "category": category.get("label"),
        "date_posted": job.get("created"),
        "description": job.get("description"),
        "url": job.get("redirect_url"),
    }


def main():
    all_jobs = []
    json_files = list(RAW_DIR.glob("*.json"))

    print(f"Found {len(json_files)} raw JSON files in {RAW_DIR}")

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)

        for job in jobs:
            all_jobs.append(extract_fields(job))

    df = pd.DataFrame(all_jobs)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Combined {len(df)} total job rows.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nColumn names in your new CSV:")
    print(list(df.columns))
    print("\nSample of first 3 rows:")
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()