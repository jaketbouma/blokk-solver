import logging
from itertools import batched

import duckdb
import pandas as pd

from blokk_solver.combinatorics import generate_all_blokk_samples

logger = logging.getLogger(__name__)


def stream_blokk_samples_to_disk(filename, cube_size, max_volume):
    sample_generator = generate_all_blokk_samples(
        cube_volume=cube_size**3, max_volume=5
    )
    con = duckdb.connect(database="my-db.duckdb", read_only=False)

    table_name = f"blokk_samples_cube{cube_size}_maxvol{max_volume}"
    sequence_name = f"sq_blokk_samples_cube{cube_size}_maxvol{max_volume}"

    # Drop table if it exists
    con.sql(f"DROP TABLE IF EXISTS {table_name}")
    con.sql(f"""DROP SEQUENCE IF EXISTS {sequence_name};
            CREATE SEQUENCE {sequence_name}""")

    # Create table
    con.sql(f"""
        CREATE TABLE {table_name} (
            sample_idx INT PRIMARY KEY DEFAULT nextval('{sequence_name}'),
            integer_partition_idx INTEGER,
            blokks INTEGER[]
        )
    """)

    for batch in batched(sample_generator, 10000):
        # save to disk

        # should really filter by blokk length < cube_length, though that becomes unimportant at higher dimensions.
        batch_data = pd.DataFrame(batch, columns=["integer_partition_idx", "blokks"])

        # Insert using DuckDB's numpy array support
        con.register("batch_data", batch_data)
        con.sql(f"""
            INSERT INTO {table_name} (integer_partition_idx, blokks)
            SELECT * FROM batch_data
        """)
        con.unregister("batch_data")


if __name__ == "__main__":
    # Example usage; adjust arguments as needed
    stream_blokk_samples_to_disk("testfile.txt", cube_size=2, max_volume=5)
