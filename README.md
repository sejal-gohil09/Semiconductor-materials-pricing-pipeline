# Semiconductor Materials Pricing & Market Intelligence Pipeline

A multi-source data processing, analytics, and market intelligence pipeline designed to ingest 5 distinct semiconductor market datasets, perform data quality validation, model pricing extrapolations, and build executive reporting deliverables.

## 📁 Repository Structure
```text
semiconductor-materials-pricing-pipeline/
├── data/
│   ├── raw/                 # Multi-source input files (5 distinct feeds)
│   └── processed/           # Consolidated & cleaned unified dataset
├── etl/
│   ├── extract_sources.py   # Ingestion engine handling multi-file loading (.xlsx / .csv)
│   ├── validation.py        # Schema alignment, bounds checking, Z-score outlier removal
│   └── Excel_builder.py     # Automated openpyxl Excel deliverable generation
├── models/
│   ├── extrapolation.py     # Linear regression forecasting on material trends
│   └── survey_analysis.py   # B2B foundry survey sentiment aggregation
├── reports/
│   └── Semiconductor_Materials_Market_Insights.xlsx # Automated multi-tab deliverable
├── README.md                # Detailed project architecture & overview
└── requirements.txt         # Dependencies
