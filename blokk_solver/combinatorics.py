import logging
from collections import Counter
from itertools import chain, combinations, product
from typing import Generator, TypeAlias

import numpy as np
from joblib import Memory
from scipy.spatial.transform import Rotation as R

from blokk_solver.blokks import get_volume_to_ids
from pads.IntegerPartition import mckay

logger = logging.getLogger(__name__)

VoxelType: TypeAlias = tuple[int, int, int]


location = "cache/combinatorics"
memory = Memory(location, verbose=0)


def generate_blokk_samples_from_integer_partition(
    integer_partition: list[int], max_volume: int
) -> Generator[frozenset[int]]:
    v_to_ids = get_volume_to_ids(max_volume=max_volume)

    # the number of blokks (n) needed per blokk volume (volume)
    v_to_n: dict[int, int] = Counter(integer_partition)

    # generate all ways to sample n blocks of volume v
    v_to_samples: dict[int, set[tuple[int]]] = {}
    for v, n in v_to_n.items():
        ids = v_to_ids.get(v, None)
        if ids is None or n > len(ids):
            return None
        samples = set(combinations(v_to_ids[v], r=n))
        v_to_samples[v] = samples

    # generate cartesian product of n ways for each volume v
    plays = product(*v_to_samples.values())
    for play in plays:
        # flatten from [[(ids with v1), (ids with v2), ...], ...]
        # to [ids, ...]
        yield frozenset(chain.from_iterable(play))


@memory()
def generate_all_blokk_samples(
    cube_volume: int, max_volume=5
) -> Generator[tuple[int, frozenset[int]]]:
    """
    Yield all unique sets of blokk IDs whose volumes sum to cube_volume,
    using only blokks with volume <= max_volume.
    """

    # loop through integer partitions
    integer_partitions = mckay(cube_volume)
    for idx, integer_partition in enumerate(integer_partitions):
        for blokk_sample in generate_blokk_samples_from_integer_partition(
            integer_partition, max_volume=max_volume
        ):
            if blokk_sample is not None:
                yield (idx, blokk_sample)


@memory()
def all_rotation_matrices() -> list[np.ndarray]:
    """
    Return all 24 proper rotation matrices of the cube (octahedral group, no reflections).
    Each matrix is a 3x3 numpy array of dtype int.
    """
    rots = R.create_group("O")
    # Ensure all matrices are integer-valued
    return [np.round(rot.as_matrix()).astype(int) for rot in rots]


def normalize_shape(voxels: frozenset[VoxelType]) -> frozenset[VoxelType]:
    """
    Normalize a set of 3D coordinates so the minimum value along each axis is zero.
    """
    xs, ys, zs = zip(*voxels)
    min_x, min_y, min_z = min(xs), min(ys), min(zs)
    return frozenset([(x - min_x, y - min_y, z - min_z) for (x, y, z) in voxels])


@memory()
def generate_rotations(
    voxels: frozenset[VoxelType],
) -> set[frozenset[VoxelType]]:
    """
    Return all unique rotations of a blokk, represented by a set of 3D voxels.
    """
    # use numpy for rotation
    voxels_matrix = np.array(sorted(voxels), dtype=int)
    rotations = all_rotation_matrices()

    blokk_rotations = set()
    for rotation_matrix in rotations:
        rotated_voxels_matrix = np.dot(voxels_matrix, rotation_matrix.T)
        rotated_voxels = frozenset(
            [frozenset(voxel_as_array) for voxel_as_array in rotated_voxels_matrix]
        )
        normalized_voxels = normalize_shape(rotated_voxels)
        blokk_rotations.add(frozenset(normalized_voxels))
    return blokk_rotations


@memory()
def generate_translations(
    voxels: frozenset[VoxelType],
    cube_size: int,
) -> set[frozenset[VoxelType]]:
    """
    Return all unique translations of the blokk shape within a cube_size x cube_size x cube_size board.
    """
    voxels_array = np.array(list(voxels), dtype=int)
    min_coords = voxels_array.min(axis=0)
    max_coords = voxels_array.max(axis=0)
    shape_size = max_coords - min_coords + 1

    translations = set()
    for dx in range(cube_size - shape_size[0] + 1):
        for dy in range(cube_size - shape_size[1] + 1):
            for dz in range(cube_size - shape_size[2] + 1):
                offset = np.array([dx, dy, dz]) - min_coords
                translated = voxels_array + offset
                if np.all((0 <= translated) & (translated < cube_size)):
                    translations.add(frozenset(map(tuple, translated)))
    return translations


@memory()
def generate_all_placements(
    voxels: frozenset[VoxelType], cube_size=3
) -> set[frozenset[VoxelType]]:
    """
    Return all unique placements of a blokk within a cube_size x cube_size x cube_size grid,
    considering all rotations and translations.
    """
    rotations = generate_rotations(voxels)
    placements = set()
    for rotation in rotations:
        translations = generate_translations(rotation, cube_size=cube_size)
        placements.update(translations)
    # Remove duplicates
    print(f"generated {len(rotations)} rotations = {len(placements)} unique placements")
    return placements
