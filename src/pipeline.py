from pathlib import Path

from ingestion.load_data import load_city_data
from profiling.validate_data import validate_data
from cleaning.clean_listings import clean_listings
from transformation.review_aggregation import aggregate_reviews
from transformation.calendar_aggregation import aggregate_calendar
from transformation.build_master import build_master_dataset


def run_city_pipeline(city_folder, city_name):
    """
    Run end-to-end pipeline for one city.

    Steps:
    1. Load raw city data
    2. Validate required files and columns
    3. Clean listings data
    4. Aggregate reviews
    5. Aggregate calendar data
    6. Build enriched city master dataset
    7. Save processed output
    """

    listings, reviews, calendar = load_city_data(city_folder)

    validate_data(listings, reviews, calendar)

    cleaned_listings = clean_listings(listings)

    review_summary = aggregate_reviews(reviews)

    calendar_summary = aggregate_calendar(calendar)

    city_master = build_master_dataset(
        cleaned_listings,
        review_summary,
        calendar_summary,
        city_name
    )

    output_dir = Path("data/processed")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = output_dir / f"{city_folder}_master.csv"

    city_master.to_csv(
        output_path,
        index=False
    )

    print(f"Saved: {output_path}")

    return city_master