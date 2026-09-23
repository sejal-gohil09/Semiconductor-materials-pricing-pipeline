# Semiconductor Materials Pricing & Market Intelligence Pipeline

A multi-source data processing, analytics, and market intelligence pipeline designed to ingest 5 distinct semiconductor market datasets, perform data quality validation, model pricing extrapolations, and build executive reporting deliverables.

## 📁 Repository Structure
```text
semiconductor-materials-pricing-pipeline/
├── data/
│   ├── raw/                 # Input datasets (.csv / .xlsx)
│   └── processed/           # Consolidated & cleaned dataset
├── etl/
│   ├── extract_sources.py   # Multi-source ingestion engine
│   ├── validation.py        # Schema alignment & outlier removal
│   └── Excel_builder.py     # Automated openpyxl Excel reporter
├── models/
│   ├── extrapolation.py     # Forecasting models
│   └── survey_analysis.py   # B2B sentiment analysis
├── reports/
│   └── Semiconductor_Materials_Market_Insights.xlsx
├── README.md                # Project documentation
└── requirements.txt         # Dependencies


**# Semiconductor Materials Pricing & Market Intelligence Pipeline**

An end-to-end multi-source data processing, ETL validation, and predictive analytics pipeline designed for semiconductor material pricing data.

## 📌 Project Overview
This project ingests multi-source data (raw feedstocks, specialty chemicals, foundry capacity, and B2B survey sentiment) to clean, normalize, forecast, and output structured executive market reports.

## 🛠️ Key Features
- **Multi-Source Ingestion**: Ingests `.csv` and `.xlsx` files with flexible column header mapping.
- **Data Hygiene & Cleaning**: Performs null checking, non-positive price filtering, and statistical outlier remediation using $Z$-score thresholding ($Z > 3.0$).
- **Predictive Extrapolation**: Applies linear regression modeling to generate 3-month forward price forecasts.
- **Automated Excel Reporting**: Generates formatted, multi-tab `.xlsx` executive summary workbooks dynamically.

## ⚙️ Tech Stack
- Languages: Python 3.x
- Libraries: `pandas`, `numpy`, `scipy`, `openpyxl`, `matplotlib`, `seaborn`

