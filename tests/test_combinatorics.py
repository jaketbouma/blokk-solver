import pandas as pd
import pytest  # noqa

from blokk_solver.blokks import get_blokks
from blokk_solver.combinatorics import (
    generate_all_blokk_samples,  # renamed import
    generate_all_placements,
    generate_rotations,
)


@pytest.fixture()
def blokks() -> pd.DataFrame:
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
    placements3 = generate_all_placements(voxels, cube_size=3)
    assert (
        len(placements3) == (3 * 3) * 2 * 3
    )  # (9 placements x 2 shifts x 3 rotations) = 54

    # There should be 144 unique placements of a 2-voxel straight piece in a 4x4x4 board
    placements4 = generate_all_placements(voxels, cube_size=4)
    assert (
        len(placements4) == (4 * 4) * 3 * 3
    )  # (16 placements x 3 shifts x 3 rotations) = 54

    # There should be 54 unique placements of a 2-voxel straight piece in a 5x5x5 board
    placements5 = generate_all_placements(voxels, cube_size=5)
    assert (
        len(placements5) == (5 * 5) * 4 * 3
    )  # (25 placements x 4 shifts x 3 rotations) = 300


@pytest.mark.parametrize(
    argnames="n,expected_placements",
    argvalues=[
        (2, 0),
        (3, 36),  # not confirmed
        (4, 192),  # not confirmed
        (5, 540),  # not confirmed
    ],
)
def test_blokk_12_placements(blokks, n, expected_placements):
    voxels = blokks.loc[12, "voxels"]
    placements = generate_all_placements(voxels, cube_size=n)
    assert len(placements) == expected_placements


# Test for the trivial cases with low volume
@pytest.mark.parametrize(
    argnames="volume,expected_samples",
    # expected possible blokk samples making up volume in form:
    # (volume, [{id,}, ])
    argvalues=[
        (0, [set()]),
        (1, [{1}]),
        (2, [{2}]),
        (3, [{3}, {4}, {1, 2}]),
        (4, [{4, 1}, {3, 1}, {5}, {6}, {7}, {8}, {9}, {10}, {11}]),
    ],
)
def test_trivial_all_blokk_samples(volume, expected_samples):
    samples = [s for _, s in generate_all_blokk_samples(volume)]
    expected_samples = set([frozenset(x) for x in expected_samples])
    assert set(samples) == expected_samples
    assert len(samples) == len(expected_samples)


@pytest.mark.parametrize(
    "max_volume,expected_number_of_samples,expected_last_partition_idx",
    [
        (2, 0, -1),
        (3, 0, -1),
        (4, 42, 2788),  # not confirmed
        (5, 565622, 2788),  # not confirmed
    ],
)
def test_generate_all_blokk_samples_27(
    blokks,
    max_volume,
    expected_number_of_samples,
    expected_last_partition_idx,
):
    count = 0
    last_partition_idx = -1
    for partition_idx, samples in generate_all_blokk_samples(27, max_volume=max_volume):
        count += 1
        last_partition_idx = partition_idx
    assert last_partition_idx == expected_last_partition_idx
    assert count == expected_number_of_samples


@pytest.mark.skip(reason="Too slow for a test")
@pytest.mark.parametrize(
    "max_volume,expected_number_of_samples,expected_last_partition_idx",
    [
        (2, 0, -1),
        (3, 0, -1),
        (4, 42, 2788),  # not confirmed
        # (5, 565622, 2788),  # not confirmed
    ],
)
def test_generate_all_blokk_samples_64(
    blokks,
    max_volume,
    expected_number_of_samples,
    expected_last_partition_idx,
):
    count = 0
    last_partition_idx = -1
    for partition_idx, samples in generate_all_blokk_samples(64, max_volume=max_volume):
        count += 1
        last_partition_idx = partition_idx
    assert last_partition_idx == expected_last_partition_idx
    assert count == expected_number_of_samples
