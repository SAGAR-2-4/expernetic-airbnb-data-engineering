"""
Load Data Module

Purpose:
This module loads raw Airbnb city datasets from the data/raw folder.

Input:
- City folder name, e.g. "london" or "new_york"

Output:
- listings DataFrame
- reviews DataFrame
- calendar DataFrame

Why this exists:
Instead of hardcoding separate read_csv commands for every city,
this function allows the same ingestion logic to be reused for any city.
"""


from pathlib import Path
import pandas as pd


def load_city_data(city: str):
    project_root = Path(__file__).resolve().parents[2]
    base_path = project_root / "data" / "raw" / city

    if not base_path.exists():
        raise FileNotFoundError(f"City raw data folder not found: {base_path}")

    listings = pd.read_csv(base_path / "listings.csv.gz")
    reviews = pd.read_csv(base_path / "reviews.csv.gz")
    calendar = pd.read_csv(base_path / "calendar.csv.gz")

    return listings, reviews, calendar