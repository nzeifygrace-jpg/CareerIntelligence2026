"""
extract_skills.py — CareerIntelligence2026
Scans job descriptions for known skills/tools and builds a job_skills
table: one row per (job_id, skill) pair found.
"""

import re
import pandas as pd
from pathlib import Path

CLEANED_DIR = Path(__file__).resolve().parent.parent / "data" / "cleaned"
INPUT_PATH = CLEANED_DIR / "jobs_clean.csv"
OUTPUT_PATH = CLEANED_DIR / "job_skills.csv"

# Skill keywords relevant to Analyst roles across SaaS, Healthcare, and Sales.
# Each entry: (display name, list of text patterns to search for)
# Patterns are matched case-insensitively as whole words/phrases.
SKILLS = {
    "SQL": [r"\bsql\b"],
    "Python": [r"\bpython\b"],
    "R": [r"\bR\b"],
    "Excel": [r"\bexcel\b"],
    "Power BI": [r"\bpower\s?bi\b"],
    "Tableau": [r"\btableau\b"],
    "Looker": [r"\blooker\b"],
    "SAS": [r"\bsas\b"],
    "VBA": [r"\bvba\b"],
    "Salesforce": [r"\bsalesforce\b"],
    "HubSpot": [r"\bhubspot\b"],
    "Google Analytics": [r"\bgoogle analytics\b"],
    "Snowflake": [r"\bsnowflake\b"],
    "AWS": [r"\baws\b"],
    "Azure": [r"\bazure\b"],
    "GCP": [r"\bgcp\b|\bgoogle cloud\b"],
    "ETL": [r"\betl\b"],
    "Machine Learning": [r"\bmachine learning\b|\bml\b"],
    "A/B Testing": [r"\ba/b testing\b|\bab testing\b"],
    "Jira": [r"\bjira\b"],
    "Statistics": [r"\bstatistics\b|\bstatistical\b"],
    "Data Visualization": [r"\bdata visualization\b"],
    "Power Query": [r"\bpower query\b"],
    "DAX": [r"\bdax\b"],
}


def find_skills(description: str) -> list:
    """Return list of skill names found in one job description."""
    if not isinstance(description, str):
        return []

    found = []
    text = description.lower()

    for skill_name, patterns in SKILLS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.append(skill_name)
                break

    return found


def main():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} jobs from {INPUT_PATH.name}")

    rows = []
    jobs_with_no_skills = 0

    for _, job in df.iterrows():
        skills_found = find_skills(job.get("description", ""))

        if not skills_found:
            jobs_with_no_skills += 1

        for skill in skills_found:
            rows.append({"job_id": job["job_id"], "skill": skill})

    job_skills_df = pd.DataFrame(rows)
    job_skills_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nTotal (job, skill) pairs found: {len(job_skills_df)}")
    print(f"Jobs with NO recognized skills mentioned: {jobs_with_no_skills}")
    print(f"Saved to: {OUTPUT_PATH}")

    print("\nTop 15 most frequently mentioned skills:")
    print(job_skills_df["skill"].value_counts().head(15).to_string())


if __name__ == "__main__":
    main()