def aggregate_reviews(reviews):
    """
    Aggregate raw review records to listing-level review metrics.
    """

    review_summary = (
        reviews
        .groupby("listing_id")
        .agg(
            total_reviews=("id", "count"),
            first_review_date=("date", "min"),
            last_review_date=("date", "max")
        )
        .reset_index()
    )

    return review_summary