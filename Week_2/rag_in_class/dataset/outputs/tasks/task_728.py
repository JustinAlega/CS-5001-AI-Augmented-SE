def sum_lists(list1, list2):
    """Return a new list where each element is the sum of corresponding elements from list1 and list2.

    Args:
        list1: First list of numbers
        list2: Second list of numbers (must be same length as list1)

    Returns:
        List of summed elements

    Raises:
        ValueError: If lists are of different lengths
    """
    if len(list1) != len(list2):
        raise ValueError("Input lists must be of equal length")

    return [a + b for a, b in zip(list1, list2)]
