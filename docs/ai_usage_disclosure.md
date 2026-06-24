# AI Usage Disclosure

## Project: Airbnb Market Intelligence Platform

AI tools were used as development-support tools during this project. The project author remained responsible for all final technical decisions, code execution, output validation, documentation, and submission content.

---

## 1. AI Tools Used

| Tool                | Model / Version                       | Primary Use                                                                                                             |
| ------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| ChatGPT             | GPT-5.5 Thinking                      | Technical mentoring, code review, debugging support, documentation drafting, report structure, and analytical reasoning |
| VS Code Local Agent | Model version not separately recorded | Local coding support, file-level implementation assistance, and development workflow support                            |
| Claude              | Claude Sonnet 4.6                     | Supporting code explanation, technical review, and development guidance                                                 |

---

## 2. AI-Assisted Sections

AI support was used in the following areas:

* Reviewing the assessment brief and converting requirements into a delivery plan.
* Structuring the modular pipeline for ingestion, validation, cleaning, review aggregation, calendar aggregation, and master-dataset construction.
* Debugging Pandas, DuckDB, Streamlit, and Scikit-learn code.
* Drafting notebook Markdown explanations and technical documentation.
* Reviewing data-quality assumptions, including missing values, outlier treatment, source-currency differences, and calendar-unavailability limitations.
* Drafting the README, decision log, completed-versus-deferred summary, AI disclosure, and report content.
* Supporting statistical-test selection and interpretation.
* Improving dashboard wording so it accurately describes exploratory segments and occupancy/unavailability proxy measures.

---

## 3. Representative Prompts Used

### Prompt A — Technical Mentoring and Review

> You are my Senior Data Engineering Mentor and Technical Reviewer for the Expernetic Data Engineer Intern Assignment. My objective is not merely to finish the assignment, but to produce a technically sound, well-documented, reproducible data-engineering solution that stands out. Review my implementation against the assignment requirements, identify risks, and provide practical next steps.

### Prompt B — Requirement Alignment

> Review the assessment brief carefully and map every required deliverable to the project implementation. Identify completed, partially completed, missing, and deferred items. Do not invent completed work.

### Prompt C — Data-Quality and Assumption Review

> Review the dataset profiling and cleaning approach. Identify assumptions, missing-data risks, invalid comparisons, outlier-handling issues, and limitations that must be documented in the report and dashboard.

### Prompt D — Code and Architecture Review

> Review the pipeline and dashboard as a senior data engineer. Ensure the pipeline logic is modular, repeatable, and separate from Streamlit presentation logic. Flag duplicated transformation logic, fragile assumptions, and reproducibility risks.

### Prompt E — Report Quality Control

> Create a professional assessment report using only verified project outputs. Include limitations, deferred work, evidence for technical decisions, and plain-English business interpretation for every analytical result. Do not make unsupported claims.

---

## 4. Output Validation

AI-generated suggestions were not accepted automatically.

The following validation activities were performed:

* Notebooks were executed locally and outputs were inspected.
* Pipeline outputs were checked for expected shapes, columns, and saved files.
* The combined processed master dataset was confirmed to contain 131,907 listings.
* SQL outputs were reviewed in DuckDB.
* Price-distribution charts and room-type boxplots were visually checked.
* Streamlit dashboard tabs were tested locally.
* Source-price comparisons were restricted to within-city interpretation because London and New York source currencies were not normalized.
* Calendar unavailability was described as an occupancy proxy rather than confirmed bookings.
* The Mann–Whitney U test was run locally and its output was saved as a curated CSV.
* KMeans results were reviewed using silhouette scores, cluster profiles, and business interpretability.

---

## 5. Meaningful Modifications Made to AI-Assisted Work

The following changes were made after review:

* Dashboard wording was changed from investment-oriented claims to exploratory market-analysis language.
* Cross-city raw-price ranking was removed because prices were not currency-normalized.
* Calendar metrics were renamed and documented as occupancy/unavailability proxies.
* The unstable uploaded-city Streamlit prototype was removed from the final dashboard.
* A Pipeline Status tab was added to demonstrate that Streamlit consumes modular pipeline outputs rather than duplicating the data-engineering workflow.
* Statistical testing was added using a Mann–Whitney U test to strengthen the Statistical Thinking component.
* Documentation was revised to separate completed features from deferred production capabilities.

---

## 6. Critical Assessment and Rejected Suggestions

AI suggestions were critically reviewed and not always accepted.

A late suggestion to replace the original KMeans feature set with an alternative city-normalized clustering setup was tested. The revised setup produced a lower silhouette score of approximately 0.313 compared with the original refined clustering result of approximately 0.505.

Because the alternative approach would have weakened cluster separation and destabilised the final dashboard and documentation near submission, it was rejected and reverted.

The original KMeans approach was retained and documented as an exploratory segmentation prototype with clear limitations.

---

## 7. Author Responsibility Statement

AI assistance accelerated development, explanation, review, and documentation. It was not used as a substitute for executing code, inspecting outputs, validating assumptions, or making final technical decisions.

All final submitted code, analysis, visualisations, documentation, and conclusions were reviewed and approved by the project author.
