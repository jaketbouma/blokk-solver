import pandas as pd
import pytest  # noqa

from blokk_solver.blokks import get_blokks
from blokk_solver.solver import solve_all_now


@pytest.fixture()
def blokks() -> pd.DataFrame:
    return get_blokks()


# Test for the trivial cases with low volume
@pytest.mark.parametrize(
    argnames="cube_volume,max_volume,expected_number_of_solutions",
    argvalues=[
        # there are no solutions to 2x2x2 using only blokks with volume <=2
        (8, 1, 0),
        (8, 2, 0),
        # there is one solution to 2x2x2 using only blokks with volume <= 3:
        (8, 3, 1),
        # there are 36? solutions to 2x2x2 using only blokks with volume <= 4:
        (8, 4, 36),
        # there are 111? solutions to 2x2x2 using any blokks:
        (8, 100, 111),
    ],
)
def test_trivial_cases(cube_volume, max_volume, expected_number_of_solutions):
    solutions = solve_all_now(cube_volume=cube_volume, max_volume=max_volume)
    assert len(solutions) == expected_number_of_solutions


@pytest.mark.skip(reason="Too slow for a test")
def test_solve_3x3x3():
    solutions = solve_all_now(cube_volume=27, max_volume=5)
    # ...
    # assert len(solutions) == 0  # ??
