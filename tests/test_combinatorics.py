from blokk_solver.combinatorics import generate_partitions


def test_generate_partitions_9():
    expected = [
        [4, 5],
        [2, 3, 4],
        [1, 4, 4],
        [1, 3, 5],
        [1, 2, 3, 3],
    ]
    result = generate_partitions(9)
    # Sort inner lists and outer list for comparison
    result_sorted = sorted([sorted(part) for part in result])
    expected_sorted = sorted([sorted(part) for part in expected])
    assert result_sorted == expected_sorted


def test_generate_partitions_27():
    expected = [
        [4, 4, 4, 5, 5, 5],
        [3, 4, 5, 5, 5, 5],
        [3, 4, 4, 4, 4, 4, 4],
        [3, 3, 4, 4, 4, 4, 5],
        [2, 5, 5, 5, 5, 5],
        [2, 4, 4, 4, 4, 4, 5],
        [2, 3, 4, 4, 4, 5, 5],
        [2, 3, 3, 4, 5, 5, 5],
        [1, 4, 4, 4, 4, 5, 5],
        [1, 3, 4, 4, 5, 5, 5],
        [1, 3, 3, 5, 5, 5, 5],
        [1, 3, 3, 4, 4, 4, 4, 4],
        [1, 2, 4, 5, 5, 5, 5],
        [1, 2, 4, 4, 4, 4, 4, 4],
        [1, 2, 3, 4, 4, 4, 4, 5],
        [1, 2, 3, 3, 4, 4, 5, 5],
    ]
    result = generate_partitions(27)
    result_sorted = sorted([sorted(part) for part in result])
    expected_sorted = sorted([sorted(part) for part in expected])
    assert result_sorted == expected_sorted
