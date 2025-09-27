"""
Aggregate structured fields extracted from multiple forms into a DataFrame and provide simple stats.
"""
from typing import List, Dict
import pandas as pd


def aggregate_fields(list_of_field_dicts: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(list_of_field_dicts)
    return df


def top_k_counts(df: pd.DataFrame, column: str, k: int = 5):
    if column not in df.columns:
        return None
    return df[column].value_counts().head(k)
