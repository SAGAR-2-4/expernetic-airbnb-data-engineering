import pandas as pd


def clean_price_column(df, source_col="price", target_col="price_clean"):
    """
    Convert Airbnb price values from text to numeric.

    Example:
    "$149.00" -> 149.00
    "$1,200.00" -> 1200.00
    """

    df[target_col] = (
        df[source_col]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    return df


def clean_listings(df):
    """
    Clean and standardize listings data for any city.

    Steps:
    1. Clean price column
    2. Dynamically flag price outliers using the 99th percentile
    3. Convert available date columns to datetime
    4. Create host_tenure_years when possible
    """

    df = df.copy()

    # 1. Clean price
    df = clean_price_column(df)

    # 2. Dynamic outlier threshold
    price_threshold = df["price_clean"].quantile(0.99)

    df["price_outlier"] = (
        df["price_clean"] > price_threshold
    )

    # Store threshold for documentation/traceability
    df["price_outlier_threshold"] = price_threshold

    # 3. Convert date columns
    date_cols = [
        "last_scraped",
        "host_since",
        "calendar_last_scraped",
        "first_review",
        "last_review",
        "price_quote_checkin_date",
        "price_quote_checkout_date"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 4. Create host tenure
    if "last_scraped" in df.columns and "host_since" in df.columns:
        df["host_tenure_years"] = (
            (df["last_scraped"] - df["host_since"]).dt.days / 365
        )

    return df