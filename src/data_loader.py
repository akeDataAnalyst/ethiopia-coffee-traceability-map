
"""
Data loading, validation and preprocessing module for Traceability Project.
"""

import pandas as pd
from .config import MOCK_DATA_CSV, PROCESSED_PICKLE


def load_traceability_data() -> pd.DataFrame:
    """Load data with priority: Pickle → CSV"""
    if PROCESSED_PICKLE.exists():
        df = pd.read_pickle(PROCESSED_PICKLE)
        print(f"Loaded {len(df)} lots from processed pickle file")
    elif MOCK_DATA_CSV.exists():
        df = pd.read_csv(MOCK_DATA_CSV)
        # Convert datetime columns
        date_cols = ['arrival_date', 'last_audit_date', 'last_updated']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        print(f"Loaded {len(df)} lots from raw CSV")
    else:
        raise FileNotFoundError("No traceability data found. Please run Phase 1 first.")

    return df


def validate_and_enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply business rules and enrich the dataset"""
    df = df.copy()

    # Calculated fields
    df['available_quantity_kg'] = df['quantity_bags'] * 60.0

    # Quality Tier
    df['quality_tier'] = pd.cut(
        df['sca_score'],
        bins=[0, 82, 85, 88, 100],
        labels=['Good', 'Very Good', 'Excellent', 'Outstanding']
    )

    # Risk Score (simple weighted score)
    risk_score = {'Low': 1, 'Medium': 2, 'High': 3}
    df['risk_score'] = df['deforestation_risk'].map(risk_score)

    return df
