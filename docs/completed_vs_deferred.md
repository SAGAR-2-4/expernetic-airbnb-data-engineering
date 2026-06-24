# Completed vs Deferred Work Summary

## Completed Work

### Data Familiarisation and Profiling

The project reviewed Airbnb listing, review, and calendar datasets for London and New York.

Completed activities include:

* Source-schema review
* Dataset relationship analysis
* Missing-value assessment
* Duplicate checks
* Price-distribution profiling
* Calendar-data assessment
* Cross-city data-comparison notes
* Data limitations and assumptions documentation

---

### Data Cleaning and Enrichment

The project implemented and documented:

* Conversion of raw source-price strings into numeric `price_clean`
* Date parsing for listing and review-related dates
* Price outlier flagging
* Host-tenure derivation where source data was available
* Listing-level review aggregation
* Calendar-level availability aggregation
* Calendar-unavailability proxy calculation
* Price-per-bedroom calculation where bedroom values were valid
* Neighbourhood-level enrichment metrics
* City-level dataset combination

---

### Dimensional Data Model

The project created an analytical data model containing:

* `dim_city`
* `dim_neighbourhood`
* `dim_listing`
* `fact_listing_performance`

The model supports listing-level analytical reporting through city, neighbourhood, listing type, review, price, and calendar-derived measures.

---

### SQL Analytics and Exploratory Analysis

The completed DuckDB SQL analysis includes:

* Listing supply by city
* Calendar-unavailability proxy by city
* Source-price patterns by room type
* Premium neighbourhoods ranked within each city
* Listings with high review counts
* London and New York price-distribution histograms
* London and New York room-type price boxplots

---

### Repeatable Data Pipeline

The project includes a modular local data-engineering pipeline with:

* Data ingestion
* Dataset validation
* Listing cleaning
* Review aggregation
* Calendar aggregation
* Master-dataset construction
* Multi-city pipeline orchestration

The combined pipeline output is saved as:

```text
data/processed/pipeline_master_dataset.csv
```

---

### Exploratory Machine Learning and Dashboard

The completed AI and dashboard components include:

* Exploratory KMeans listing segmentation
* Four interpretable segment labels
* Segment profiling
* Curated segmentation outputs
* Guided analytics questions
* Streamlit Market Overview
* Streamlit Guided Analytics
* Streamlit Segment Explorer
* Streamlit Pipeline Status tab

---

## Deferred Work

### Formal Statistical Testing

Formal hypothesis testing, confidence intervals, effect sizes, and advanced statistical validation were deferred.

The project prioritised completion of the end-to-end pipeline, analytics, segmentation, dashboard, documentation, and reproducibility requirements within the available assessment timeframe.

---

### Production Pipeline Operations

The following production-grade capabilities are deferred:

* Structured logging
* Retry mechanisms
* Incremental processing
* Metadata-driven orchestration
* Automated data-quality monitoring
* Scheduled execution
* Cloud storage and deployment
* CI/CD integration

The current solution establishes a modular local pipeline foundation that can be extended with these capabilities.

---

### Currency Normalisation

Historical exchange-rate normalisation was deferred.

London and New York prices remain in their local source currencies. Therefore, cross-city price values are descriptive only and are not treated as direct financial comparisons.

---

### Forecasting and Advanced Machine Learning

The following items are deferred:

* Demand forecasting
* Revenue forecasting
* Confirmed occupancy prediction
* Alternative clustering algorithms
* Automated cluster-stability testing
* Model monitoring

The available calendar data supports an availability and unavailability proxy, not verified bookings or revenue.

---

### New-City Upload Workflow

A prototype uploaded-city workflow was removed from the final dashboard.

The final dashboard focuses on reliable London and New York curated outputs. Future work can connect new-city ingestion to the existing modular pipeline through a validated configuration-driven workflow.

---

## Completion Statement

The final solution delivers a complete analytical workflow:

```text
Raw Airbnb Data
        ↓
Modular Data Pipeline
        ↓
Processed Master Dataset
        ↓
SQL Analytics and Exploratory Segmentation
        ↓
Curated Outputs
        ↓
Streamlit Market Intelligence Dashboard
```

Deferred work is documented transparently and is not represented as completed functionality.
