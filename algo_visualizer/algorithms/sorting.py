# algorithms/sorting.py
from typing import List, Generator, Tuple, Optional


State = Tuple[List[int], Optional[int], Optional[int]]
# (array snapshot, index_a, index_b)


def bubble_sort(arr: List[int]) -> Generator[State, None, None]:
    a = arr[:]  # work on a copy
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            # yield comparison
            yield (a[:], j, j + 1)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                # yield after swap
                yield (a[:], j, j + 1)
    # final state
    yield (a[:], None, None)


def insertion_sort(arr: List[int]) -> Generator[State, None, None]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        # show key selection
        yield (a[:], i, None)
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            yield (a[:], j, j + 1)
            j -= 1
        a[j + 1] = key
        yield (a[:], j + 1, None)
    yield (a[:], None, None)


def selection_sort(arr: List[int]) -> Generator[State, None, None]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            # highlight current comparison
            yield (a[:], min_idx, j)
            if a[j] < a[min_idx]:
                min_idx = j
                yield (a[:], i, min_idx)
        a[i], a[min_idx] = a[min_idx], a[i]
        yield (a[:], i, min_idx)
    yield (a[:], None, None)
