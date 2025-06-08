import logging
from itertools import batched

import duckdb
import polars as pl
import pyarrow as pa

from blokk_solver.combinatorics import generate_all_blokk_samples

logger = logging.getLogger(__name__)


def stream_blokk_samples_to_duckdb(
    database="/tmp/quack.duckdb", cube_size=2, max_volume=4
):
    sample_generator = generate_all_blokk_samples(
        cube_volume=cube_size**3, max_volume=5
    )
    con = duckdb.connect(database=database, read_only=False)

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
            blokks INT8[],
            batch_idx INT
        )
    """)

    for batch_idx, batch in enumerate(batched(sample_generator, 10000)):
        # should really filter by blokk length < cube_length, though that becomes unimportant at higher dimensions.
        integer_partition_idx, blokk_ids = zip(*batch)

        df = pl.DataFrame(
            {
                "integer_partition_idx": pl.Series(
                    integer_partition_idx, dtype=pl.Int8
                ),
                "blokks": pl.Series(
                    [list(map(int, x)) for x in blokk_ids], dtype=pl.List(pl.Int8)
                ),
            },
        )

        # Insert using DuckDB's numpy array support
        con.sql(f"""
            INSERT INTO {table_name} (integer_partition_idx, blokks, batch_idx)
            SELECT *, '{batch_idx}' as batch_idx FROM df
        """)


def stream_blokk_samples_with_arrow(filename, cube_size, max_volume):
    sample_generator = generate_all_blokk_samples(
        cube_volume=cube_size**3, max_volume=5
    )

    schema = pa.schema(
        [
            pa.field("integer_partition_id", pa.int32()),
            pa.field("blokk_ids", pa.list_(pa.int8())),
        ]
    )

    local = fs.LocalFileSystem()
    with local.open_output_stream(filename) as stream:
        # with pa.ipc.RecordBatchStreamWriter(stream, schema) as writer:
        with csv.CSVWriter(stream, schema) as writer:
            for batch in batched(sample_generator, 10000):
                integer_partition_ids, blokk_ids = list(
                    zip(*batch)
                )  # transpose list of rows to list of cols
                blokk_ids = pa.array([list(x) for x in blokk_ids])
                integer_partition_ids = pa.array(integer_partition_ids)
                record_batch = pa.record_batch(
                    [integer_partition_ids, blokk_ids],
                    schema=schema,
                )
                writer.write_batch(record_batch)


if __name__ == "__main__":
    stream_blokk_samples_to_duckdb(cube_size=4, max_volume=5)
