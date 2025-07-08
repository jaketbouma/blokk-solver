import logging

import dlt

from blokk_solver.combinatorics import BlokkCombinatorics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# could move this into the class?
@dlt.resource(
    name="blokk_samples",
    write_disposition="replace",
    primary_key="sample",
    columns={
        # "sample_idx": {"data_type": "bigint"},
        "integer_partition_idx": {"data_type": "bigint"},
        "sample": {"data_type": "json"},
    },
)
def sample_generator(max_blokk_volume=None, cube_size=3):
    combinatorics = BlokkCombinatorics(
        max_blokk_volume=max_blokk_volume, cube_size=cube_size
    )
    for partition_samples in combinatorics.generate_all_blokk_samples_by_partition():
        sample = {
            "integer_partition_idx": partition_samples["idx"],
            "sample": [sorted(s) for s in partition_samples["samples"]],
        }
        yield sample


def run_pipeline(
    dataset_name=None, max_blokk_volume=4, cube_size=4, database_name=None
):
    # some defaults
    if dataset_name is None:
        dataset_name = f"cube_{cube_size}" + (
            f"_v{max_blokk_volume}"
            if max_blokk_volume is None or max_blokk_volume >= 5
            else ""
        )
    if database_name is None:
        database_name = "blokk.duckdb"

    pipeline = dlt.pipeline(
        dataset_name=dataset_name,
        destination=dlt.destinations.duckdb(database_name),
        progress="enlighten",
    )
    pipeline.run(
        sample_generator(max_blokk_volume=max_blokk_volume, cube_size=cube_size)
    )

    return pipeline
