![Banner](assets/banner-001.png)
# Blokk! Solver
> [Blokk!](https://blokk.games/) is the ultimate puzzle game. It is easy to learn, but hard to master. It's also an interesting mathematical and algorithmic puzzle, which this project explores.

### Goals
| **Now** | **Later** |
|:--------|:---------|
| - Determine all solutions to the game<br>- Develop an API for set(pieces) -> set(solutions) | - UX with a 3D viewer of solutions<br>- An AI player (RL?) |

### Algorithm 1.0
Given a large set of game `blokks` that may be used to build a cube of dimension `cube_size` with perfect volume `cube_size**3`.

Prep. Build the following data structures
1. Generate all the subsets of `blokks` that have a combined voxel volume equal to the perfect volume. Base the solution on integer partitions. This is a sequential generation that doesn't parallelize well, so save these subsets to disk. They can then be used to parallelize and track/resume progress.
1. Generate all possible rotations and translations of the blokk within the cube. Cache these.

Parallel processing of each subset:
1. Iterate through the cartesian product of all possible rotations and translations of each blokk in the subset
   1. Add the blokks together.
   2. If no voxels overlap, then this subset is a solution!
   3. If any voxels overlap, this is not a solution. Continue searching.
2. If you have processed the last element of the product, and haven't yet found a solution, then this subset is not a solution.
3. Save the outcome to disk.

### Running the project
Prerequisites;
* Python poetry
* Optionally, duckdb cli

1. Install with `poetry install`
2. Build the samples `poetry run poe save-blokk-samples`
3. ...

---
[Kickstarter](https://www.kickstarter.com/projects/blokkgames/blokk-dare-to-be-square) | [Instagram](https://www.instagram.com/blokk.games) | [Get in touch to contribute](mailto:jake@honestgrowth.no)


