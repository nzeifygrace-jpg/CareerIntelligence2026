"""
extract_adzuna.py — CareerIntelligence2026
Pulls job postings from Adzuna and saves raw JSON to data/raw/
"""

import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from config import SEARCHES, COUNTRY, RESULTS_PER_PAGE, MAX_PAGES_PER_SEARCH

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    raise SystemExit(
        "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY.\n"
        "Check your .env file has both values filled in."
    )

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CALL_LOG_PATH = RAW_DIR.parent.parent / "api_call_log.txt"


def log_call(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CALL_LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


def fetch_page(role: str, page: int):
    url = BASE_URL.format(country=COUNTRY, page=page)
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": role,
        "content-type": "application/json",
        "full_description": 1,
    }


    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        log_call(f"  Rate limited on '{role}' page {page}. Waiting 30s...")
        time.sleep(30)
        return fetch_page(role, page)
    else:
        log_call(f"  ERROR {response.status_code} on '{role}' page {page}: {response.text[:200]}")
        return None


def run_search(role: str, industry: str):
    safe_role_name = role.lower().replace(" ", "_")
    total_fetched = 0

    for page in range(1, MAX_PAGES_PER_SEARCH + 1):
        data = fetch_page(role, page)

        if data is None:
            break

        results = data.get("results", [])
        if not results:
            log_call(f"  '{role}' — no more results at page {page}. Stopping this search.")
            break

        for job in results:
            job["_industry"] = industry
            job["_search_role"] = role

        out_path = RAW_DIR / f"{safe_role_name}_page{page}.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)

        total_fetched += len(results)
        log_call(f"  '{role}' page {page}: {len(results)} jobs saved -> {out_path.name}")

        time.sleep(1)

    log_call(f"TOTAL for '{role}' ({industry}): {total_fetched} jobs\n")
    return total_fetched


def main():
    log_call(f"=== Starting extraction run: {len(SEARCHES)} search terms ===")
    grand_total = 0

    for search in SEARCHES:
        role = search["role"]
        industry = search["industry"]
        log_call(f"Searching: '{role}' [{industry}]")
        grand_total += run_search(role, industry)
        time.sleep(2)

    log_call(f"=== Extraction complete. Grand total jobs fetched: {grand_total} ===")
    log_call(f"Raw files saved to: {RAW_DIR}")


if __name__ == "__main__":
    main()