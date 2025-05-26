import numpy as np
import pytest  # noqa

from blokk_solver.blokks import get_blokks
from blokk_solver.combinatorics import generate_all_placements, generate_partitions


@pytest.fixture()
def blokks():
    return get_blokks()


#
# Basic blokk placement tests


def test_blokk_2_placements(blokks):
    # Example "id=2" blokk: a 2-voxel straight piece (could be [[0,0,0],[1,0,0]])
    voxels = blokks.loc[2, "voxels"]
    assert np.array_equal(voxels, [[0, 0, 0], [1, 0, 0]])

    # There should be 54 unique placements of a 2-voxel straight piece in a 3x3x3 board
    placements3 = generate_all_placements(voxels, n=3)
    assert (
        placements3.shape[0] == (3 * 3) * 2 * 3
    )  # (9 placements x 2 shifts x 3 rotations) = 54

    # There should be 54 unique placements of a 2-voxel straight piece in a 4x4x4 board
    placements4 = generate_all_placements(voxels, n=4)

    assert (
        placements4.shape[0] == (4 * 4) * 3 * 3
    )  # (16 placements x 3 shifts x 3 rotations) = 144


def test_blokk_12_placements(blokks):
    voxels = blokks.loc[12, "voxels"]
    placements2 = generate_all_placements(voxels, n=2)
    placements3 = generate_all_placements(voxels, n=3)
    placements4 = generate_all_placements(voxels, n=4)
    assert placements2 is not None


def test_generate_partitions_9():
    expected = [
        [4, 5],
        [2, 3, 4],
        [1, 4, 4],
        [1, 3, 5],
        [1, 2, 3, 3],
    ]
    result = generate_partitions(9)
    # Sort inner lists and outer list for comparison
    result_sorted = sorted([sorted(part) for part in result])
    expected_sorted = sorted([sorted(part) for part in expected])
    assert result_sorted == expected_sorted


def test_generate_partitions_27():
    expected = [
        [4, 4, 4, 5, 5, 5],
        [3, 4, 5, 5, 5, 5],
        [3, 4, 4, 4, 4, 4, 4],
        [3, 3, 4, 4, 4, 4, 5],
        [2, 5, 5, 5, 5, 5],
        [2, 4, 4, 4, 4, 4, 5],
        [2, 3, 4, 4, 4, 5, 5],
        [2, 3, 3, 4, 5, 5, 5],
        [1, 4, 4, 4, 4, 5, 5],
        [1, 3, 4, 4, 5, 5, 5],
        [1, 3, 3, 5, 5, 5, 5],
        [1, 3, 3, 4, 4, 4, 4, 4],
        [1, 2, 4, 5, 5, 5, 5],
        [1, 2, 4, 4, 4, 4, 4, 4],
        [1, 2, 3, 4, 4, 4, 4, 5],
        [1, 2, 3, 3, 4, 4, 5, 5],
    ]
    result = generate_partitions(27)
    result_sorted = sorted([sorted(part) for part in result])
    expected_sorted = sorted([sorted(part) for part in expected])
    assert result_sorted == expected_sorted
