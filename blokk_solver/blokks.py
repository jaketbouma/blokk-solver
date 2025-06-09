import numpy as np
import pandas as pd

# import polars as pl  # noqa

# thanks copilot :doge:
_blokks = pd.DataFrame(
    [
        {
            "id": 1,
            "name": "Block 01",
            "color": "rgb(239, 139, 27)",
            "volume": 1,
            "shape": [(0, 0, 0)],
        },
        {
            "id": 2,
            "name": "Block 02",
            "color": "rgb(106, 194, 84)",
            "volume": 2,
            "shape": [(0, 0, 0), (1, 0, 0)],
        },
        {
            "id": 3,
            "name": "Block 03",
            "color": "rgb(244, 195, 203)",
            "volume": 3,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0)],
        },
        {
            "id": 4,
            "name": "Block 04",
            "color": "rgb(252, 221, 80)",
            "volume": 3,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0)],
        },
        {
            "id": 5,
            "name": "Block 05",
            "color": "purple-blue",
            "volume": 4,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)],
        },
        {
            "id": 6,
            "name": "Block 06",
            "color": "rgb(239, 139, 27)",
            "volume": 4,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)],
        },
        {
            "id": 7,
            "name": "Block 07",
            "color": "rgb(239, 139, 27)",
            "volume": 4,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0)],
        },
        {
            "id": 8,
            "name": "Block 08",
            "color": "rgb(239, 139, 27)",
            "volume": 4,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0)],
        },
        {
            "id": 9,
            "name": "Block 09",
            "color": "rgb(252, 221, 80)",
            "volume": 4,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)],
        },
        {
            "id": 10,
            "name": "Block 10",
            "color": "rgb(244, 195, 203)",
            "volume": 4,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0)],
        },
        {
            "id": 11,
            "name": "Block 11",
            "color": "rgb(239, 139, 27)",
            "volume": 4,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)],
        },
        {
            "id": 12,
            "name": "Block 12",
            "color": "rgb(106, 194, 84)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 13,
            "name": "Block 13",
            "color": "rgb(252, 221, 80)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 1, 0)],
        },
        {
            "id": 14,
            "name": "Block 14",
            "color": "rgb(239, 139, 27)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (2, 1, 0)],
        },
        {
            "id": 15,
            "name": "Block 15",
            "color": "rgb(252, 221, 80)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 16,
            "name": "Block 16",
            "color": "rgb(106, 194, 84)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 17,
            "name": "Block 17",
            "color": "rgb(106, 194, 84)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 18,
            "name": "Block 18",
            "color": "rgb(244, 195, 203)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 1, 0), (2, 1, 0)],
        },
        {
            "id": 19,
            "name": "Block 19",
            "color": "rgb(244, 195, 203)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0), (2, 0, 0)],
        },
        {
            "id": 20,
            "name": "Block 20",
            "color": "rgb(106, 194, 84)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 21,
            "name": "Block 21",
            "color": "rgb(106, 194, 84)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 22,
            "name": "Block 22",
            "color": "rgb(252, 221, 80)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 23,
            "name": "Block 23",
            "color": "rgb(239, 139, 27)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (1, 2, 0)],
        },
        {
            "id": 24,
            "name": "Block 24",
            "color": "rgb(252, 221, 80)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 1, 0), (2, 1, 0)],
        },
        {
            "id": 25,
            "name": "Block 25",
            "color": "rgb(244, 195, 203)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 26,
            "name": "Block 26",
            "color": "rgb(244, 195, 203)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 27,
            "name": "Block 27",
            "color": "rgb(87, 194, 230)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 1, 0)],
        },
        {
            "id": 28,
            "name": "Block 28",
            "color": "rgb(167, 99, 137)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 29,
            "name": "Block 29",
            "color": "rgb(87, 194, 230)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 30,
            "name": "Block 30",
            "color": "rgb(167, 99, 137)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (2, 1, 0)],
        },
        {
            "id": 31,
            "name": "Block 31",
            "color": "rgb(87, 194, 230)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)],
        },
        {
            "id": 32,
            "name": "Block 32",
            "color": "rgb(167, 99, 137)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 33,
            "name": "Block 33",
            "color": "rgb(87, 194, 230)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 34,
            "name": "Block 34",
            "color": "rgb(167, 99, 137)",
            "volume": 5,
            "shape": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 35,
            "name": "Block 35",
            "color": "rgb(87, 194, 230)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (2, 2, 0)],
        },
        {
            "id": 36,
            "name": "Block 36",
            "color": "rgb(167, 99, 137)",
            "volume": 5,
            "shape": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)],
        },
    ]
)


def get_blokks():
    blokks = _blokks.copy()
    blokks["voxels"] = blokks["shape"].apply(frozenset)
    blokks = blokks.set_index("id")
    blokks["max_length"] = blokks["shape"].apply(
        lambda points: max([coord for point in points for coord in point]) + 1
    )
    return blokks


def get_volume_to_ids(max_volume=5):
    volume_to_ids = (
        _blokks[_blokks["volume"] <= max_volume]
        .groupby("volume")["id"]
        .agg(set)
        .to_dict()
    )
    return volume_to_ids


def shape_to_game_board(shape, n, flatten=False):
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
