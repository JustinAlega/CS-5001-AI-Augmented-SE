def heap_sort(arr):
    """Sorts the input array in ascending order using heap sort algorithm.

    Args:
        arr: List of comparable elements to be sorted in-place.

    Returns:
        The sorted list (same reference as input).
    """
    if not arr:
        return arr

    _heapify(arr)
    _shift_down(arr, 0, len(arr) - 1)

    end = len(arr) - 1
    while end > 0:
        arr[end], arr[0] = arr[0], arr[end]
        _shift_down(arr, 0, end - 1)
        end -= 1
    return arr

def _heapify(arr):
    """Converts the array into a max-heap in-place."""
    start = (len(arr) - 1) // 2
    while start >= 0:
        _shift_down(arr, start, len(arr) - 1)
        start -= 1

def _shift_down(arr, start, end):
    """Shifts the element at 'start' down the heap to maintain heap property."""
    root = start
    while (child := root * 2 + 1) <= end:
        if child + 1 <= end and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break
