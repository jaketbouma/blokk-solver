import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.transform import Rotation as R

from pads.IntegerPartition import mckay


def generate_partitions(n: int):
    integer_partitions = mckay(n)
    for integer_partition in integer_partitions:
        yield integer_partition


def all_rotation_matrices() -> list[ArrayLike]:
    """
    Generate all 24 proper rotation matrices of the cube (the octahedral group, no reflections).

    Returns:
        List[np.ndarray]: A list of 3x3 numpy arrays, each representing a rotation matrix.
    """

    # The 24 rotation matrices of the cube (proper rotations, no reflections)
    rots = R.create_group("O")  # 'O' is the octahedral group (24 elements)
    return [rot.as_matrix().round().astype(int) for rot in rots]


def normalize_shape(voxels: list[ArrayLike]) -> list[ArrayLike]:
    """
    Normalize a set of 3D coordinates so that the minimum value along each axis is zero.

    Args:
        coords (array-like): List or array of shape (N, 3), where each row is a (x, y, z) coordinate.

    Returns:
        Tuple[Tuple[int, int, int], ...]: Normalized coordinates as a tuple of tuples.
    """
    # Shift so min coordinate is at (0,0,0)
    arr = np.array(voxels)
    arr -= arr.min(axis=0)
    return arr


def generate_rotations(voxels: list) -> list:
    """
    Generates all unique rotations of a blokk (represented by a set of 3D voxels).

    Args:
        voxels (list): A list of 3D coordinates representing the voxels of the blokk.

    Returns:
        np.ndarray: An array of unique voxel coordinates, each corresponding to proper rotations.
    """
    blokk = np.array(voxels)
    rotations = all_rotation_matrices()

    blokk_rotations = [voxels]
    for rotation_matrix in rotations:
        rotated = np.dot(blokk, rotation_matrix.T)
        # Normalize to start at (0,0,0)
        norm = rotated - rotated.min(axis=0)
        blokk_rotations.append(norm)

    return np.unique(blokk_rotations, axis=0)


def generate_translations(voxels, n):
    """
    Generate all unique translations of the blokk shape defined by voxels, within the nxnxn game board.
    Returns a list of translated shapes (each as a list of [x, y, z] coordinates).
    """

    voxels = np.array(voxels)
    min_coords = voxels.min(axis=0)
    max_coords = voxels.max(axis=0)
    shape_size = max_coords - min_coords + 1

    translations = []
    for dx in range(n - shape_size[0] + 1):
        for dy in range(n - shape_size[1] + 1):
            for dz in range(n - shape_size[2] + 1):
                translated = voxels - min_coords + np.array([dx, dy, dz])
                if np.all((translated >= 0) & (translated < n)):
                    translations.append(translated.tolist())
    return translations


def voxels_to_gameboard(voxels: list[ArrayLike], n: int = 5, flatten=False):
    """
    Converts a list of voxel coordinates into a 3D gameboard array.

    Args:
        voxels (list[ArrayLike]): List of coordinates, where each coordinate is a list or tuple of 3 integers (x, y, z).
        n (int, optional): Size of the gameboard along each dimension (creates an n x n x n grid). Defaults to 5.
        flatten (bool, optional): If True, returns the gameboard as a flattened 1D array of length n*n*n. Defaults to False.

        np.ndarray: An n x n x n numpy array (or a flattened 1D array if `flatten` is True) with 1s at the specified voxel positions and 0s elsewhere.
    """
    board = np.zeros((n, n, n), dtype=int)
    for coords in voxels:
        x, y, z = map(int, coords)  # notype
        board[x, y, z] = 1
    if flatten:
        return board.flatten()
    return board
