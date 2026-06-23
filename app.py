import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



st.set_page_config(
    page_title="Airbnb AI Analyst Assistant",
    layout="wide"
)


@st.cache_data
def load_default_data():
    master = pd.read_csv("data/processed/pipeline_master_dataset.csv")
    segments = pd.read_csv("data/curated/ai_segmented_listings.csv")
    profile = pd.read_csv("data/curated/ai_segment_profile.csv")

    return master, segments, profile


def clean_price_column(df):
    df["price_clean"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("nan", pd.NA)
    )

    df["price_clean"] = pd.to_numeric(
        df["price_clean"],
        errors="coerce"
    )

    return df

 


def process_uploaded_city(listings, reviews, calendar, city_name):
    listings = listings.copy()
    reviews = reviews.copy()
    calendar = calendar.copy()

    listings = clean_price_column(listings)

    date_cols = [
        "last_scraped",
        "host_since",
        "calendar_last_scraped",
        "first_review",
        "last_review",
    ]

    for col in date_cols:
        if col in listings.columns:
            listings[col] = pd.to_datetime(listings[col], errors="coerce")

    if "last_scraped" in listings.columns and "host_since" in listings.columns:
        listings["host_tenure_years"] = (
            (listings["last_scraped"] - listings["host_since"]).dt.days / 365
        )

    review_summary = (
        reviews.groupby("listing_id")
        .agg(
            total_reviews=("id", "count"),
            first_review_date=("date", "min"),
            last_review_date=("date", "max"),
        )
        .reset_index()
    )

    calendar_summary = (
        calendar.groupby("listing_id")
        .agg(
            total_days=("date", "count"),
            available_days=("available", lambda x: (x == "t").sum()),
            unavailable_days=("available", lambda x: (x == "f").sum()),
        )
        .reset_index()
    )

    calendar_summary["availability_rate"] = (
        calendar_summary["available_days"] / calendar_summary["total_days"]
    )

    calendar_summary["occupancy_rate"] = (
        calendar_summary["unavailable_days"] / calendar_summary["total_days"]
    )

    master = (
        listings.merge(
            review_summary,
            left_on="id",
            right_on="listing_id",
            how="left",
        )
        .merge(
            calendar_summary,
            left_on="id",
            right_on="listing_id",
            how="left",
        )
    )

    drop_cols = [
        col for col in ["listing_id_x", "listing_id_y"]
        if col in master.columns
    ]

    master = master.drop(columns=drop_cols)
    master["city"] = city_name

    return master


def generate_ai_segments(master_df):
    features = [
        "occupancy_rate",
        "availability_rate",
        "total_reviews",
        "price_clean",
    ]

    segment_df = master_df[
        [
            "id",
            "city",
            "room_type",
            "property_type",
            "neighbourhood_cleansed",
        ] + features
    ].copy()

    segment_df = segment_df.dropna(subset=features)

    if len(segment_df) < 20:
        return None, None

    price_cap = segment_df["price_clean"].quantile(0.999)

    segment_df = segment_df[
        segment_df["price_clean"] <= price_cap
    ].copy()

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        segment_df[features]
    )

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10,
    )

    segment_df["cluster"] = model.fit_predict(scaled_features)

    cluster_summary = (
        segment_df.groupby("cluster")[features]
        .mean()
        .round(2)
    )

    high_demand_cluster = cluster_summary["occupancy_rate"].idxmax()
    luxury_cluster = cluster_summary["price_clean"].idxmax()
    popular_cluster = cluster_summary["total_reviews"].idxmax()
    low_performance_cluster = cluster_summary["occupancy_rate"].idxmin()

    segment_mapping = {}

    segment_mapping[high_demand_cluster] = "High Demand"
    segment_mapping[luxury_cluster] = "Premium Luxury"
    segment_mapping[popular_cluster] = "Established Popular"
    segment_mapping[low_performance_cluster] = "Low Performance"

    for cluster in cluster_summary.index:
        if cluster not in segment_mapping:
            segment_mapping[cluster] = "General Market"

    segment_df["segment"] = segment_df["cluster"].map(segment_mapping)

    segment_profile = (
        segment_df.groupby("segment")
        .agg(
            occupancy_rate=("occupancy_rate", "mean"),
            total_reviews=("total_reviews", "mean"),
            price_clean=("price_clean", "mean"),
            listing_count=("id", "count"),
        )
        .round(2)
        .reset_index()
    )

    return segment_df, segment_profile


segment_insights = {
    "High Demand":
        "Strong booking activity and consistent demand. Suitable for revenue-focused investment strategies.",

    "Established Popular":
        "Large review history indicates proven market acceptance and customer trust.",

    "Premium Luxury":
        "High-value listings targeting premium travelers and luxury experiences.",

    "Low Performance":
        "Potential opportunities for pricing optimization, marketing improvements, or listing enhancements.",

    "General Market":
        "Balanced segment that does not strongly dominate on demand, pricing, or review history.",
}


