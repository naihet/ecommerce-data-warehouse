import pandas as pd


#=============

def validate_not_empty(df: pd.DataFrame):

    if df.empty:
        raise ValueError("DataFrame is empty")

#=============

def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str]
):

    missing = [
        c
        for c in required_columns
        if c not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

#=============

def validate_primary_key(
    df: pd.DataFrame,
    column: str
):

    if df[column].duplicated().any():

        raise ValueError(
            f"Duplicate values found in {column}"
        )

#=============

def validate_null_primary_key(
    df: pd.DataFrame,
    column: str
):

    if df[column].isnull().any():

        raise ValueError(
            f"Null values found in {column}"
        )