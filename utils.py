import pandas as pd
import numpy as np

def engineer_features(df):
    """
    Robust feature engineering for the Smart Study system.
    Ensures consistent columns and handling of edge cases (zeros, missing).
    """
    df = df.copy()
    
    # Fill missing with sensible defaults for inference if not provided
    defaults = {
        'study_hours': 1.0,
        'focus_score': 5.0,
        'previous_score': 70.0,
        'sleep_hours': 7.0,
        'break_time': 0.5,
        'distraction_level': 'medium',
        'day_of_week': 'Monday'
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val
            
    # Clip to avoid division by zero
    sh = df['study_hours'].astype(float).clip(lower=0.1)
    fs = df['focus_score'].astype(float).clip(lower=0.1)
    sl = df['sleep_hours'].astype(float)
    bt = df['break_time'].astype(float)
    ps = df['previous_score'].astype(float)
    
    # Core engineered features
    df['efficiency_base'] = (fs * ps) / sh
    df['sleep_focus_ratio'] = sl / fs
    df['break_ratio'] = bt / sh
    df['distraction_penalty'] = df['distraction_level'].map({'low': 1, 'medium': 2, 'high': 3}).fillna(2)
    df['weekend_flag'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    
    return df
