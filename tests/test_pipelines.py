import logging
import os

import duckdb

from blokk_solver import _blokk_data
from pipelines import sampling_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_sample_pipeline():
    db_path = "_test_databases/pytest.duckdb"
    dataset_name = "cube3"
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"Deleted existing database file: {db_path}")
    sampling_pipeline.run_pipeline(
        dataset_name=dataset_name,
        cube_size=3,
        max_blokk_volume=4,
        database_name=db_path,
    )

    # read the records back from duckdb and count them
    with duckdb.connect(db_path) as con:
        result = con.execute(
            f"SELECT COUNT(*) FROM {dataset_name}.blokk_samples"
        ).fetchone()
        count = result[0] if result else 0
        logger.info(f"Number of records in 'blokk_samples' table: {count}")
    expected_count = len(_blokk_data.ways_to_sample_c3_from_v4)
    assert count == expected_count, (
        f"Expected {expected_count} records, found {count} in samples table."
    )
