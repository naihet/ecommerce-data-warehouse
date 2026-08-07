import uuid
import pandas as pd
from sqlalchemy import text

def load_dataframe(
    df,
    engine,
    table_name,
    schema,
):

    temp_table = f"temp_{uuid.uuid4().hex[:8]}"

    df.to_sql(
        temp_table,
        engine,
        schema=schema,
        if_exists="replace",
        index=False,
    )

    print(temp_table)