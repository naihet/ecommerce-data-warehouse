from datetime import datetime

from sqlalchemy import text


def log_pipeline_run(
    engine,
    table_name: str,
    source_rows: int,
    processed_rows: int,
    started_at: datetime,
    completed_at: datetime,
    status: str,
):

    query = text(
        """
        INSERT INTO audit.pipeline_runs (
            table_name,
            source_rows,
            processed_rows,
            started_at,
            completed_at,
            status
        )
        VALUES (
            :table_name,
            :source_rows,
            :processed_rows,
            :started_at,
            :completed_at,
            :status
        )
        """
    )

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "table_name": table_name,
                "source_rows": source_rows,
                "processed_rows": processed_rows,
                "started_at": started_at,
                "completed_at": completed_at,
                "status": status,
            },
        )