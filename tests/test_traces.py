import pytest

from cachesim.traces import loop, sequential, thrash, uniform, zipf


def test_sequential_repeats_pages() -> None:
    assert sequential(10, 4) == [0, 1, 2, 3, 0, 1, 2, 3, 0, 1]


def test_loop_repeats_full_cycles() -> None:
    assert loop(3, 2) == [0, 1, 2, 0, 1, 2]


def test_uniform_is_deterministic() -> None:
    first = uniform(50, 10, seed=7)
    second = uniform(50, 10, seed=7)

    assert first == second
    assert len(first) == 50
    assert set(first) <= set(range(10))


def test_zipf_is_deterministic() -> None:
    first = zipf(50, 10, seed=7)
    second = zipf(50, 10, seed=7)

    assert first == second
    assert len(first) == 50
    assert set(first) <= set(range(10))


def test_thrash_working_set_is_one_page_larger_than_cache() -> None:
    trace = thrash(100, 3)

    assert len(trace) == 100
    assert set(trace) <= set(range(4))


def test_invalid_sizes_are_rejected() -> None:
    with pytest.raises(ValueError):
        sequential(0, 4)
    with pytest.raises(ValueError):
        loop(0, 1)
    with pytest.raises(ValueError):
        uniform(10, 0)
