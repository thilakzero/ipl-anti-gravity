import pandas as pd

REQUIRED_COLS = ['player_name', 'role', 'strike_rate', 'average', 'wickets', 'economy', 'recent_form']

def validate_and_preprocess(df):
    """
    Validates the uploaded data against expected schema,
    handles missing values, and normalizes inputs.
    """
    # 1. Validate Columns
    # Assuming user might have slightly different caps, lower everything for check
    df.columns = [c.lower() for c in df.columns]
    
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    # 2. Fill Missing or Null Values
    # We replace NaNs safely with 0 for most stats, handling missing player cases.
    df['strike_rate'] = df['strike_rate'].fillna(0)
    df['average'] = df['average'].fillna(0)
    df['wickets'] = df['wickets'].fillna(0)
    df['economy'] = df['economy'].fillna(0)
    
    # Default form to a neutral 50 if missing
    df['recent_form'] = df['recent_form'].fillna(50)  

    # 3. Ensure correct types (convert strings capable of numeric representations)
    numeric_cols = ['strike_rate', 'average', 'wickets', 'economy', 'recent_form']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df
