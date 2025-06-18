from collections import defaultdict
from dataclasses import dataclass
from typing import FrozenSet, Iterable, Optional

import numpy as np

from blokk_solver._blokk_data import blokk_data
from blokk_solver.geometry import VoxelType, generate_all_placements

# thanks copilot :doge:


@dataclass
class Blokk:
    id: int
    name: str
    color: str
    volume: int
    voxels: FrozenSet[VoxelType]
    max_length: int = 0

    def __post_init__(self):
        self.max_length = max([coord for point in self.voxels for coord in point]) + 1


def get_blokks(ids: Optional[Iterable[int]] = None) -> list[Blokk]:
    all_blokks = [Blokk(**data) for data in blokk_data]
    if ids is not None:
        ids_set = set(ids)
        return [b for b in all_blokks if b.id in ids_set]
    return all_blokks


def get_volume_to_ids(
    cube_size: Optional[int] = None, max_blokk_volume=None
) -> dict[int, set[int]]:
    volume_to_ids = defaultdict(set)
    for blokk in get_blokks():
        if cube_size is not None and blokk.max_length > cube_size:
            continue
        if max_blokk_volume is not None and blokk.volume > max_blokk_volume:
            continue
        volume_to_ids[blokk.volume].add(blokk.id)
    return volume_to_ids


def get_id_to_placements(cube_size=5) -> dict[int, set[frozenset[VoxelType]]]:
    id_to_placements = {}
    for blokk in get_blokks():
        placements = generate_all_placements(blokk.voxels, cube_size=cube_size)
        id_to_placements[blokk.id] = placements
    return id_to_placements


def shape_to_game_board(
    shape: FrozenSet[VoxelType], n: int, flatten: bool = False
) -> np.ndarray:
    """
    shape: list of coordinates (each coordinate is a tuple of 3 ints)
    n: size of the nxnxn game grid
    flatten: if True, return the gameboard as a 1D vector of length n*n*n

    Returns:
        np.ndarray: nxnxn array (or flattened vector) with 1s at blokk positions, 0 elsewhere
    """
    board = np.zeros((n, n, n), dtype=int)
    for coord in shape:
        x, y, z = coord
        board[x, y, z] = 1
    if flatten:
        return board.flatten()
    return board
