import itertools
import logging
from operator import itemgetter

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
    itertools.groupby(combinatorics.generate_all_blokk_samples(), key=itemgetter(0))
    for sample_idx, (integer_partition_idx, blokk_ids) in enumerate(
        combinatorics.generate_all_blokk_samples()
    ):
        sample = {
            # "sample_idx": sample_idx,
            "integer_partition_idx": integer_partition_idx,
            "sample": sorted(blokk_ids),
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

    # Get the trace of the last run of the pipeline
    # The trace contains timing information on extract, normalize, and load steps
    trace = pipeline.last_trace

    # Load the trace information into a table named "_trace" in the destination
    pipeline.run([trace], table_name="_trace")

    return pipeline
