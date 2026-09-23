import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime

def load_or_generate_5_datasets(raw_dir="data/raw"):
    os.makedirs(raw_dir, exist_ok=True)
    
    # Search for all Excel or CSV files inside data/raw/
    excel_files = glob.glob(os.path.join(raw_dir, "*.xlsx")) + glob.glob(os.path.join(raw_dir, "*.csv"))
    
    dataframes = {}
    
    if len(excel_files) >= 5:
        print(f"[INGESTION] Detected {len(excel_files)} data files in '{raw_dir}'. Loading files...")
        for file in excel_files:
            filename = os.path.basename(file)
            if file.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            dataframes[filename] = df
            print(f"  -> Successfully ingested: {filename} ({len(df)} rows)")
    else:
        print("[INGESTION] Less than 5 local files found. Automatically generating all 5 structured industry datasets...")
        dates = pd.date_range(start="2022-01-01", end="2026-01-01", freq='MS')
        np.random.seed(42)
        
        # File 1: Raw Material Feedstocks
        df1 = pd.DataFrame([{
            "Timestamp": d.strftime("%Y-%m-%d"),
            "Material_Name": "Electronic Grade Silicon",
            "Category": "Feedstock",
            "Price_USD": round(28.5 * (1 + np.random.normal(0.01, 0.03)), 2)
        } for d in dates])
        # Inject deliberate outlier anomaly
        df1.loc[5, "Price_USD"] = -10.0
        df1.loc[15, "Price_USD"] = 99999.0
        df1.to_csv(os.path.join(raw_dir, "1_raw_material_prices.csv"), index=False)
        dataframes["1_raw_material_prices.csv"] = df1

        # File 2: Chemical Precursors
        df2 = pd.DataFrame([{
            "Timestamp": d.strftime("%Y-%m-%d"),
            "Material_Name": "EUV Photoresist",
            "Category": "Chemical",
            "Price_USD": round(1850.0 * (1 + np.random.normal(0.01, 0.02)), 2)
        } for d in dates])
        df2.to_csv(os.path.join(raw_dir, "2_chemical_precursors.csv"), index=False)
        dataframes["2_chemical_precursors.csv"] = df2

        # File 3: Wafer Fabrication Costs
        df3 = pd.DataFrame([{
            "Timestamp": d.strftime("%Y-%m-%d"),
            "Material_Name": "Gallium Arsenide Wafers",
            "Category": "Finished Wafers",
            "Price_USD": round(320.0 * (1 + np.random.normal(0.01, 0.04)), 2)
        } for d in dates])
        df3.to_csv(os.path.join(raw_dir, "3_wafer_fab_costs.csv"), index=False)
        dataframes["3_wafer_fab_costs.csv"] = df3

        # File 4: Foundry Capacity & Lead Times
        df4 = pd.DataFrame([{
            "Timestamp": d.strftime("%Y-%m-%d"),
            "Foundry_Region": np.random.choice(["APAC", "AMER", "EMEA"]),
            "Capacity_Utilization_Pct": round(np.random.uniform(75.0, 98.0), 1),
            "Lead_Time_Weeks": np.random.randint(12, 36)
        } for d in dates])
        df4.to_csv(os.path.join(raw_dir, "4_foundry_capacity.csv"), index=False)
        dataframes["4_foundry_capacity.csv"] = df4

        # File 5: B2B Survey Sentiment
        surveys = [{
            "Respondent_ID": f"FOUNDRY_{100+i}",
            "Region": np.random.choice(["APAC", "AMER", "EMEA"]),
            "Lead_Time_Constraint_Score": np.random.randint(1, 6),
            "Price_Volatility_Impact": np.random.randint(1, 6),
            "Survey_Weight": round(np.random.uniform(0.8, 1.2), 2)
        } for i in range(100)]
        df5 = pd.DataFrame(surveys)
        df5.to_csv(os.path.join(raw_dir, "5_survey_sentiment.csv"), index=False)
        dataframes["5_survey_sentiment.csv"] = df5
        
        print("  -> Generated 5 separate datasets in 'data/raw/'.")
        
    return dataframes

if __name__ == "__main__":
    load_or_generate_5_datasets()
