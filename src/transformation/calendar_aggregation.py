def aggregate_calendar(calendar):
    """
    Aggregate daily calendar records to listing-level availability metrics.
    """

    calendar_summary = (
        calendar
        .groupby("listing_id")
        .agg(
            total_days=("date", "count"),
            available_days=("available", lambda x: (x == "t").sum()),
            unavailable_days=("available", lambda x: (x == "f").sum())
        )
        .reset_index()
    )

    calendar_summary["availability_rate"] = (
        calendar_summary["available_days"]
        / calendar_summary["total_days"]
    )

    calendar_summary["occupancy_rate"] = (
        calendar_summary["unavailable_days"]
        / calendar_summary["total_days"]
    )

    return calendar_summary