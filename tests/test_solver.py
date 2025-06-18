import pytest  # noqa

from blokk_solver.solver import solve_all_now


# Test for the trivial cases with low volume
@pytest.mark.parametrize(
    argnames="cube_size,max_blokk_volume,expected_number_of_solutions",
    argvalues=[
        # there is one solution to 1x1x1
        (1, 1, 1),
        (1, None, 1),
        # there are no solutions to 2x2x2
        (2, 1, 0),
        (2, 2, 0),
        (2, None, 0),
    ],
)
def test_trivial_cases(cube_size, max_blokk_volume, expected_number_of_solutions):
    solutions = solve_all_now(cube_size=cube_size, max_blokk_volume=max_blokk_volume)
    assert len(solutions) == expected_number_of_solutions


@pytest.mark.skip(reason="Too slow for a test")
def test_solve_3x3x3():
    solutions = solve_all_now(cube_size=3, max_blokk_volume=5)
    # ...
    # assert len(solutions) == 0  # ??
