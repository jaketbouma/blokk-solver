![Banner](assets/banner-001.png)
# Blokk! Solver
> [Blokk!](https://blokk.games/) is the ultimate puzzle game. It is easy to learn, but hard to master. It's also an interesting mathematical and algorithmic puzzle, which this project explores.

## Goals
| **Now** | **Later** |
|:--------|:---------|
| - Determine all solutions to the game<br>- Develop an API for set(pieces) -> set(solutions) | - UX with a 3D viewer of solutions<br>- An AI player (RL?) |

## Integer Partition Algorithm
**🎯 Goal:** Find all subsets of the game pieces that can be assembled into a perfect cube of dimension `cube_size` with volume `cube_size**3`.

The first algorithm is based on the [Integer Partition](https://en.wikipedia.org/wiki/Integer_partition) problem, scanning through and testing subsets of game pieces based on their volume.

## Data prep
1. Generate all the subsets of `blokks` that have a combined voxel volume equal to the perfect volume `cube_size**3`. This is analogous to the integer partition problem, which is solved with sequential generation, and doesn't parallelize well, so we save these subsets to disk. The saved partitions can then be parallelized and track/resume progress.
2. Separately generate all possible rotations and translations of the blokk within the cube. Cache these.

## Parallel processing of each subset:
1. Iterate through the cartesian product of all possible rotations and translations of each blokk in the subset
   1. Add the blokks together.
   2. If no voxels overlap, then this subset is a solution!
   3. If any voxels overlap, this is not a solution. Continue searching.
2. If you have processed the last element of the product, and haven't yet found a solution, then this subset is not a solution.
3. Save the outcome to disk.

## Running the code
Prerequisites
* Python poetry
* Optionally, duckdb cli
Installation steps
1. Install with `poetry install`
2. Run tests with `poetry run pytest`
3. Check the available commands with `poetry run poe`
4. Generate and write blokk samples to duckdb `poetry run poe save-blokk-samples`
4. Generate and write blokk rotations and translations to duckdb `poetry run poe save-blokk-positions` (coming soon)
5. Optionally, inspect and analyze the results with the duckdb ui `duckdb -ui blokk.duckdb`
6. ... and more to follow

---
[Kickstarter](https://www.kickstarter.com/projects/blokkgames/blokk-dare-to-be-square) | [Instagram](https://www.instagram.com/blokk.games) | [Get in touch to contribute](mailto:jake@honestgrowth.no)


