# CareerIntelligence2026

A data analytics project analyzing 2026 US Analyst job postings on Adzuna across three industries: **SaaS, Healthcare, and Sales**; covering salaries, skills, and hiring trends. Built end-to-end: data extraction, cleaning, SQL modeling, and Power BI dashboards.

## Project Goal

As a career changer moving from clinical Veterinary Medicine into data analytics, I wanted to answer a practical question for my own job search: *what skills and industries should I focus on to maximize my chances of landing a remote analyst role in 2026?*

## Tech Stack

- **Python** (pandas, requests, sqlalchemy): data extraction, cleaning, and loading
- **Adzuna API**: job posting data source
- **SQL Server (SSMS)**: relational data modeling and analysis
- **Power BI**: dashboard visualization
- **Git/GitHub**: version control

## Pipeline Overview

```
Adzuna API
    ↓
extract_adzuna.py    → raw JSON (data/raw/)
    ↓
transform.py          → flattened CSV (data/cleaned/all_jobs_raw.csv)
    ↓
clean.py               → deduplicated, labeled dataset (data/cleaned/jobs_clean.csv)
    ↓
extract_skills.py     → skill keyword extraction (data/cleaned/job_skills.csv)
    ↓
load_to_sql.py         → loads into SQL Server
    ↓
SQL analysis + Power BI dashboards
```

### 1. Data Collection
Pulled job postings from the [Adzuna API](https://developer.adzuna.com/) across 17 role/industry search combinations (e.g., "Data Analyst SaaS," "Health Data Analyst," "Sales Operations Analyst"), covering SaaS, Healthcare, and Sales industries. Raw JSON responses saved before any transformation, so the pipeline can be re-run downstream without re-hitting the API.

**Result:** 2,168 raw job postings collected.

### 2. Cleaning
- Flattened nested JSON into a single tabular dataset
- Removed 150 duplicate postings → **2,018 final rows**
- Labeled salaries as employer-stated vs. Adzuna-estimated (`is_estimated` flag)
- Calculated `avg_salary` from min/max salary ranges
- Standardized missing location data

### 3. Skills Extraction
Scanned job description text for a defined list of relevant tools/skills (SQL, Python, Power BI, Excel, Tableau, AWS, etc.), producing a normalized `job_skills` table (one row per job-skill pair) for clean SQL joins.

### 4. Work Arrangement Classification
Classified postings as Remote / Hybrid / On-site / Not specified based on keyword matching in job titles and descriptions.

### 5. SQL Modeling
Loaded cleaned data into SQL Server with a proper relational structure (`jobs`, `job_skills`, plus a `skill_cooccurrence` view) to support real analytical queries, salary by skill, top hiring companies, skill co-occurrence, and more.

### 6. Power BI Dashboards
Three dashboards built on the SQL Server data:
- **Executive Overview**: total postings, average salary, remote %, top companies and states
- **Salary Intelligence**: salary by industry, job title, state, and estimated vs. stated comparison
- **Skills Intelligence**: most in-demand skills, salary by skill, skills by industry, skill co-occurrence

## Key Findings

- **SaaS pays the highest average salary** among the three industries, followed by Healthcare and Sales.
- **Adzuna's estimated salaries closely track employer-stated ones** (within ~$1K on average), lending confidence to using estimated figures where real ones aren't available.
- **Statistics and Salesforce were the most frequently mentioned skills**, though overall skill mention volume was limited by a data source constraint (see below).
- Only **~13% of postings explicitly mention remote work** in the available text, likely an undercount given the description truncation limitation.

## Known Data Limitations

Being transparent about data quality is part of good analysis:

- **Description truncation:** Adzuna's free-tier API returns job descriptions truncated to 500 characters, even when requesting `full_description=1`. This limited skill and work-arrangement detection to whatever appears in the first 500 characters of each posting, likely undercounting true skill frequency and remote/hybrid mentions.
- **Salary estimates:** ~76% of postings had Adzuna-estimated (not employer-stated) salaries. These are clearly flagged via the `is_estimated` column throughout the dataset and dashboards.
- **Small sample for some searches:** A few role searches (e.g. "Sales Operations Analyst SaaS") returned very few or zero results due to Adzuna's literal keyword matching.

## Repository Structure

```
CareerIntelligence2026/
│
├── scripts/
│   ├── config.py           # Search term definitions
│   ├── extract_adzuna.py   # Pulls raw data from Adzuna API
│   ├── transform.py        # Flattens raw JSON into CSV
│   ├── clean.py             # Deduplicates, labels, standardizes
│   ├── extract_skills.py   # Keyword-based skill extraction
│   └── load_to_sql.py       # Loads cleaned data into SQL Server
│
├── data/
│   └── cleaned/
│       ├── jobs_clean.csv
│       └── job_skills.csv
│
├── requirements.txt
├── .env.example
└── README.md
```

## Author

Dr. Ifunanya Grace Nze
[LinkedIn](https://linkedin.com/in/drifunanyanze/) | [GitHub](https://github.com/nzeifygrace-jpg)