def show_segment(profile_df, segmented_df, segment_name):
    segment_row = profile_df[
        profile_df["segment"] == segment_name
    ].iloc[0]

    st.subheader(f"AI Segment: {segment_name}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Listings", f"{int(segment_row['listing_count']):,}")
    c2.metric("Avg Occupancy", f"{segment_row['occupancy_rate']:.2f}")
    c3.metric("Avg Reviews", f"{segment_row['total_reviews']:.2f}")
    c4.metric("Avg Price", f"£{segment_row['price_clean']:.2f}")

    st.success(segment_insights.get(segment_name, "AI-generated segment."))

    segment_data = segmented_df[
        segmented_df["segment"] == segment_name
    ]

    st.dataframe(
        segment_data[
            [
                "city",
                "neighbourhood_cleansed",
                "room_type",
                "property_type",
                "price_clean",
                "occupancy_rate",
                "total_reviews",
            ]
        ].head(20),
        use_container_width=True,
    )


st.title("🏠 Airbnb AI Analyst Assistant")

st.markdown(
    """
    Interactive Airbnb market intelligence tool combining:
    **repeatable data pipeline + AI segmentation + business analytics dashboard**.
    """
)


tab1, tab2 = st.tabs(
    [
        "Default Market Dashboard",
        "Upload New City Dataset",
    ]
)


with tab1:
    master_df, segmented_df, profile_df = load_default_data()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Listings", f"{len(master_df):,}")
    col2.metric("Cities", master_df["city"].nunique())
    col3.metric("Average Price", f"£{master_df['price_clean'].mean():.2f}")
    col4.metric("AI Segments", profile_df["segment"].nunique())

    st.header("Ask a Market Question")

    question = st.selectbox(
        "Choose a business question",
        [
            "Which city has highest occupancy?",
            "Which city has highest average price?",
            "Top expensive neighbourhoods",
            "Best investment opportunities",
            "Show luxury market",
            "Show established performers",
            "Show underperforming listings",
        ],
    )

    if question == "Which city has highest occupancy?":
        result = (
            master_df.groupby("city")["occupancy_rate"]
            .mean()
            .reset_index()
            .sort_values("occupancy_rate", ascending=False)
        )

        st.dataframe(result, use_container_width=True)

        top_city = result.iloc[0]["city"]
        top_occ = result.iloc[0]["occupancy_rate"]

        st.success(
            f"{top_city} has the highest average occupancy rate at {top_occ:.2f}."
        )

    elif question == "Which city has highest average price?":
        result = (
            master_df.groupby("city")["price_clean"]
            .mean()
            .reset_index()
            .sort_values("price_clean", ascending=False)
        )

        st.dataframe(result, use_container_width=True)

        top_city = result.iloc[0]["city"]
        top_price = result.iloc[0]["price_clean"]

        st.success(
            f"{top_city} has the highest average listing price at £{top_price:.2f}."
        )

    elif question == "Top expensive neighbourhoods":
        result = (
            master_df.groupby(["city", "neighbourhood_cleansed"])["price_clean"]
            .median()
            .reset_index()
            .rename(columns={"price_clean": "median_price"})
            .sort_values("median_price", ascending=False)
            .head(10)
        )

        st.dataframe(result, use_container_width=True)

        st.success(
            "These neighbourhoods represent the highest-priced market areas based on median listing price."
        )

    elif question == "Best investment opportunities":
        show_segment(profile_df, segmented_df, "High Demand")

    elif question == "Show luxury market":
        show_segment(profile_df, segmented_df, "Premium Luxury")

    elif question == "Show established performers":
        show_segment(profile_df, segmented_df, "Established Popular")

    elif question == "Show underperforming listings":
        show_segment(profile_df, segmented_df, "Low Performance")

    st.header("Explore AI Segments")

    selected_segment = st.selectbox(
        "Select a segment to inspect",
        profile_df["segment"].sort_values().unique(),
    )

    show_segment(profile_df, segmented_df, selected_segment)


with tab2:
    st.header("Upload New City Dataset")

    city_name = st.text_input(
        "City Name",
        value="Paris",
    )

    listings_file = st.file_uploader(
        "Upload listings.csv.gz",
        type=["gz"],
    )

    reviews_file = st.file_uploader(
        "Upload reviews.csv.gz",
        type=["gz"],
    )

    calendar_file = st.file_uploader(
        "Upload calendar.csv.gz",
        type=["gz"],
    )

    if st.button("Run Uploaded City Pipeline"):
        if listings_file and reviews_file and calendar_file:
            listings = pd.read_csv(listings_file, compression="gzip")
            reviews = pd.read_csv(reviews_file, compression="gzip")
            calendar = pd.read_csv(calendar_file, compression="gzip")

            uploaded_master = process_uploaded_city(
                listings,
                reviews,
                calendar,
                city_name,
            )

            uploaded_segments, uploaded_profile = generate_ai_segments(
                uploaded_master
            )

            st.success("Uploaded city pipeline completed successfully.")

            st.metric("Processed Listings", f"{len(uploaded_master):,}")

            if uploaded_segments is not None:
                st.subheader("Generated AI Segment Profile")
                st.dataframe(uploaded_profile, use_container_width=True)

                selected_uploaded_segment = st.selectbox(
                    "Inspect uploaded city segment",
                    uploaded_profile["segment"].sort_values().unique(),
                )

                show_segment(
                    uploaded_profile,
                    uploaded_segments,
                    selected_uploaded_segment,
                )

            else:
                st.warning(
                    "Not enough valid records to generate AI segments."
                )

        else:
            st.error(
                "Please upload listings, reviews, and calendar files."
            )