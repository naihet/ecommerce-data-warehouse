import pandas as pd


def get_new_records(
    source_df: pd.DataFrame,
    target_df: pd.DataFrame,
    primary_key: str,
) -> pd.DataFrame:
    """
    Return records that do not already exist in target.
    """

    return source_df[
        ~source_df[primary_key].isin(
            target_df[primary_key]
        )
    ]