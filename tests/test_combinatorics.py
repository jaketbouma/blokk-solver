import pytest  # noqa

from blokk_solver.blokks import get_blokks
from blokk_solver.combinatorics import (
    generate_all_placements,
    generate_partitions,
    generate_rotations,
)


@pytest.fixture()
def blokks():
    return get_blokks()


#
# Basic blokk placement tests


def test_blokk_2(blokks):
    # Example "id=2" blokk: a 2-voxel straight piece (could be [[0,0,0],[1,0,0]])
    voxels = blokks.loc[2, "voxels"]
    expected_voxels = {(0, 0, 0), (1, 0, 0)}
    assert voxels == expected_voxels

    rotations = generate_rotations(voxels)
    assert len(rotations) == 3

    # There should be 54 unique placements of a 2-voxel straight piece in a 3x3x3 board
    placements3 = generate_all_placements(voxels, n=3)
    assert (
        len(placements3) == (3 * 3) * 2 * 3
    )  # (9 placements x 2 shifts x 3 rotations) = 54

    # There should be 54 unique placements of a 2-voxel straight piece in a 4x4x4 board
    placements4 = generate_all_placements(voxels, n=4)

    # There should be 54 unique placements of a 2-voxel straight piece in a 5x5x5 board
    placements5 = generate_all_placements(voxels, n=5)
    assert (
        len(placements5) == (5 * 5) * 4 * 3
    )  # (25 placements x 4 shifts x 3 rotations) = 300


def test_blokk_12_placements(blokks):
    voxels = blokks.loc[12, "voxels"]
    placements2 = generate_all_placements(voxels, n=2)
    placements3 = generate_all_placements(voxels, n=3)
    placements4 = generate_all_placements(voxels, n=4)


@pytest.mark.skip(reason="Skipping test for generate_partitions(27)")
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


@pytest.mark.skip(reason="Skipping test for generate_partitions(27)")
def test_generate_partitions_27_outcome():
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


def test_generate_partitions_27(flatten=True):
    # there are 88 different samples of blokks with volume <= 3 [NOT CONFIRMED]
    assert len(list(generate_partitions(27, max_volume=3, flatten=True))) == 88

    # there are 0 different samples of blokks with volume <= 2 [NOT CONFIRMED]
    assert len(list(generate_partitions(27, max_volume=2, flatten=True))) == 0
