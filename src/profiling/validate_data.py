def validate_data(listings, reviews, calendar):
    """
    Basic validation checks.
    """

    print("Running validation...")

    assert len(listings) > 0, "Listings dataset is empty."
    assert len(reviews) > 0, "Reviews dataset is empty."
    assert len(calendar) > 0, "Calendar dataset is empty."

    assert "id" in listings.columns, \
        "Listings missing 'id' column."

    assert "listing_id" in reviews.columns, \
        "Reviews missing 'listing_id' column."

    assert "listing_id" in calendar.columns, \
        "Calendar missing 'listing_id' column."

    print("Validation passed.")