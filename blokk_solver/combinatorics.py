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


def _sample_by_volume(
    volume: int,
    n: int,
    volume_to_ids: dict[int, list[int]],
) -> set:
    """
    Generates a set of all unique samples of n blokks
    of volume v from the volume_to_ids dict.

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


def generate_cube_volume_samples(cube_volume: int, max_volume=5):
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
            # to [[ids], ...]
            yield frozenset(chain.from_iterable(play))


def all_rotation_matrices() -> list[np.ndarray]:
    """
    Generate all 24 proper rotation matrices of the cube (the octahedral group, no reflections).

    Returns:
        List[np.ndarray]: A list of 3x3 numpy arrays, each representing a rotation matrix (dtype=int).
    """
    rots = R.create_group("O")
    # Ensure all matrices are integer-valued
    return [np.round(rot.as_matrix()).astype(int) for rot in rots]


def normalize_shape(voxels: frozenset[VoxelType]) -> frozenset[VoxelType]:
    """
    Normalize a set of 3D coordinates so that the minimum value along each axis is zero.

    Args:
        voxels (list of tuples): List of (x, y, z) coordinates.

    Returns:
        List[Tuple[int, int, int]]: Normalized coordinates as a list of tuples.
    """
    xs, ys, zs = zip(*voxels)
    min_x, min_y, min_z = min(xs), min(ys), min(zs)
    return frozenset([(x - min_x, y - min_y, z - min_z) for (x, y, z) in voxels])


def generate_rotations(
    voxels: frozenset[VoxelType],
) -> set[frozenset[VoxelType]]:
    """
    Generates all unique rotations of a blokk (represented by a set of 3D voxels).

    Args:
        voxels (list): A list of 3D coordinates representing the voxels of the blokk.

    Returns:
        List[List[Tuple[int, int, int]]]: List of unique voxel coordinate lists, each corresponding to a rotation.
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
    n: int,
) -> set[frozenset[VoxelType]]:
    """
    Generate all unique translations of the blokk shape defined by voxels, within the nxnxn game board.
    Returns a list of translated shapes (each as a list of (x, y, z) tuples).
    """
    voxels_array = np.array(list(voxels), dtype=int)
    min_coords = voxels_array.min(axis=0)
    max_coords = voxels_array.max(axis=0)
    shape_size = max_coords - min_coords + 1

    translations = set()
    for dx in range(n - shape_size[0] + 1):
        for dy in range(n - shape_size[1] + 1):
            for dz in range(n - shape_size[2] + 1):
                offset = np.array([dx, dy, dz]) - min_coords
                translated = voxels_array + offset
                if np.all((0 <= translated) & (translated < n)):
                    translations.add(frozenset(map(tuple, translated)))
    return translations


def generate_all_placements(
    voxels: frozenset[VoxelType], n=3
) -> set[frozenset[VoxelType]]:
    """
    Generate all possible unique placements of a blokk within an n x n x n grid.

    This function computes all unique placements by generating all possible rotations of the input voxels,
    then translating each rotation within the bounds of the grid. Duplicate placements are removed.

    Args:
        voxels (list of tuples): The coordinates of the voxels to be placed.
        n (int, optional): The size of the cubic grid along each axis. Defaults to 3.

    Returns:
        List[List[Tuple[int, int, int]]]: All unique placements of the input voxels within the grid.
    """
    rotations = generate_rotations(voxels)
    placements = set()
    for rotation in rotations:
        translations = generate_translations(rotation, n=n)
        placements.update(translations)
    # Remove duplicates
    print(f"generated {len(rotations)} rotations = {len(placements)} unique placements")
    return placements


def voxels_to_gameboard(voxels: list[VoxelType], n: int = 5, flatten=False):
    """
    Converts a list of voxel coordinates into a 3D gameboard array.

    Args:
        voxels (list of tuples): List of (x, y, z) coordinates.
        n (int, optional): Size of the gameboard along each dimension (creates an n x n x n grid). Defaults to 5.
        flatten (bool, optional): If True, returns the gameboard as a flattened 1D array of length n*n*n. Defaults to False.

    Returns:
        np.ndarray: An n x n x n numpy array (or a flattened 1D array if `flatten` is True) with 1s at the specified voxel positions and 0s elsewhere.
    """
    board = np.zeros((n, n, n), dtype=int)
    for x, y, z in voxels:
        board[x, y, z] = 1
    if flatten:
        return board.flatten()
    return board
    return board
