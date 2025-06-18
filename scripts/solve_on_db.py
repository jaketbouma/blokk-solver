import logging

import duckdb

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def iterate_through_duckdb_samples(
    table_name,
    database,
    size=10000,
    loglevel="INFO",
):
    with duckdb.connect(database=database, read_only=True) as read_con:
        query = read_con.execute(f"""
            select blokks, from {table_name}
        """)

        while batch := query.fetchmany(size=size):
            logger.debug(f"N={len(batch)}")
            # solve the batch
            _solve_a_batch(batch)


def _solve_a_batch(batch):
    for blokk_ids in batch:
        pass


if __name__ == "__main__":
    iterate_through_duckdb_samples(
        table_name="blokk.cube_2.samples_5",
        database="blokk.duckdb",
        size=20,
    )
