import logging
from collections import Counter
from itertools import chain, combinations, product
from typing import Generator

from blokk_solver.blokks import get_volume_to_ids
from pads.IntegerPartition import mckay

logger = logging.getLogger(__name__)


class BlokkCombinatorics:
    def __init__(self, max_blokk_volume, cube_size):
        self.max_blokk_volume = max_blokk_volume
        self.cube_size = cube_size
        self.volume_to_ids = get_volume_to_ids(
            cube_size=cube_size, max_blokk_volume=max_blokk_volume
        )

    def generate_blokk_samples_from_integer_partition(
        self, integer_partition: list[int]
    ) -> Generator[frozenset[int]]:
        # the number of blokks (n) needed per blokk volume (volume)
        v_to_n: dict[int, int] = Counter(integer_partition)

        # generate all ways to sample n blocks of volume v
        v_to_samples: dict[int, set[tuple[int]]] = {}
        for v, n in v_to_n.items():
            ids = self.volume_to_ids.get(v, None)
            if ids is None or n > len(ids):
                return None
            samples = set(combinations(self.volume_to_ids[v], r=n))
            v_to_samples[v] = samples

        # generate cartesian product of n ways for each volume v
        plays = product(*v_to_samples.values())
        for play in plays:
            # flatten from [[(ids with v1), (ids with v2), ...], ...]
            # to [ids, ...]
            yield frozenset(chain.from_iterable(play))

    def generate_all_blokk_samples(self) -> Generator[tuple[int, frozenset[int]]]:
        """
        Yield all unique sets of blokk IDs whose volumes sum to cube_volume,
        using only blokks with volume <= max_volume.
        """

        # loop through integer partitions
        integer_partitions = mckay(self.cube_size**3)
        for idx, integer_partition in enumerate(integer_partitions):
            # loop through all possible ways to sample that partition
            for blokk_sample in self.generate_blokk_samples_from_integer_partition(
                integer_partition
            ):
                if blokk_sample is not None:
                    yield (idx, blokk_sample)
