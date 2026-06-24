# Decision and Assumption Log

## Project: Airbnb Market Intelligence Platform

### D01 — London and New York as the Analysis Cities

**Decision:** Use Airbnb datasets from London and New York for cross-city analysis.

**Rationale:** Both cities provide listings, reviews, and calendar datasets suitable for pipeline development and comparative analytics.

**Impact:** Supports multi-city analysis and demonstrates that the pipeline can process more than one location.

---

### D02 — Combined Master Dataset

**Decision:** Create one combined master dataset with a `city` identifier.

**Rationale:** A unified dataset supports consistent SQL analytics, machine learning, and dashboard reporting while preserving each listing's original city.

**Impact:** Produces one processed dataset for downstream analysis and application use.

---

### D03 — Source Price Interpretation

**Decision:** Retain cleaned source prices as `price_clean` without directly ranking London against New York by price.

**Rationale:** The two source datasets use different currencies and no exchange-rate normalization was applied.

**Impact:** Cross-city price values are treated as descriptive only. Price-based neighbourhood analysis is performed within each city.

---

### D04 — Calendar Unavailability as a Proxy

**Decision:** Use calendar unavailability as an occupancy/unavailability proxy.

**Rationale:** Calendar data identifies whether a date is available or unavailable, but unavailable dates do not confirm that a booking occurred.

**Impact:** All dashboard and report references use the phrase **occupancy/unavailability proxy** rather than confirmed occupancy or bookings.

---

### D05 — Price Outlier Treatment

**Decision:** Flag price outliers in the processed dataset instead of deleting them.

**Rationale:** Keeping flagged records preserves data lineage and allows unusual listings to remain traceable.

**Impact:** Outliers remain accessible in the processed master dataset for inspection.

---

### D06 — Clustering-Specific Outlier Exclusion

**Decision:** Exclude listings above the 99.9th percentile of `price_clean` only from the KMeans clustering subset.

**Rationale:** A very small number of extreme prices can distort the distance calculations used by KMeans.

**Impact:** The original master dataset remains unchanged. Only the machine-learning subset is refined.

---

### D07 — KMeans for Exploratory Segmentation

**Decision:** Use KMeans clustering for listing segmentation.

**Rationale:** KMeans provides a reproducible and interpretable baseline for exploratory unsupervised analysis.

**Impact:** Listings are grouped according to selected availability, review, and price-related characteristics.

---

### D08 — Four Final Listing Segments

**Decision:** Use four final clusters for the exploratory segmentation.

**Rationale:** Four clusters provided the strongest practical balance between the original model evaluation results and business interpretability.

**Impact:** The final segment labels are:

* High Demand
* Established Popular
* Premium Luxury
* Low Performance

---

### D09 — DuckDB for SQL Analytics

**Decision:** Use DuckDB for analytical SQL queries.

**Rationale:** DuckDB supports fast local analysis of curated CSV outputs without requiring a separate database server.

**Impact:** SQL analytics can be reproduced through Notebook 06.

---

### D10 — Separation of Pipeline and Dashboard Logic

**Decision:** Keep core transformation logic inside the modular pipeline rather than duplicating it in Streamlit.

**Rationale:** The raw calendar datasets contain tens of millions of records and should not be repeatedly processed through a dashboard interface.

**Impact:** Streamlit reads processed and curated outputs, while the repeatable pipeline remains responsible for ingestion, validation, cleaning, aggregation, and master-dataset construction.

---

### D11 — Removal of Uploaded-City Dashboard Feature

**Decision:** Remove the uploaded-city prototype from the final Streamlit dashboard.

**Rationale:** The prototype duplicated pipeline logic in `app.py` and was less stable for the final demonstration.

**Impact:** The final dashboard focuses on reliable outputs for London and New York.

---

### D12 — Interpretation of Segment Labels

**Decision:** Treat segment labels as analyst-assigned business descriptions.

**Rationale:** KMeans produces numeric cluster identifiers rather than natural business categories.

**Impact:** Labels are presented as exploratory interpretations and not as ground-truth classes, booking predictions, profitability measures, or investment recommendations.
