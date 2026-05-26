
"""
Utility functions for analysis and map preparation.
"""

import pandas as pd


def get_compliance_summary(df: pd.DataFrame) -> pd.DataFrame:
    """EUDR Compliance Summary"""
    return df.groupby('compliance_status').agg({
        'lot_id': 'count',
        'sca_score': ['mean', 'max'],
        'available_quantity_kg': 'sum',
        'eudr_compliant': 'sum'
    }).round(2)


def get_region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Deep regional performance"""
    return df.groupby('region').agg({
        'sca_score': ['mean', 'max', 'count'],
        'eudr_compliant': 'sum',
        'deforestation_risk': lambda x: (x == 'Low').sum(),
        'available_quantity_kg': 'sum',
        'farmer_premium_usd': 'mean'
    }).round(2)


def get_traceability_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Traceability level analysis"""
    return df.groupby('traceability_level').agg({
        'lot_id': 'count',
        'sca_score': 'mean',
        'eudr_compliant': 'sum',
        'available_quantity_kg': 'sum'
    }).round(2)


def filter_for_eu_market(df: pd.DataFrame):
    """Filter lots suitable for EU market (high standards)"""
    return df[
        (df['eudr_compliant'] == True) &
        (df['sca_score'] >= 85) &
        (df['deforestation_risk'] != 'High')
    ]
