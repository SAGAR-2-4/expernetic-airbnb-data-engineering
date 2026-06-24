# Airbnb Market Intelligence Platform

### Repeatable Data Pipeline, Exploratory Segmentation, and Guided Analytics Dashboard

## Project Overview

This project delivers an end-to-end Airbnb market intelligence solution using London and New York listing data.

The solution transforms raw Airbnb datasets into a cleaned and enriched master dataset, performs exploratory SQL analytics and KMeans-based listing segmentation, and presents the results through a Streamlit dashboard.

The project was developed as part of the Expernetic Data Engineer Talent Assessment Program.

---

## Business Objective

The project aims to support exploratory Airbnb market analysis by answering questions such as:

* How do listing supply and calendar availability patterns differ between London and New York?
* Which neighbourhoods have higher median source-price levels within each city?
* Which listing types show different price distributions?
* Which listings appear in high-demand, premium, established-popular, or low-performance segments?
* How can a repeatable pipeline support future city-level Airbnb data analysis?

---

## Key Deliverables

* Modular data ingestion and transformation (repeatable) pipeline
* Data profiling and cleaning workflow
* Enriched listing-level master dataset
* Dimensional data model with fact and dimension tables
* DuckDB SQL analytics
* Exploratory KMeans listing segmentation
* Guided Analytics Assistant
* Streamlit market intelligence dashboard
* Documentation, assumptions, limitations, and AI usage disclosure

---

## Solution Architecture

```text
Raw Airbnb Datasets
(Listings, Reviews, Calendar)
        │
        ▼
Modular Data Engineering Pipeline
        │
        ├── Ingestion
        ├── Validation
        ├── Cleaning
        ├── Review Aggregation
        ├── Calendar Aggregation
        └── Master Dataset Construction
        │
        ▼
Processed Master Dataset
        │
        ├── SQL Analytics
        ├── Exploratory EDA
        ├── KMeans Segmentation
        └── Curated Segment Outputs
        │
        ▼
Streamlit Market Intelligence Dashboard
```

---

## Data Sources

The project uses Airbnb datasets for two cities:

| City     | Listings |Listings with Review History |                                         Calendar |
| -------- | -------: | --------------------------: | ------------------------------------------------: |
| London   |   96,871 |              72,749 | 35M+ calendar records[ 35,357,974 daily calendar records] |
| New York |   35,036 |             24,542  | 12M+ calendar records[ 35,357,974 daily calendar records] |

The final combined master dataset contains:

```text
Combined: 131,907 listings
```
The review and calendar datasets are one-to-many relative to listings. Both were aggregated to listing level before enrichment to prevent row duplication in the final master dataset.
---

## Project Structure

```text
expernetic-airbnb-data-engineering/
│
├── data/
│   ├── raw/
│   │   ├── london/
│   │   └── new_york/
│   │
│   ├── processed/
│   │   └── pipeline_master_dataset.csv
│   │
│   └── curated/
│       ├── ai_segmented_listings.csv
│       ├── ai_segment_profile.csv
│       ├── dim_city.csv
│       ├── dim_listing.csv
│       ├── dim_neighbourhood.csv
│       └── fact_listing_performance.csv
│
├── docs/
│   ├── figures/
│   └── star_schema.svg
│
├── notebooks/
│   ├── 01_dataset_familiarization.ipynb
│   ├── 02_data_profiling.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_data_enrichment.ipynb
│   ├── 05_data_modeling.ipynb
│   ├── 06_sql_analytics.ipynb
│   ├── 07_pipeline_design.ipynb
│   └── 08_ai_analyst_assistant.ipynb
│
├── src/
│   ├── ingestion/
│   │   └── load_data.py
│   │
│   ├── profiling/
│   │   └── validate_data.py
│   │
│   ├── cleaning/
│   │   └── clean_listings.py
│   │
│   ├── transformation/
│   │   ├── review_aggregation.py
│   │   ├── calendar_aggregation.py
│   │   └── build_master.py
│   │
│   └── pipeline.py
│
├── app.py
├── README.md
└── requirements.txt
```

---

## Data Engineering Pipeline

The project uses a modular repeatable data pipeline rather than keeping all transformation logic inside notebooks or the Streamlit application.

| Stage                | Module                                       |   Purpose                                     |---------------
| -------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------- |
| Ingestion            | `src/ingestion/load_data.py`                 | Loads listings, reviews, and calendar datasets for each city                        |
| Validation           | `src/profiling/validate_data.py`             | Validates required datasets, key columns, and non-empty inputs                      |
| Cleaning             | `src/cleaning/clean_listings.py`             | Cleans prices, parses dates, flags outliers, and derives host tenure where possible |
| Review Aggregation   | `src/transformation/review_aggregation.py`   | Creates listing-level review counts and review-date summaries                       |
| Calendar Aggregation | `src/transformation/calendar_aggregation.py` | Derives availability and calendar-unavailability proxy metrics                      |
| Master Dataset       | `src/transformation/build_master.py`         | Joins listings, reviews, calendar metrics, and city identifiers                     |
| Orchestration        | `src/pipeline.py`                            | Runs the workflow for both cities and writes processed outputs                      |

