import logging
from collections import Counter
from itertools import chain, combinations, product
from typing import Generator

import enlighten

from blokk_solver._blokk_data import p_n_by_cube
from blokk_solver.blokks import get_volume_to_ids
from pads.IntegerPartition import mckay

logger = logging.getLogger(__name__)


def accel_asc(n, m):
    """grabbed this one;
    https://jeromekelleher.net/tag/integer-partitions.html

    honestly I can't figure out how to restrict even the simpler
    version of this algorithm, so I just filter the yields here
    for now and fingers crossed for the tests :D
    """
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    idx = 0
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            idx += 1
            if a[k] <= m:  # patched in
                yield idx, a[: k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1

        idx += 1
        if a[k] <= m:  # patched in
            yield idx, a[: k + 1]


print(list(accel_asc(8, 4)))


class BlokkCombinatorics:
    def __init__(self, max_blokk_volume, cube_size):
        self.max_blokk_volume = max_blokk_volume
        self.cube_size = cube_size
        self.volume_to_ids = get_volume_to_ids(
            cube_size=cube_size, max_blokk_volume=max_blokk_volume
        )

        self.n_integer_partitions = p_n_by_cube[self.cube_size]

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

    def generate_all_blokk_samples_by_partition(
        self, progress_bar=False
    ) -> Generator[tuple[int, list[frozenset[int]]]]:
        """
        Yield all unique sets of blokk IDs whose volumes sum to cube_volume,
        using only blokks with volume <= max_volume.
        """
        # loop through integer partitions
        integer_partitions = accel_asc(self.cube_size**3, m=self.max_blokk_volume)

        manager = enlighten.get_manager()
        pbar = manager.counter(
            total=self.n_integer_partitions, desc="Basic", unit="ticks"
        )

        for integer_partition_number, integer_partition in integer_partitions:
            # loop through all possible ways to sample that partition
            blokk_samples = self.generate_blokk_samples_from_integer_partition(
                integer_partition
            )
            pbar.update(incr=integer_partition_number - pbar.position)
            for blokk_sample in blokk_samples:
                if blokk_sample is not None:
                    yield (integer_partition_number, list(blokk_samples))
