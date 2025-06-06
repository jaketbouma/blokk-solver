import json
import logging
from itertools import product
from typing import Optional

from joblib import Memory

from blokk_solver.blokks import get_blokks
from blokk_solver.combinatorics import (
    VoxelType,
    generate_all_blokk_samples,  # updated import
    generate_all_placements,
)

logger = logging.getLogger(__name__)


blokk_data = get_blokks()


location = "joblib-cache"
memory = Memory(location, verbose=0)


@memory.cache()
def cached_partitions(cube_volume, max_volume):
    yield generate_all_blokk_samples(cube_volume=cube_volume, max_volume=max_volume)


@memory.cache()
def cached_solutions(cube_volume, max_volume):
    solutions = []
    for blokk_ids in generate_all_blokk_samples(
        cube_volume=cube_volume,
        max_volume=max_volume,
    ):
        winning_build = solve(blokk_ids=blokk_ids)
        if winning_build is not None:
            solutions.append([{"ids": blokk_ids, "build": winning_build}])
    if len(solutions) == 0:
        return None
    return solutions


def solve_all_now(cube_volume, max_volume=5):
    solutions = []
    for integer_partition_number, blokk_ids in generate_all_blokk_samples(
        cube_volume=cube_volume,
        max_volume=max_volume,  # updated call
    ):
        first_winning_build = solve(blokk_ids=blokk_ids) or []
        solutions.append(
            [{"ids": blokk_ids, "first_winning_build": first_winning_build}]
        )
    return solutions


def solve(blokk_ids: set[int]) -> Optional[set[frozenset[VoxelType]]]:
    blokk_voxels: list[frozenset[VoxelType]] = blokk_data.loc[
        list(blokk_ids), "voxels"
    ].tolist()

    all_blokk_placements: list[set[frozenset[VoxelType]]] = [
        generate_all_placements(voxels) for voxels in blokk_voxels
    ]
    all_build_attempts = product(*all_blokk_placements)
    for build in all_build_attempts:
        build_success = _test_build(set(build))
        if build_success:
            return set(build)
    return None


def _test_build(build: set[frozenset[VoxelType]]) -> bool:
    seen_voxels: set[VoxelType] = set()
    for blokk in build:
        for voxel in blokk:
            if voxel in seen_voxels:
                return False
            else:
                seen_voxels.add(voxel)
    return True


def hash_partition(n: int, partition: frozenset) -> str:
    return json.dumps({"n": n, "ids": sorted(partition)})


def unhash_partition(s: str) -> tuple[int, frozenset]:
    """
    Parse a JSON string of the form '{"n": 27, "ids": [1,2,3]}' and return (n, frozenset of ids).
    """
    data = json.loads(s)
    n = data["n"]
    ids = frozenset(data["ids"])
    return n, ids
