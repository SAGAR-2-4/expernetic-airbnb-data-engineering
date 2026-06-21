def build_master_dataset(
    listings,
    review_summary,
    calendar_summary,
    city_name
):
    """
    Build enriched listing-level master dataset.
    """

    master = (
        listings
        .merge(
            review_summary,
            left_on="id",
            right_on="listing_id",
            how="left"
        )
        .merge(
            calendar_summary,
            left_on="id",
            right_on="listing_id",
            how="left"
        )
    )

    # Remove duplicate join columns created during merge
    drop_cols = [
        col for col in ["listing_id_x", "listing_id_y"]
        if col in master.columns
    ]

    master = master.drop(columns=drop_cols)

    # Add city name for cross-city analysis
    master["city"] = city_name

    return master