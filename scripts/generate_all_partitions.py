import argparse
import logging
from itertools import batched

import duckdb
import polars as pl
import pyarrow as pa
from tqdm import tqdm

from blokk_solver.combinatorics import generate_all_blokk_samples

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def stream_blokk_samples_to_duckdb(
    database="blokk.duckdb",
    cube_size=2,
    max_volume=5,
    database_schema=None,
    restart=True,
):
    if database_schema is None:
        database_schema = f"cube_{cube_size}"
    table_name = f"{database_schema}.samples_{max_volume}"
    sequence_name = f"{database_schema}.sq_samples_{max_volume}"

    sample_generator = generate_all_blokk_samples(
        cube_volume=cube_size**3, max_volume=5
    )

    con = duckdb.connect(database=database, read_only=False)

    if not restart:
        raise (NotImplementedError("Restart comes later"))
        try:
            result = con.sql(f"""
                select max(integer_partition_idx) as continue from {table_name}
            """).fetchone()
            restart_point = result[0] if result is not None else 0
            logger.info(f"restarting from {restart_point}")
        except ValueError:
            logger.warning("Could not access previously saved data, restarting.")
            restart = True

    if restart:
        logger.info(f"Recreating {table_name}")
        # Drop table if it exists
        con.sql(f"CREATE SCHEMA IF NOT EXISTS {database_schema}")
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

    # Wrap batch enumeration with tqdm for progress tracking
    batch_size = 10000
    logger.info(f"Processing batches of {batch_size} rows")
    for batch_idx, batch in enumerate(
        tqdm(batched(sample_generator, batch_size), desc="Inserting batches")
    ):
        # should really filter by blokk length < cube_length,
        # though that becomes unimportant at higher dimensions.
        integer_partition_idx, blokk_ids = zip(*batch)

        df = pl.DataFrame(
            {
                "integer_partition_idx": pl.Series(
                    integer_partition_idx, dtype=pl.UInt32
                ),
                "blokks": pl.Series(
                    [list(map(int, x)) for x in blokk_ids], dtype=pl.List(pl.Int8)
                ),
            },
        )
        logger.debug(f"Prepared polars df {df}")

        # Insert using DuckDB's numpy array support
        con.sql(f"""
            INSERT INTO {table_name} (integer_partition_idx, blokks, batch_idx)
            SELECT *, '{batch_idx}' as batch_idx FROM df
        """)
    logger.info("Insertion completed successfully.")

    # After all batches, check row count and print
    result = con.sql(f"SELECT COUNT(*) FROM {table_name}").fetchone()
    logger.info(f"Inserted {result[0]} rows into {table_name}")


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
    parser = argparse.ArgumentParser(
        description="Generate and store blokk samples in DuckDB."
    )
    parser.add_argument(
        "--cube-size", type=int, default=2, help="Cube size (default: 2)"
    )
    parser.add_argument(
        "--max-volume", type=int, default=4, help="Max volume (default: 4)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Set logging level (default: DEBUG)",
    )
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level.upper())
    logger.setLevel(args.log_level.upper())

    stream_blokk_samples_to_duckdb(
        cube_size=args.cube_size,
        max_volume=args.max_volume,
        restart=True,
    )
