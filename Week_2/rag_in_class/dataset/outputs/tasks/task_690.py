def multiply_consecutive_numbers(numbers):
    """Return a list of products of each pair of consecutive numbers in the input list.

    Args:
        numbers: List of numbers to process.

    Returns:
        List of products where each element is the product of two consecutive numbers
        from the input list. The length of the result is len(numbers) - 1.
    """
    return [a * b for a, b in zip(numbers[:-1], numbers[1:])]
