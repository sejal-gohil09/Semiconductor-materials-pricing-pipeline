import os
import glob
import pandas as pd
import numpy as np
from scipy import stats

def validate_and_merge_datasets(raw_dir="data/raw", processed_dir="data/processed"):
    os.makedirs(processed_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(raw_dir, "*.csv")) + glob.glob(os.path.join(raw_dir, "*.xlsx")) + glob.glob(os.path.join(raw_dir, "*.xls"))
    
    pricing_dfs = []
    
    # Comprehensive alias mapping for real-world Kaggle/semiconductor datasets
    material_col_aliases = [
        "Material_Name", "Material", "Product", "Item", "Material Name", "Component", 
        "chip", "chip_name", "product_name", "company", "Company", "segment", "market_segment"
    ]
    price_col_aliases = [
        "Price_USD", "Price", "Cost", "Price (USD)", "Unit Price", "Rate", "price", 
        "avg_price", "ASP", "market_cap", "revenue", "value", "price_usd"
    ]
    date_col_aliases = [
        "Timestamp", "Date", "Year_Month", "Month", "Time", "year", "date", "year_month"
    ]

    for f in files:
        try:
            df = pd.read_excel(f) if (f.endswith('.xlsx') or f.endswith('.xls')) else pd.read_csv(f)
        except Exception as e:
            print(f"  [SKIP] Could not read {os.path.basename(f)}: {e}")
            continue
        
        col_map = {}
        for col in df.columns:
            col_lower = str(col).strip().lower()
            
            # Match material/product column
            if any(alias.lower() == col_lower for alias in material_col_aliases) and "Material_Name" not in col_map.values():
                col_map[col] = "Material_Name"
            # Match price/cost column
            elif any(alias.lower() == col_lower for alias in price_col_aliases) and "Price_USD" not in col_map.values():
                col_map[col] = "Price_USD"
            # Match date column
            elif any(alias.lower() == col_lower for alias in date_col_aliases) and "Timestamp" not in col_map.values():
                col_map[col] = "Timestamp"

        df = df.rename(columns=col_map)

        # Fallback 1: If no material column matched, pick the first text/string column
        if "Material_Name" not in df.columns:
            text_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(text_cols) > 0:
                df = df.rename(columns={text_cols[0]: "Material_Name"})

        # Fallback 2: If no price column matched, pick the first numeric column
        if "Price_USD" not in df.columns:
            num_cols = df.select_dtypes(include=[np.number]).columns
            if len(num_cols) > 0:
                df = df.rename(columns={num_cols[0]: "Price_USD"})

        # If we successfully mapped or found numerical price & categorical material
        if "Price_USD" in df.columns and "Material_Name" in df.columns:
            df["Price_USD"] = pd.to_numeric(df["Price_USD"], errors="coerce")
            if "Timestamp" not in df.columns:
                df["Timestamp"] = "2024-01-01" # Default placeholder date if timestamp is missing
                
            pricing_dfs.append(df[["Material_Name", "Price_USD", "Timestamp"]])
            print(f"  [VALIDATION] Successfully ingested & mapped: {os.path.basename(f)} ({len(df)} rows)")

    if pricing_dfs:
        merged_df = pd.concat(pricing_dfs, ignore_index=True)
    else:
        raise ValueError("No valid numeric pricing or metric columns found across uploaded files.")
        
    initial_count = len(merged_df)
    
    # 1. Null remediation
    merged_df = merged_df.dropna(subset=["Material_Name", "Price_USD"])
    
    # 2. Logic check (Filter out non-positive prices)
    merged_df = merged_df[merged_df["Price_USD"] > 0]
    
    # 3. Statistical Anomaly Removal (Z-Score > 3.0)
    merged_df["Z_Score"] = merged_df.groupby("Material_Name")["Price_USD"].transform(
        lambda x: np.abs(stats.zscore(x)) if len(x) > 1 else 0
    )
    
    outliers = merged_df[merged_df["Z_Score"] > 3.0]
    for idx in outliers.index:
        mat = merged_df.loc[idx, "Material_Name"]
        median_val = merged_df[(merged_df["Material_Name"] == mat) & (merged_df["Z_Score"] <= 3.0)]["Price_USD"].median()
        merged_df.loc[idx, "Price_USD"] = median_val if pd.notnull(median_val) else merged_df.loc[idx, "Price_USD"]
        
    merged_df = merged_df.drop(columns=["Z_Score"])
    
    output_path = os.path.join(processed_dir, "consolidated_clean_market_data.csv")
    merged_df.to_csv(output_path, index=False)
    
    print(f"\n[DATA HYGIENE COMPLETE] Successfully processed and merged {len(pricing_dfs)} files.")
    print(f"Saved clean master dataset to '{output_path}' ({len(merged_df)}/{initial_count} valid rows).")
    return merged_df

if __name__ == "__main__":
    validate_and_merge_datasets()
