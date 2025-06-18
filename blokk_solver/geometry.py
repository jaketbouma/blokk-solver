import logging
from typing import TypeAlias

import numpy as np
from scipy.spatial.transform import Rotation as R

VoxelType: TypeAlias = tuple[int, int, int]

logger = logging.getLogger(__name__)


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
        rotated_voxels = frozenset(
            [tuple(voxel_as_array) for voxel_as_array in rotated_voxels_matrix]
        )
        normalized_voxels = normalize_shape(rotated_voxels)
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
