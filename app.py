"""
Airbnb Market Intelligence Dashboard

This Streamlit application presents curated outputs from the Airbnb
data-engineering pipeline, exploratory KMeans listing segmentation,
and guided business analytics for London and New York.

Important interpretation notes:
- Prices are shown in local source currencies and are not currency-normalized.
- Occupancy rate is an occupancy/unavailability proxy derived from calendar data.
- Segments are exploratory analytical groups, not investment recommendations.
"""

import pandas as pd
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Airbnb Market Intelligence Dashboard",
    page_icon="🏠",
    layout="wide",
)


@st.cache_data
def load_curated_data():
    """Load pipeline and segmentation outputs created by the project."""

    master = pd.read_csv(
        "data/processed/pipeline_master_dataset.csv",
        low_memory=False,
    )

    segments = pd.read_csv(
        "data/curated/ai_segmented_listings.csv",
        low_memory=False,
    )

    profile = pd.read_csv(
        "data/curated/ai_segment_profile.csv",
        low_memory=False,
    )

    return master, segments, profile


def get_premium_neighbourhoods(master_df):
    """
    Return the top five premium neighbourhoods within each city.

    Raw source prices are not compared across cities because London and
    New York use different source currencies.
    """

    neighbourhoods = (
        master_df
        .dropna(subset=["neighbourhood_cleansed", "price_clean"])
        .groupby(
            ["city", "neighbourhood_cleansed"],
            as_index=False,
        )
        .agg(
            median_source_price=("price_clean", "median"),
            listing_count=("id", "count"),
        )
    )

    neighbourhoods = neighbourhoods[
        neighbourhoods["listing_count"] >= 50
    ].copy()

    neighbourhoods["price_rank"] = (
        neighbourhoods
        .groupby("city")["median_source_price"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    return (
        neighbourhoods[
            neighbourhoods["price_rank"] <= 5
        ]
        .sort_values(["city", "price_rank"])
        .reset_index(drop=True)
    )


segment_insights = {
    "High Demand": (
        "This segment has the highest average calendar unavailability proxy. "
        "It may represent listings with consistently limited availability, "
        "but unavailable dates can include bookings, host-blocked dates, "
        "or other restrictions."
    ),
    "Established Popular": (
        "This segment has substantial historical review activity, suggesting "
        "longer-term guest engagement and established market presence."
    ),
    "Premium Luxury": (
        "This segment has a high source-price profile. It should be interpreted "
        "as an exploratory premium segment because London and New York prices "
        "are not currency-normalized."
    ),
    "Low Performance": (
        "This segment has the lowest calendar unavailability proxy. It may "
        "represent opportunities to review price positioning, listing quality, "
        "marketing visibility, or availability-management practices."
    ),
    "General Market": (
        "This segment represents listings with balanced characteristics that "
        "do not strongly dominate on demand proxy, review history, or price profile."
    ),
}


def show_segment(profile_df, segmented_df, segment_name):
    """Display one selected exploratory listing segment."""

    segment_row = profile_df[
        profile_df["segment"] == segment_name
    ]

    if segment_row.empty:
        st.warning(
            f"No profile information is available for '{segment_name}'."
        )
        return

    segment_row = segment_row.iloc[0]

    st.subheader(f"Segment Explorer: {segment_name}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Listings",
        f"{int(segment_row['listing_count']):,}",
    )

    col2.metric(
        "Avg Unavailability Proxy",
        f"{segment_row['occupancy_rate']:.2f}",
    )

    col3.metric(
        "Avg Reviews",
        f"{segment_row['total_reviews']:.1f}",
    )

    col4.metric(
        "Avg Source Price",
        f"{segment_row['price_clean']:.2f}",
    )

    st.info(
        segment_insights.get(
            segment_name,
            "Exploratory listing segment based on clustering outputs.",
        )
    )

    st.caption(
        "Caveat: Occupancy rate is an occupancy/unavailability proxy, "
        "not confirmed booking occupancy. Source-price values are not "
        "currency-normalized across cities."
    )

    segment_data = segmented_df[
        segmented_df["segment"] == segment_name
    ].copy()

    display_columns = [
        "city",
        "neighbourhood_cleansed",
        "room_type",
        "property_type",
        "price_clean",
        "occupancy_rate",
        "total_reviews",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in segment_data.columns
    ]

    st.dataframe(
        segment_data[available_columns].head(20),
        use_container_width=True,
        hide_index=True,
    )


# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

master_df, segmented_df, profile_df = load_curated_data()

st.title("🏠 Airbnb Market Intelligence Dashboard")

st.caption(
    "Curated data pipeline • Exploratory KMeans segmentation • "
    "Guided business analytics for London and New York"
)

st.info(
    "Interpretation note: Prices are shown in local source currencies and "
    "must not be treated as directly comparable across London and New York. "
    "Calendar unavailability is used as an occupancy proxy, not confirmed bookings."
)

overview_tab, analytics_tab, segments_tab, pipeline_tab = st.tabs(
    [
        "Market Overview",
        "Guided Analytics",
        "Segment Explorer",
        "Pipeline Status",
    ]
)


# -------------------------------------------------------------------
# Market Overview
# -------------------------------------------------------------------

with overview_tab:
    st.subheader("Market Overview")

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Total Listings",
        f"{len(master_df):,}",
    )

    metric_2.metric(
        "Cities Analysed",
        master_df["city"].nunique(),
    )

    metric_3.metric(
        "Exploratory Segments",
        profile_df["segment"].nunique(),
    )

    metric_4.metric(
        "Segmented Listings",
        f"{len(segmented_df):,}",
    )

    city_overview = (
        master_df
        .groupby("city", as_index=False)
        .agg(
            listing_count=("id", "count"),
            avg_unavailability_proxy=("occupancy_rate", "mean"),
            avg_availability_rate=("availability_rate", "mean"),
            avg_source_price=("price_clean", "mean"),
        )
        .round(3)
    )

    st.subheader("City-Level Supply and Availability Overview")

    st.dataframe(
        city_overview,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Average source prices are descriptive values only and are not "
        "currency-normalized across cities."
    )

    st.subheader("Average Calendar Unavailability Proxy by City")

    st.bar_chart(
        city_overview.set_index("city")[
            "avg_unavailability_proxy"
        ]
    )

    st.caption(
        "A higher value means listings were marked unavailable on a larger "
        "share of observed calendar days. This may reflect bookings, host-blocked "
        "dates, or other restrictions."
    )


# -------------------------------------------------------------------
# Guided Analytics
# -------------------------------------------------------------------

with analytics_tab:
    st.subheader("Guided Analytics Assistant")

    st.write(
        "Select a validated business question. The dashboard returns "
        "results calculated from curated project outputs."
    )

    question = st.selectbox(
        "Choose a business question",
        [
            "Which city has the highest occupancy/unavailability proxy?",
            "Show premium neighbourhoods within each city",
            "Show high-demand listing segment",
            "Show premium-luxury listing segment",
            "Show established-popular listing segment",
            "Show low-performance listing opportunities",
        ],
    )

    if question == "Which city has the highest occupancy/unavailability proxy?":
        result = (
            master_df
            .groupby("city", as_index=False)["occupancy_rate"]
            .mean()
            .sort_values("occupancy_rate", ascending=False)
            .round(3)
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
        )

        top_city = result.iloc[0]["city"]
        top_proxy = result.iloc[0]["occupancy_rate"]

        st.success(
            f"{top_city} has the highest average calendar "
            f"unavailability proxy at {top_proxy:.3f}."
        )

        st.caption(
            "This is not confirmed booking occupancy. Unavailable dates "
            "may include bookings, host blocks, or other restrictions."
        )

    elif question == "Show premium neighbourhoods within each city":
        premium_neighbourhoods = get_premium_neighbourhoods(
            master_df
        )

        st.dataframe(
            premium_neighbourhoods,
            use_container_width=True,
            hide_index=True,
        )

        st.success(
            "The table identifies the five highest median-price "
            "neighbourhoods within each city, using neighbourhoods "
            "with at least 50 listings."
        )

        st.caption(
            "Prices are ranked within each city only. London and New York "
            "source currencies are not normalized for cross-city comparison."
        )

    elif question == "Show high-demand listing segment":
        show_segment(
            profile_df,
            segmented_df,
            "High Demand",
        )

    elif question == "Show premium-luxury listing segment":
        show_segment(
            profile_df,
            segmented_df,
            "Premium Luxury",
        )

    elif question == "Show established-popular listing segment":
        show_segment(
            profile_df,
            segmented_df,
            "Established Popular",
        )

    elif question == "Show low-performance listing opportunities":
        show_segment(
            profile_df,
            segmented_df,
            "Low Performance",
        )


# -------------------------------------------------------------------
# Segment Explorer
# -------------------------------------------------------------------

with segments_tab:
    st.subheader("Explore Listing Segments")

    st.write(
        "Select a segment to inspect its profile and a sample of "
        "listings assigned to that exploratory group."
    )

    selected_segment = st.selectbox(
        "Select a segment",
        sorted(profile_df["segment"].dropna().unique()),
    )

    show_segment(
        profile_df,
        segmented_df,
        selected_segment,
    )

    st.divider()

    st.subheader("Segment Profile Table")

    st.dataframe(
        profile_df.sort_values("segment"),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Segment labels are business interpretations applied after KMeans "
        "clustering. They are not ground-truth classes or investment recommendations."
    )
    # -------------------------------------------------------------------
# Pipeline Status
# -------------------------------------------------------------------

with pipeline_tab:
    st.subheader("Repeatable Data Pipeline")

    st.write(
        "The dashboard reads outputs generated by the project's modular "
        "data-engineering pipeline. Core transformation logic is maintained "
        "in the `src/` directory rather than duplicated inside the user interface."
    )

    pipeline_stages = pd.DataFrame(
        [
            {
                "Stage": "1. Ingestion",
                "Module": "src/ingestion/load_data.py",
                "Purpose": "Loads city-level listings, reviews, and calendar datasets.",
            },
            {
                "Stage": "2. Validation",
                "Module": "src/profiling/validate_data.py",
                "Purpose": "Checks required datasets, core identifiers, and non-empty inputs.",
            },
            {
                "Stage": "3. Cleaning",
                "Module": "src/cleaning/clean_listings.py",
                "Purpose": "Cleans price fields, parses dates, flags price outliers, and derives host tenure.",
            },
            {
                "Stage": "4. Review Aggregation",
                "Module": "src/transformation/review_aggregation.py",
                "Purpose": "Creates listing-level review counts and review-date summaries.",
            },
            {
                "Stage": "5. Calendar Aggregation",
                "Module": "src/transformation/calendar_aggregation.py",
                "Purpose": "Creates availability and calendar-unavailability proxy metrics.",
            },
            {
                "Stage": "6. Master Dataset",
                "Module": "src/transformation/build_master.py",
                "Purpose": "Joins cleaned listings, review summaries, calendar summaries, and city labels.",
            },
            {
                "Stage": "7. Pipeline Orchestration",
                "Module": "src/pipeline.py",
                "Purpose": "Runs the workflow for London and New York and saves processed outputs.",
            },
        ]
    )

    st.dataframe(
        pipeline_stages,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Pipeline Output Status")

    output_files = {
    "Combined Processed Master Dataset":
        Path("data/processed/pipeline_master_dataset.csv"),
    "Curated AI Segmentation Output":
        Path("data/curated/ai_segmented_listings.csv"),
    "Curated Segment Profile":
        Path("data/curated/ai_segment_profile.csv"),
}

    output_status = []

    for output_name, output_path in output_files.items():
        output_status.append(
            {
                "Output": output_name,
                "Path": str(output_path),
                "Status": "Available" if output_path.exists() else "Missing",
            }
        )

    st.dataframe(
        pd.DataFrame(output_status),
        use_container_width=True,
        hide_index=True,
    )

    st.success(
    "The repeatable pipeline successfully generated the combined processed "
    "master dataset and curated AI segmentation outputs consumed by this dashboard. "
    "This keeps engineering logic modular, reproducible, and separate from "
    "presentation logic."
)

    st.caption(
        "The dashboard does not rerun the full pipeline interactively because "
        "the raw calendar datasets contain tens of millions of rows. Pipeline "
        "execution is performed through the modular source code and documented "
        "in Notebook 07."
    )