import os
import glob
import pandas as pd

def process_survey_data(raw_dir="data/raw"):
    survey_files = glob.glob(os.path.join(raw_dir, "*survey*.csv")) + glob.glob(os.path.join(raw_dir, "*survey*.xlsx"))
    
    if not survey_files:
        print("[SURVEY MODEL] No survey file found. Returning default placeholder.")
        return pd.DataFrame()
        
    f = survey_files[0]
    df = pd.read_excel(f) if f.endswith('.xlsx') else pd.read_csv(f)
    
    df["Weighted_Lead_Time_Score"] = df["Lead_Time_Constraint_Score"] * df["Survey_Weight"]
    df["Weighted_Volatility_Score"] = df["Price_Volatility_Impact"] * df["Survey_Weight"]
    
    summary = df.groupby("Region")[["Weighted_Lead_Time_Score", "Weighted_Volatility_Score"]].mean().reset_index()
    return summary
