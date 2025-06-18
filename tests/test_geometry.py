import pytest

from blokk_solver.blokks import get_blokks
from blokk_solver.geometry import generate_all_placements, generate_rotations


def test_blokk_2():
    # Example "id=2" blokk: a 2-voxel straight piece (could be [[0,0,0],[1,0,0]])
    blokk2 = get_blokks(ids={2})[0]
    voxels = blokk2.voxels
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
def test_blokk_12_placements(n, expected_placements):
    blokk12 = get_blokks(ids={12})[0]
    voxels = blokk12.voxels
    placements = generate_all_placements(voxels, cube_size=n)
    assert len(placements) == expected_placements
