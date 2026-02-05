def is_nonagonal(n):
    """Calculate the nth nonagonal number.

    Args:
        n: The position in the sequence of nonagonal numbers.

    Returns:
        The nth nonagonal number.
    """
    return int(n * (7 * n - 5) / 2)
