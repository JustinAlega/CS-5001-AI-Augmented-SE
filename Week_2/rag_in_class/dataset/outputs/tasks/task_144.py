def sum_pairs(arr, n):
    """Calculate the sum of pairs in the array with alternating signs.

    For each element at index i (0-based), the contribution to the sum is:
    - Positive if the index is even (0, 2, 4, ...)
    - Negative if the index is odd (1, 3, 5, ...)

    Args:
        arr: List of numbers
        n: Number of elements to consider (from the end of the array)

    Returns:
        The calculated sum
    """
    total = 0
    for i in range(n - 1, -1, -1):
        if (n - 1 - i) % 2 == 0:
            total += arr[i]
        else:
            total -= arr[i]
    return total