The main processed output is:

```text
data/processed/pipeline_master_dataset.csv
```

---

## Data Cleaning and Enrichment

Key cleaning and enrichment activities include:

* Conversion of source price strings into numeric `price_clean`
* Date parsing for listing and review-related dates
* Price-outlier flagging using percentile-based thresholds
* Host-tenure calculation where source data supports it
* Listing-level review count aggregation
* Calendar availability and unavailable-day aggregation
* Derivation of `availability_rate`
* Derivation of `occupancy_rate` as an occupancy/unavailability proxy
* Price-per-bedroom calculation where bedroom data is valid
* Neighbourhood-level enrichment metrics
* Cross-city master dataset construction

---

## Dimensional Data Model

The project includes a dimensional model designed for analytical reporting.

### Dimension Tables

* `dim_city`
* `dim_neighbourhood`
* `dim_listing`

### Fact Table

* `fact_listing_performance`

The fact table contains listing-level measures such as:

* `price_clean`
* `availability_rate`
* `occupancy_rate`
* `total_reviews`
* `review_frequency`
* `price_per_bedroom`
* `host_tenure_years`

---

## SQL Analytics

DuckDB is used to perform analytical queries on the curated model.

Key analyses include:

* Listing counts by city
* Average source prices by city
* Average calendar-unavailability proxy by city
* Premium neighbourhoods within each city
* Room-type price distributions
* Highly reviewed listings
* Cross-city supply and availability comparisons

Important note: source price values are not currency-normalized between London and New York. Therefore, price comparisons across cities are descriptive only and should not be interpreted as direct financial comparisons.

---

## Exploratory Machine Learning Segmentation

KMeans clustering is used to create exploratory listing segments.

The final segmentation produces four business-oriented segments:

| Segment             | Interpretation                                                                           |
| ------------------- | ---------------------------------------------------------------------------------------- |
| High Demand         | Listings with relatively high calendar-unavailability proxy                              |
| Established Popular | Listings with substantial historical review activity                                     |
| Premium Luxury      | Listings with high source-price characteristics                                          |
| Low Performance     | Listings with low calendar-unavailability proxy and potential optimisation opportunities |

The final segmentation outputs are saved in:

```text
data/curated/ai_segmented_listings.csv
data/curated/ai_segment_profile.csv
```

---

## Streamlit Dashboard

The Streamlit dashboard is launched from:

```text
app.py
```

The dashboard includes:

* Market Overview
* Guided Analytics Assistant
* Segment Explorer
* Pipeline Status

The dashboard consumes processed and curated outputs generated by the pipeline. It does not rerun the complete raw-data pipeline interactively because the calendar datasets contain tens of millions of records.

---

## Running the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd expernetic-airbnb-data-engineering
```

### 2. Create and Activate a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the Pipeline

Run the pipeline workflow through:

```powershell
python -m src.pipeline
```

The pipeline generates the processed master dataset.

### 5. Run the Streamlit Dashboard

```powershell
streamlit run app.py
```

The application opens locally at:

```text
http://localhost:8501
```

---

## Technology Stack

| Area                 | Technologies                         |
| -------------------- | ------------------------------------ |
| Programming Language | Python                               |
| Data Processing      | Pandas, NumPy                        |
| Data Modelling       | Pandas, CSV-based dimensional tables |
| SQL Analytics        | DuckDB                               |
| Machine Learning     | Scikit-learn KMeans                  |
| Dashboard            | Streamlit                            |
| Visualisation        | Matplotlib, Streamlit charts         |
| Version Control      | Git and GitHub                       |

---

## Important Assumptions and Limitations

* `occupancy_rate` is an occupancy/unavailability proxy derived from calendar records. It does not represent confirmed bookings.
* Calendar dates marked unavailable may represent booked dates, host-blocked dates, maintenance periods, or other restrictions.
* London and New York source prices are not currency-normalized.
* Raw source-price comparisons across cities should not be interpreted as direct affordability or profitability comparisons.
* Missing review values can indicate listings with no review history rather than invalid records.
* New York host-tenure analysis is limited because `host_since` values are unavailable in the source dataset.
* KMeans segments are exploratory analytical groups, not ground-truth classifications.
* The segmentation is not a profitability prediction, booking forecast, or investment recommendation engine.

---

## Future Enhancements

* Currency normalization using historical exchange rates
* Structured pipeline logging and retry mechanisms
* Incremental pipeline execution
* Data quality monitoring dashboard
* Formal statistical hypothesis testing
* More advanced clustering validation
* Forecasting of availability or demand proxy metrics
* Cloud storage and scheduled orchestration
* Additional city ingestion through validated pipeline configuration

---

## AI Usage Disclosure

AI tools were used as a development support mechanism for:

* Code review and debugging support
* Documentation drafting
* Markdown structure generation
* Explanation of analytical approaches
* Drafting report and README content

All code, outputs, assumptions, interpretations, and final submission materials were reviewed and validated by the project author.
