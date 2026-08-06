import pandas as pd


def load_dataframe(
    df: pd.DataFrame,
    engine,
    table_name: str,
    schema: str,
):
    """
    Load dataframe into PostgreSQL.
    """

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False,
    )