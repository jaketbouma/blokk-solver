import json
import logging
from itertools import product
from typing import Optional

from blokk_solver.blokks import get_blokks
from blokk_solver.combinatorics import BlokkCombinatorics
from blokk_solver.geometry import VoxelType, generate_all_placements

logger = logging.getLogger(__name__)


def solve_all_now(cube_size, max_blokk_volume=5):
    combinatorics = BlokkCombinatorics(
        max_blokk_volume=max_blokk_volume, cube_size=cube_size
    )
    solutions = []
    for (
        integer_partition_number,
        blokk_ids,
    ) in combinatorics.generate_all_blokk_samples():
        first_winning_build = solve(blokk_ids=set(blokk_ids)) or []
        solutions.append(
            [{"ids": blokk_ids, "first_winning_build": first_winning_build}]
        )
    return solutions


def solve(blokk_ids: set[int]) -> Optional[set[frozenset[VoxelType]]]:
    # a list of blokks
    blokks = get_blokks(blokk_ids)

    # a list where each element is all possible placements of a blokk
    all_blokk_placements = [generate_all_placements(blokk.voxels) for blokk in blokks]

    # take the cartesian produce of all those lists
    all_build_attempts = product(*all_blokk_placements)

    # and then test all of those possibilities
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
