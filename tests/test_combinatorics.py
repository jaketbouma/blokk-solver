import pytest  # noqa

from blokk_solver._blokk_data import ways_to_sample_c3_from_v4
from blokk_solver.blokks import Blokk, get_blokks
from blokk_solver.combinatorics import BlokkCombinatorics


@pytest.fixture()
def blokks() -> list[Blokk]:
    return get_blokks()


# Test for the trivial cases with low volume
@pytest.mark.parametrize(
    argnames="max_blokk_volume,cube_size,expected_samples",
    # expected possible blokk samples making up volume in form:
    # (volume, [{id,}, ])
    argvalues=[
        (0, 1, []),
        (0, 2, []),
        (1, 1, [{1}]),
        (2, 1, [{1}]),
        (None, 1, [{1}]),
        # You can't build a 2x2x2 cube in blokk [?]
        (None, 2, []),
        # You can't build a 3x3x3 with on v3 blokks [?]
        (3, 3, []),
        (4, 3, ways_to_sample_c3_from_v4),
    ],
)
def test_trivial_all_blokk_samples(max_blokk_volume, cube_size, expected_samples):
    combinatorics = BlokkCombinatorics(
        max_blokk_volume=max_blokk_volume, cube_size=cube_size
    )
    samples = [s for _, s in combinatorics.generate_all_blokk_samples()]
    expected_samples = set([frozenset(x) for x in expected_samples])
    assert set(samples) == expected_samples
    assert len(samples) == len(expected_samples)
