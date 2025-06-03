import logging
from collections import Counter
from itertools import chain, combinations, product
from typing import TypeAlias

import numpy as np
from scipy.spatial.transform import Rotation as R

from blokk_solver.blokks import get_volume_to_ids
from pads.IntegerPartition import mckay

logger = logging.getLogger(__name__)

VoxelType: TypeAlias = tuple[int, int, int]


def solve(cube_size, blokks: frozenset[frozenset[VoxelType]]):
    all_blokk_placements: list[set[frozenset[VoxelType]]] = [
        generate_all_placements(blokk, cube_size) for blokk in blokks
    ]
    all_build_attempts = product(*all_blokk_placements)
    for build in all_build_attempts:
        logger.debug(build)
        break


def _sample_by_volume(
    volume: int,
    n: int,
    volume_to_ids: dict[int, list[int]],
) -> set:
    """
    Return all unique samples of n blokks of the given volume from volume_to_ids.
    Returns an empty set if no samples can be made.
    """
    try:
        ids = volume_to_ids[volume]
    except KeyError:
        return set()

    if len(ids) < n:
        return set()

    samples = set(combinations(ids, r=n))

    return samples


def generate_cube_volume_samples(cube_volume: int, max_volume=5) -> frozenset[int]:
    """
    Yield all unique sets of blokk IDs whose volumes sum to cube_volume,
    using only blokks with volume <= max_volume.
    """
    volume_to_ids = {
        volume: ids
        for volume, ids in get_volume_to_ids().items()
        if volume <= max_volume
    }

    # loop through integer partitions
    integer_partitions = mckay(cube_volume)
    for integer_partition in integer_partitions:
        # the number of blokks per blokk volume
        volume_to_n: dict[int, int] = Counter(integer_partition)

        # try fill the volume from blokks
        selections = []
        partition_is_possible = True
        for volume, n in volume_to_n.items():
            volume_samples = _sample_by_volume(volume, n, volume_to_ids)
            if len(volume_samples) > 0:
                selections.append(volume_samples)
            else:
                partition_is_possible = False
                break

        # partition is not possible
        if not partition_is_possible:
            continue

        # generate cartesian product of all the ways
        # to fill each factor of the partition
        plays = product(*selections)
        for play in plays:
            # flatten from [[(ids with vol1), (ids with vol2), ...], ...]
            # to [ids, ...]
            yield frozenset(chain.from_iterable(play))


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
        rotated_voxels = [
            tuple(voxel_as_array) for voxel_as_array in rotated_voxels_matrix
        ]
        normalized_voxels: set = normalize_shape(rotated_voxels)
        blokk_rotations.add(frozenset(normalized_voxels))
    return blokk_rotations


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
