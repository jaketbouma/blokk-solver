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
        (0, 1, set()),
        (0, 2, set()),
        (1, 1, set([frozenset([1])])),
        (2, 1, set([frozenset([1])])),
        (None, 1, set([frozenset([1])])),
        # You can't build a 2x2x2 cube in blokk [?]
        (None, 2, set()),
        # You can't build a 3x3x3 with v3 blokks [?]
        (3, 3, set()),
        # Exponentially more samples from here onwards
        (4, 3, ways_to_sample_c3_from_v4),
    ],
)
def test_trivial_all_blokk_samples_by_partition(
    max_blokk_volume, cube_size, expected_samples
):
    combinatorics = BlokkCombinatorics(
        max_blokk_volume=max_blokk_volume, cube_size=cube_size
    )

    samples: set[frozenset[int]] = set(
        [
            sample
            for partition_result in combinatorics.generate_all_blokk_samples_by_partition()
            for sample in partition_result["samples"]
        ]
    )

    # check the total volume of each sample is correct
    id_to_v = {
        id: vol for vol, ids in combinatorics.volume_to_ids.items() for id in ids
    }
    for sample in samples:
        total_volume = sum(id_to_v[id] for id in sample)
        assert total_volume == cube_size**3

    # check for exact match if given
    if expected_samples is not None:
        assert len(samples) == len(expected_samples)
        assert samples == expected_samples
