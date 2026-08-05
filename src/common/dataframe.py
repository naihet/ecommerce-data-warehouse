import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply common cleaning rules.
    """

    df = df.drop_duplicates()

    """
    Remove duplicate rows.

    Remove rows containing only NULL values.
    """
    
    df = df.dropna(how="all")

    return df